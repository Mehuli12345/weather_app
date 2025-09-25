# weather_api.py
import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY", "sk-proj-P9ut")  

BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_weather(city: str):
    if not city:
        return None
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None

def get_5day_forecast(city: str):
    if not city:
        return None
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None

def get_weather_by_coords(lat: float, lon: float):
    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None
