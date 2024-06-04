from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.api import recommendations, status

from utils.logger import logger


app = FastAPI()

app.include_router(recommendations.router, prefix="/recommendations")
app.include_router(status.router, prefix="/status")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down FastAPI application...")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
