
async function loadCities(query) {
    const response = await fetch(`/api/get-cities?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data;
}

async function loadTemp(city_name){
    const response = await fetch(`/api/get-temp?city_name=${encodeURIComponent(city_name)}`);
    const data = await response.json();
    return data;
}

async function loadDay(){
    const response = await fetch('/api/get-day');
    const data = await response.json();
    return await data;
}
async function loadData(){
    const response = await fetch(`/api/get-day-data`);
    const data = await response.json();
    return await data;
}


const cityInput = document.getElementById("CityInput");
const autocompleteList = document.getElementById("autocomplete-list");

cityInput.addEventListener("input", async function () {
    const inputVal = this.value;
    autocompleteList.innerHTML = "";

    if (!inputVal) return;

    const cities = await loadCities(inputVal);

    const filtered = cities.filter(city =>
        city.toLowerCase().includes(inputVal.toLowerCase())
    );

    filtered.forEach(city => {
        const itemElement = document.createElement("div");
        itemElement.classList.add("itemElement")
        itemElement.innerHTML = city;

        itemElement.addEventListener("click", async function () {
            cityInput.value = this.innerHTML;
            autocompleteList.innerHTML = "";
            fetchWeather(cityInput.value);

        });

        autocompleteList.appendChild(itemElement);
    });
});



document.addEventListener("click", function(e) {
    if (e.target !== cityInput) {
        autocompleteList.innerHTML = "";
    }
});

const days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];



async function days_add(temp){
    const loadDays = await loadDay();
    const loadDays_data = await loadData();

    
    days.forEach(day => {
        dayAdd = document.getElementById(day);
        const thisDay = days.indexOf(day);
        let dayName;
        switch(loadDays[thisDay]) {
            case "Monday":
              dayName = 'Понедельник';
              break;
            case "Tuesday":
              dayName = 'Вторник';
              break;
            case "Wednesday":
              dayName = 'Среда';
              break;
            case "Thursday":
              dayName = 'Четверг';
              break;
            case "Friday":
              dayName = 'Пятница';
              break;
            case "Saturday":
              dayName = 'Суббота';
              break;
            case "Sunday":
              dayName = 'Воскресенье';
              break;
        }
        const daydata = document.createElement("h3");
        const allData = document.createElement("div");
        const blockL = document.createElement("div");
        const blockR = document.createElement("div");

        allData.classList.add("allData"); 
        blockL.classList.add("block"); 
        blockR.classList.add("block"); 

        daydata.textContent = loadDays_data[thisDay] + " " + dayName;
        console.log(loadDays[thisDay]);

        dayAdd.appendChild(daydata);
        const createAllData = dayAdd.appendChild(allData);
        const createBlockL = createAllData.appendChild(blockL);
        const createBlockR = createAllData.appendChild(blockR);

        for (let hour = 0; hour < 24; hour++) {
            const timeItem = document.createElement("p");
            const c = document.createElement("p");

            const formattedHour = hour.toString().padStart(2, '0') + ":00 ";
            timeItem.textContent = formattedHour;
            c.textContent = parseFloat(temp[thisDay + hour].toFixed(1)) +"°C";
            createBlockL.appendChild(timeItem);
            createBlockR.appendChild(c);
        }
    });
}

async function get_temp(name){
    const data = await loadTemp(name)
    titl.textContent = "Прогноз погоды: " + data.city;
    days_add(data.temperatures);
    
    if (name === "" && data.city) {
        cityInput.value = data.city;
    }
}

const titl = document.getElementById('titl');
document.getElementById('find_butt').addEventListener('click', async function() {
    if(cityInput.value != ""){
    document.querySelectorAll('.allData').forEach(container => {
        container.remove();
    });
    document.querySelectorAll('H3').forEach(container => {
        container.remove();
    });
    await get_temp(cityInput.value);
    }
  });

(async () => {
    await get_temp("");
})();


