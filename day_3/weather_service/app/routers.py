from fastapi import APIRouter

from app.schemas import ConvertResponse, HealthResponse, WeatherResponse
from app.services import fetch_weather_from_api
from app.utils import celsius_to_fahrenheit, get_weather_description

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Проверка работоспособности сервиса."""
    return HealthResponse(status="ok")


@router.get("/convert", response_model=ConvertResponse)
def convert_temperature(celsius: float):
    """Конвертация Celsius → Fahrenheit."""
    return ConvertResponse(
        celsius=celsius,
        fahrenheit=celsius_to_fahrenheit(celsius),
    )


@router.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    """Получение погоды для города."""
    data = await fetch_weather_from_api(city)
    temp = data["current"]["temp_c"]
    return WeatherResponse(
        city=city,
        temperature=temp,
        description=get_weather_description(temp),
        feels_like=data["current"]["feelslike_c"],
    )
