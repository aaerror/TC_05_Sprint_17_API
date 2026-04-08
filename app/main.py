from app.database.db_init import init_database

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.routes import auth, model, user
from typing import Annotated, Any, Dict, Optional




@asynccontextmanager
async def lifespan(app: FastAPI):
    # inicializar la DB
    init_database()

    # yield deja que FastAPI continúe con startup normal
    yield

    # Aquí puedes cerrar recursos si fuera necesario
    print("App shutting down")


description = """
---

🚀 Machine Learning API to help digital nomads choose the best city.

## Overview
This API provides tools to manage users and evaluate cities using machine learning models.

## ⚙️ Tech Stack
- FastAPI
- Python
- Machine Learning

## ✨ Features
### User Management
You can:
- Create a user
- Update personal data
- Delete your account
- Retrieve your information

### City Evaluation (Machine Learning)
You can:
- Evaluate cities based on different features (cost of living, internet, quality of life, etc.)
- Get recommendations tailored to your preferenceso

## 👥 Team
- Aguirre Daniela
- Argañin Agustín
- Juán F. Cía
"""

app = FastAPI(
    title="Team 09 - Digital Nomad ML API",
    description=description,
    contact={
        "name": "Team 09",
        "email": "team09@example.com",
        # "url": "https://github.com/team09"
        "url": "https://example.com"
    },
    license_info={
        "name": "Apache License 2.0",
        "identifier": "Apache-2"
    },
    lifespan=lifespan,
    summary="API for user management and ML-based city recommendations",
    terms_of_service="https://example.com",
    version="0.1.0",
)

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(model.router)
router.include_router(user.router)
app.include_router(router)