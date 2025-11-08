import requests
import json

# WEATHER (Open-Meteo)
weather_url = "https://api.open-meteo.com/v1/forecast"
latitude = 35.6895
longitude = 139.6917

params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": "temperature_2m_max,temperature_2m_min",
    "timezone": "Asia/Tokyo"
}

weather = requests.get(weather_url, params=params)
if weather.status_code == 200:
    with open("weather.json", "w") as f:
        json.dump(weather.json(), f, indent=2)
else:
    print("Weather API Error:", weather.status_code)

# NEWS (GNews)
gnews_api = ""
category = "general"
lang = "en"
country = "us"

gnews_url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang={lang}&country={country}&max=10&apikey={gnews_api}"

gnews = requests.get(gnews_url)
if gnews.status_code == 200:
    gnews_data = gnews.json()
    with open("gnews.json", "w") as f:
        json.dump(gnews_data, f, indent=2)
else:
    print("GNews API Error:", gnews.status_code)

# FOREX (ExchangeRate.host)
ex_api = ""
forex_url = "https://api.exchangerate.host/convert"
params = {
    "access_key": ex_api,
    "from": "EUR",
    "to": "USD",
    "amount": 1
}

forex = requests.get(forex_url, params=params)
if forex.status_code == 200:
    with open("forex.json", "w") as f:
        json.dump(forex.json(), f, indent=2)
else:
    print("Forex API Error:", forex.status_code)

# MERGE ALL JSONS
import json

merged = []
for f in ["weather.json", "gnews.json", "forex.json"]:
    with open(f) as infile:
        data = json.load(infile)
        merged += data if isinstance(data, list) else [data]

with open("merged.json", "w") as outfile:
    json.dump(merged, outfile, indent=2)

print("merged.json created")

# READ MERGED.JSON AND PRINT SUMMARY
import json

with open("merged.json") as f:
    data = json.load(f)

print("\n============================")
print("WEATHER SUMMARY")
print("============================")

weather = data[0]  # first block is from Open Meteo
daily = weather["daily"]
for date, tmax, tmin in zip(daily["time"], daily["temperature_2m_max"], daily["temperature_2m_min"]):
    print(f"{date}: Max {tmax}°C / Min {tmin}°C")

print("\n============================")
print("NEWS HEADLINES (Top 5)")
print("============================")

news = data[1]["articles"]
for article in news[:5]:
    print(f"- {article['title']}")

print("\n============================")
print("FOREX RATE")
print("============================")

forex = data[2]
rate = forex["result"]
print(f"1 EUR = {rate} USD")
