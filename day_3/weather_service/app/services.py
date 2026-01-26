import httpx
from fastapi import HTTPException

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
HTTP_TIMEOUT = 10.0  # секунд


async def fetch_coordinates(city: str) -> tuple[float, float]:
    """Получить координаты города через Nominatim."""
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.get(
            NOMINATIM_URL,
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "WeatherService/1.0"},
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")
        return float(data[0]["lat"]), float(data[0]["lon"])


async def fetch_weather_by_coords(lat: float, lon: float) -> dict:
    """Получить погоду по координатам через Open-Meteo."""
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.get(
            OPEN_METEO_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,apparent_temperature",
            },
        )
        response.raise_for_status()
        return response.json()


async def fetch_weather_from_api(city: str) -> dict:
    """Запрос погоды: геокодинг + погодный API."""
    lat, lon = await fetch_coordinates(city)
    weather = await fetch_weather_by_coords(lat, lon)

    return {
        "current": {
            "temp_c": weather["current"]["temperature_2m"],
            "feelslike_c": weather["current"]["apparent_temperature"],
        }
    }
