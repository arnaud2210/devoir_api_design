from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi_auth0 import Auth0, Auth0User
from datetime import datetime
from proxy_config import fetch_user, fetch_weather, fetch_clothing, classify_temperature


# Configuration Auth0
AUTH0_DOMAIN = "dev-jpzjychpmohjc4wr.eu.auth0.com"
AUTH0_CLIENT_ID = "CQZWjmiw25vgWX1ONPsqZG27eEWX6cmD"
AUTH0_CLIENT_SECRET = "omVlGn4vTN-7R0QO4Hdtqc_yqjl5msMro4qnFyD_NLd8lY_R73GVQcOzv-LaBD0e"
AUTH0_API_AUDIENCE = "meteo_service"
AUTH0_ALGORITHM = "RS256"

auth = Auth0(domain=AUTH0_DOMAIN, api_audience=AUTH0_API_AUDIENCE, scopes={'read:recommandations': 'get read recommandation for your clothes with meteo'})

app = FastAPI()

@app.get("/secure", dependencies=[Depends(auth.implicit_scheme)])
def get_secure(user: Auth0User = Security(auth.get_user, scopes=['read:recommandations'])):
    return {"message": f"{user}"}

@app.get("/recommendation", dependencies=[Depends(auth.implicit_scheme)])
async def get_recommendation(location: str, date: str, user_id: int, user: Auth0User = Security(auth.get_user, scopes=['read:recommandations'])):
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