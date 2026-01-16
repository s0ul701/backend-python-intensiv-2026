from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    feels_like: float


class ConvertResponse(BaseModel):
    celsius: float
    fahrenheit: float


class HealthResponse(BaseModel):
    status: str
