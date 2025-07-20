from fastapi import FastAPI
from .routers import resistance, cardio

app = FastAPI(title="Health Hub API")

app.include_router(resistance.router)
app.include_router(cardio.router)
