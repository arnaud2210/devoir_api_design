from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
import jwt
from datetime import datetime, timedelta


import secrets
API_TOKEN = secrets.token_hex(16)
print(f"Votre token d'accès : {API_TOKEN}")

# Clé secrète pour signer les JWT
SECRET_KEY = "votre_secret_jwt_super_secure"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Durée de validité du token

# Créez les tables de la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dépendance pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost:5500",  # Remplacez par l'URL de votre front-end
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.post("/token")
def login():
    token = create_access_token({"sub": "user"})
    return {"token": token}

# Créer une catégorie
@app.post("/categories/", response_model=schemas.Category, dependencies=[Depends(authenticate)])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(name=category.name, description=category.description, author=category.author)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Lire toutes les catégories
@app.get("/categories/", response_model=list[schemas.Category], dependencies=[Depends(authenticate)])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

# Lire une catégorie par ID
@app.get("/categories/{category_id}", response_model=schemas.Category, dependencies=[Depends(authenticate)])
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Mettre à jour une catégorie
@app.put("/categories/{category_id}", response_model=schemas.Category, dependencies=[Depends(authenticate)])
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db_category.description = category.description
    db_category.author=category.author
    db.commit()
    db.refresh(db_category)
    return db_category

# Supprimer une catégorie
@app.delete("/categories/{category_id}", response_model=schemas.Category, dependencies=[Depends(authenticate)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category
