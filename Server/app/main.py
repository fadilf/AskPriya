from contextlib import asynccontextmanager
from app.priya import Priya
from fastapi import FastAPI
from dotenv import load_dotenv
from os import environ


load_dotenv()
ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["priya"] = Priya()
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/priya")
async def predict(api_key: str, q: str):
    if api_key == environ["API_KEY"]:
        result = ml_models["priya"].query(q)
        return result
    else:
        return {}