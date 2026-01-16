import pytest

from app.utils import celsius_to_fahrenheit, get_weather_description


def test_celsius_to_fahrenheit_freezing_point():
    """Точка замерзания воды."""
    assert celsius_to_fahrenheit(0) == 32.0


def test_celsius_to_fahrenheit_boiling_point():
    """Точка кипения воды."""
    assert celsius_to_fahrenheit(100) == 212.0


def test_celsius_to_fahrenheit_negative_forty():
    """При -40 шкалы совпадают."""
    assert celsius_to_fahrenheit(-40) == -40.0


def test_celsius_to_fahrenheit_room_temperature():
    """Комнатная температура."""
    assert celsius_to_fahrenheit(20) == 68.0


@pytest.mark.parametrize(
    "temp,expected",
    [
        (-15, "freezing"),
        (-1, "freezing"),
        (0, "cold"),
        (5, "cold"),
        (10, "mild"),
        (15, "mild"),
        (20, "warm"),
        (25, "warm"),
        (30, "hot"),
        (40, "hot"),
    ],
)
def test_weather_description_temperature_ranges(temp, expected):
    """Проверка всех температурных диапазонов."""
    assert get_weather_description(temp) == expected
