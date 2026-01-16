def celsius_to_fahrenheit(celsius: float) -> float:
    """Конвертация температуры."""
    return round(celsius * 9 / 5 + 32, 1)


def get_weather_description(temp: float) -> str:
    """Текстовое описание погоды по температуре."""
    if temp < 0:
        return "freezing"
    elif temp < 10:
        return "cold"
    elif temp < 20:
        return "mild"
    elif temp < 30:
        return "warm"
    else:
        return "hot"
