import httpx
from fastapi import HTTPException


async def fetch_weather_from_api(city: str) -> dict:
    """Запрос к внешнему API погоды."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.weatherapi.com/v1/current.json",
            params={"key": "SECRET_KEY", "q": city},
        )
        if response.status_code == 400:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")
        response.raise_for_status()
        return response.json()
