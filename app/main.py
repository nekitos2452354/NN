from flask import Flask, render_template, request, jsonify
import requests

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
import numpy as np

app = Flask(__name__)

GEONAMES_USERNAME = "nokia"  

@app.route('/')
def index():
    return render_template('index.html')

def get_cities_from_geonames(query=""): #получание списка городов через geonames
    url = "http://api.geonames.org/searchJSON"
    unique_cities = set()
    name = ""
    if query:
        max_rows = 10
    else:
        max_rows = 20

    for start in range(0, 100000, max_rows):
        params = {
            "country": "RU",
            "featureClass": "P",
            "maxRows": max_rows,
            "startRow": start,
            "username": GEONAMES_USERNAME,
            "lang": "ru",
        }
        if query:
            params["name_startsWith"] = query

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            #print(data)
        except Exception as e:
            print(f"Ошибка при запросе GeoNames (start={start}): {e}")
            break

        geonames = data.get("geonames", [])
        if not geonames:
            break

        for place in geonames:
            name = place.get("name")
            if name:
                unique_cities.add(name)

        if query:
            break

    return sorted(unique_cities)



cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)



def get_coordinates_from_geonames(city_name): #получаем координаты города по названию
    url = "http://api.geonames.org/searchJSON"
    params = {
        "q": city_name,
        "maxRows": 1,
        "username": GEONAMES_USERNAME,
        "country": "RU",
        "featureClass": "P",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["geonames"]:
            lat = float(data["geonames"][0]["lat"])
            lon = float(data["geonames"][0]["lng"])
            return lat, lon
        else:
            raise ValueError("Город не найден")
    except Exception as e:
        print(f"Ошибка при получении координат: {e}")
        return None, None

def get_temp_by_city(city_name):  #Получаем температуру по координатам
    lat, lon = get_coordinates_from_geonames(city_name)
    if lat is None or lon is None:
        print("Координаты не получены")
        return

    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m"
        }

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        return hourly_temperature_2m
    except Exception as e:
        print(f"Ошибка при запросе GeoNames: {e}")
        return None

import pandas as pd


@app.route('/api/get-cities')  #Получаем список городов для поиска
def api_get_cities():
    query = request.args.get('query', '').strip()
    cities = get_cities_from_geonames(query)
    return jsonify(cities)

@app.route('/api/get-temp')
def api_get_temp():

    city_name = request.args.get('city_name', '').strip()  
    

    if not city_name:  
        city_name = request.cookies.get('last_search')
        if not city_name:
            city_name = "Москва"
    

    try:
        temp_data = np.array(get_temp_by_city(city_name))
        response_data = {
            "city": city_name,  
            "temperatures": temp_data.tolist()
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    response = jsonify(response_data)
    response.set_cookie(
        'last_search',
        city_name,
        max_age=30*24*60*60,
        secure=True,
        httponly=True,
        samesite='Lax'
    )
    return response
    
   


@app.route('/api/get-day')  #Получаем сегодняшний день недели 
def api_get_day():
    dates = pd.date_range(start=pd.Timestamp.today(), periods=8)
    day = dates.strftime('%A').to_list()
    return jsonify(day)
    
@app.route('/api/get-day-data') # Получаем сегодняшнюю дату
def api_get_data():
    dates = pd.date_range(start=pd.Timestamp.today(), periods=8)
    day_data = dates.strftime('%d-%m').to_list()
    return jsonify(day_data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)