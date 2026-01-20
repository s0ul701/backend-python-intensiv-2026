from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

# ===== /health =====

async def test_health_returns_ok(async_client):
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ===== /convert =====

async def test_convert_positive_temperature(async_client):
    response = await async_client.get("/convert", params={"celsius": 100})

    assert response.status_code == 200
    assert response.json() == {
        "celsius": 100.0,
        "fahrenheit": 212.0,
    }


async def test_convert_negative_temperature(async_client):
    response = await async_client.get("/convert", params={"celsius": -40})

    assert response.status_code == 200
    assert response.json()["fahrenheit"] == -40.0


async def test_convert_missing_param_returns_422(async_client):
    """Отсутствует обязательный параметр."""
    response = await async_client.get("/convert")

    assert response.status_code == 422


# ===== /weather/{city} =====

async def test_weather_success(async_client, mock_weather_data):
    """Успешное получение погоды."""
    with patch(
        "app.routers.fetch_weather_from_api",
        new_callable=AsyncMock,
        return_value=mock_weather_data,
    ):
        response = await async_client.get("/weather/London")

        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "London"
        assert data["temperature"] == 22.5
        assert data["feels_like"] == 21.0
        assert data["description"] == "warm"


async def test_weather_cold_city(async_client):
    """Погода для холодного города."""
    cold_weather = {"current": {"temp_c": -5.0, "feelslike_c": -10.0}}

    with patch(
        "app.routers.fetch_weather_from_api",
        new_callable=AsyncMock,
        return_value=cold_weather,
    ):
        response = await async_client.get("/weather/Yakutsk")

        assert response.status_code == 200
        assert response.json()["description"] == "freezing"


async def test_weather_city_not_found(async_client):
    """Город не найден."""
    with patch(
        "app.routers.fetch_weather_from_api",
        new_callable=AsyncMock,
        side_effect=HTTPException(status_code=404, detail="City 'xyz' not found"),
    ):
        response = await async_client.get("/weather/xyz")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


# ===== /weather/{city} с monkeypatch =====

async def test_weather_success_monkeypatch(async_client, mock_weather_data, monkeypatch):
    """Успешное получение погоды с использованием monkeypatch."""

    async def mock_fetch(city: str) -> dict:
        return mock_weather_data

    monkeypatch.setattr("app.routers.fetch_weather_from_api", mock_fetch)

    response = await async_client.get("/weather/Paris")

    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Paris"
    assert data["temperature"] == 22.5
    assert data["description"] == "warm"


async def test_weather_city_not_found_monkeypatch(async_client, monkeypatch):
    """Город не найден с использованием monkeypatch."""

    async def mock_fetch(city: str) -> dict:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    monkeypatch.setattr("app.routers.fetch_weather_from_api", mock_fetch)

    response = await async_client.get("/weather/unknown")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
