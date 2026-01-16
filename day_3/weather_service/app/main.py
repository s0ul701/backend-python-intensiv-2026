from fastapi import FastAPI

from app.routers import router

app = FastAPI(title="Weather Service")

app.include_router(router)
