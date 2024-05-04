document.querySelector('form').addEventListener('submit', e => {
    e.preventDefault();
    const input = document.querySelector('input');
    getData(input.value.trim());
});

getData('London');
async function getData(city) {

    const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=78c49d0da7041c7c2d9e2de8d0db7caa`);
    const data = await res.json();

    if (res.status !== 200) {
        alert(data.message);
    } else {
        createWeather(data);
    }
}

function createWeather(data) {
    document.querySelector('.weather').innerHTML = `
    <div class="left">
        <b class="city">${data.name}</b>
        <span>Humidity: <b>${data.main.humidity}%</b></span>
        <span>Wind: <b>${Math.round(data.wind.speed)} m/s</b></span>
    </div>
    <div class="right">
        <img src="https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png">
        <span class="temp">${Math.round(data.main.temp - 273)}℃</span>
    </div>`;
}