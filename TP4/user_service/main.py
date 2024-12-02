from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel

app = FastAPI()

# Clé secrète pour signer les JWT
SECRET_KEY = "votre_secret_jwt_super_secure"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Durée de validité du token

class User(BaseModel):
    id: int
    name: str
    temperature_preference: str  # "cold", "comfort", "hot"

users = [
    {"id": 1, "name": "Alice", "temperature_preference": "comfort"},
    {"id": 2, "name": "Bob", "temperature_preference": "cold"},
]

# Fonction pour créer un token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Middleware pour vérifier les JWT
def authenticate(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré. Veuillez vous reconnecter.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide. Accès refusé.",
        )


# Route pour obtenir un token JWT
@app.post("/client/token")
def login():
    token = create_access_token({"sub": "user"})
    return {"token": token}

@app.get("/users/{user_id}", dependencies=[Depends(authenticate)])
async def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}
