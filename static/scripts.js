// static/script.js - (optional) used if you add a public home page
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("publicWeatherForm");
    const cityInput = document.getElementById("publicCity");
    const resultDiv = document.getElementById("publicWeatherResult");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const city = cityInput.value.trim();
        if (!city) return;
        resultDiv.innerHTML = "Fetching...";
        try {
            const apiKey = "YOUR_API_KEY"; // replace if used
            const resp = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`);
            if (!resp.ok) throw new Error("City not found");
            const data = await resp.json();
            resultDiv.innerHTML = `<h3>${data.name}</h3><img src="https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png"><p style="font-size:1.3rem">${data.main.temp} °C</p><p>${data.weather[0].description}</p>`;
        } catch (err) {
            resultDiv.innerHTML = `<p style="color:red">${err.message}</p>`;
        }
    });
});
