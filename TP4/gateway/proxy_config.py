import httpx
from fastapi import HTTPException
from datetime import datetime

USER_SERVICE_URL = "http://localhost:8001"
CLOTHING_SERVICE_URL = "http://localhost:8002"
WEATHER_API_BASE_URL = "https://api.meteo-concept.com/api/forecast/daily"
WEATHER_API_KEY = "287d880ad1f291f0baceb2d3f51802efb322313d0c401d97844772854db56f53"

async def fetch_user(user_id: int):
    async with httpx.AsyncClient() as client:
        user_token = await client.post(f"{USER_SERVICE_URL}/client/token")
        print("USER_TOKEN", user_token.json())

        headers = {"Authorization": f"Bearer {user_token.json()['token']}"}
        
        response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        return response.json()


def find_forecast_by_date(forecasts: list, target_date: str):
    """
    Recherche la prévision correspondant à une date donnée (format YYYY-MM-DD).
    Si la date n'est pas trouvée, un message clair est levé.
    """
    matching_forecast = None

    for forecast in forecasts:
        # Extraire la date au format YYYY-MM-DD depuis le champ "datetime"
        forecast_date = forecast["datetime"].split("T")[0]
        print(f"Checking forecast_date: {forecast_date} against target_date: {target_date}")
        if forecast_date == target_date:
            matching_forecast = forecast
            break

    if matching_forecast is None:
        # Afficher toutes les dates disponibles pour comprendre l'erreur
        available_dates = [f["datetime"].split("T")[0] for f in forecasts]
        raise HTTPException(
            status_code=404,
            detail=f"Weather forecast not available for the requested date. "
                   f"Available dates are: {available_dates}"
        )

    return matching_forecast

async def fetch_weather(location: str, target_date: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            WEATHER_API_BASE_URL,
            params={"token": WEATHER_API_KEY, "name": location}
        )
        
        # Vérifier si la requête a réussi
        if response.status_code != 200:
            print("-------------------- FORECAST ------------------------")
            print(response)
            raise HTTPException(status_code=500, detail="Weather API error")

        # Récupérer les données de la météo
        weather_data = response.json()
        
        # Vérifier si la ville demandée existe dans la réponse
        city_name = weather_data.get('city', {}).get('name')
        if city_name != location:
            raise HTTPException(status_code=404, detail="City not found in weather data")
        
        # Filtrer les prévisions en fonction de la date
        forecast = find_forecast_by_date(weather_data["forecast"], target_date)
        return forecast

async def fetch_clothing(temperature_condition: str):
    async with httpx.AsyncClient() as client:
        clothing_token = await client.post(f"{CLOTHING_SERVICE_URL}/client/token")
        print("CLOTHING_TOKEN", clothing_token.json())

        headers = {"Authorization": f"Bearer {clothing_token.json()['token']}"}

        response = await client.get(f"{CLOTHING_SERVICE_URL}/clothing/{temperature_condition}", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Clothing service error")
        return response.json()

def classify_temperature(temperature: float) -> str:
    if temperature < 10:
        return "cold"
    elif 10 <= temperature <= 20:
        return "comfort"
    else:
        return "hot"
