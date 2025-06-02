 🌤 Weather Forecast App
 ---

A web application that shows the weather forecast for a selected city. The app remembers the last searched city and automatically loads its weather on the next visit. City suggestions are provided via the GeoNames API, and the weather data is retrieved from the Open-Meteo API. The backend is powered by Flask and containerized with Docker.

---

🚀 Features

- City autocomplete via **GeoNames API**
- Weather data via **Open-Meteo API**
- Remembers last searched city using **localStorage**
- Backend with **Flask**
- Containerized with **Docker**

---

📦 Installation and Run (Docker)

bash
docker build -t flask_app .
docker run -p 5000:5000 flask_app

The app will be available at http://localhost:5000

🧑‍💻 Developer
Developed solo by NOKIA.

---
🌤 Приложение прогноза погоды
---
Веб-приложение, которое показывает прогноз погоды для выбранного города. Сохраняет последний введённый город и автоматически показывает его погоду при следующем посещении. Есть подсказки городов через API GeoNames и прогноз через Open-Meteo API. Backend построен на Flask, приложение упаковано в Docker.

---

🚀 Возможности

 - Подсказки при вводе города (GeoNames API)
 - Получение прогноза погоды (Open-Meteo API)
 - Сохранение последнего города через localStorage
 - Backend на Flask
 - Контейнеризация через Docker

---

📦 Установка и запуск (Docker)
    bash
docker build -t flask_app .
docker run -p 5000:5000 flask_app

Приложение будет доступно по адресу: http://localhost:5000

👤 Автор

Разработано самостоятельно — NOKIA.
