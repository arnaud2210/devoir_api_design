from fastapi import FastAPI, HTTPException
from datetime import datetime
from . proxy_config import fetch_user, fetch_weather, fetch_clothing, classify_temperature

app = FastAPI()


@app.get("/recommendation")
async def get_recommendation(location: str, date: str, user_id: int):
    # Validation de la date
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Appels aux services via proxy_config
    user = await fetch_user(user_id)
    weather_data = await fetch_weather(location, date)
    print(weather_data)
    # Recherche de la météo pour la date spécifiée
    #weather_data = find_weather_data_by_date(weather_data["weather_data"], date)
    temperature_condition = classify_temperature(weather_data["tmin"])

    # Appel au service des vêtements
    clothing = await fetch_clothing(temperature_condition)

    # Construire la réponse finale
    return {
        "user": user,
        "weather": {
            "date": date,
            "temperature_min": weather_data["tmin"],
            "temperature_max": weather_data["tmax"],
            "condition": weather_data["weather"],
            "rain_probability": weather_data["probarain"],
        },
        "clothing_recommendation": clothing
    }