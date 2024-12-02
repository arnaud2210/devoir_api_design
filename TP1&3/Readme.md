Voici un exemple de fichier `README.md` pour le projet CRUD FastAPI :

---

# FastAPI CRUD pour la gestion des catégories

Ce projet est une API CRUD construite avec **FastAPI** et **SQLAlchemy**. L'API permet de créer, lire, mettre à jour et supprimer des catégories, et utilise une base de données SQLite par défaut (modifiable).

## Prérequis

Assurez-vous d'avoir Python installé sur votre machine. Pour vérifier, exécutez :

```bash
python --version
```

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/votre_utilisateur/votre_projet.git
   cd votre_projet
   ```

2. Créez un environnement virtuel (recommandé) :

   ```bash
   python -m venv env
   source env/bin/activate  # Pour Linux et macOS
   env\Scripts\activate     # Pour Windows
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

   > **Remarque** : Si vous n'avez pas encore de fichier `requirements.txt`, utilisez :
   >
   > ```bash
   > pip install fastapi uvicorn sqlalchemy
   > ```

## Configuration de la base de données

Par défaut, ce projet utilise SQLite comme base de données. Vous pouvez modifier `SQLALCHEMY_DATABASE_URL` dans `database.py` pour utiliser un autre SGBD, comme PostgreSQL ou MySQL.

### Exemple de configuration pour PostgreSQL

```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

## Structure du projet

- `main.py` : Fichier principal contenant les points de terminaison de l'API.
- `models.py` : Définit le modèle de données avec SQLAlchemy.
- `schemas.py` : Définit les schémas Pydantic pour la validation des données.
- `database.py` : Configuration de la base de données et initialisation.

## Lancer l'API

Pour lancer l'API en local, utilisez la commande suivante :

```bash
uvicorn main:app --reload
```

- L'API sera disponible à : [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Vous pouvez accéder à la documentation interactive de l'API (générée automatiquement par FastAPI) à : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Points de terminaison

### Créer une catégorie

- **POST** `/categories/`
- **Body** : `{ "name": "string", "description": "string" }`

### Lire toutes les catégories

- **GET** `/categories/`
- **Query params** : `skip` (par défaut `0`), `limit` (par défaut `10`)

### Lire une catégorie par ID

- **GET** `/categories/{category_id}`

### Mettre à jour une catégorie

- **PUT** `/categories/{category_id}`
- **Body** : `{ "name": "string", "description": "string" }`

### Supprimer une catégorie

- **DELETE** `/categories/{category_id}`

## Exemple de requêtes avec `curl`

### Créer une catégorie

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Catégorie Exemple",
  "description": "Description de la catégorie"
}'
```

### Lire toutes les catégories

```bash
curl -X 'GET' 'http://127.0.0.1:8000/categories/' -H 'accept: application/json'
```

## Remarques

- Ce projet utilise une base de données SQLite pour la simplicité, mais il peut être facilement configuré pour d'autres bases de données.
- FastAPI génère automatiquement la documentation de l'API à l'adresse `/docs`.

