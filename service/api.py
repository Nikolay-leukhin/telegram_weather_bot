import requests
from dataclasses import dataclass
from typing import Dict, Any, List


# Этот файл содержит реализацию клиента для взаимодействия с API погоды
# и модель данных для представления информации о погоде.


class Api:
    url = "http://127.0.0.1:5000"

    def get_weather(self, days, points):
        response = requests.post(self.url + '/weather', json={'days': days, 'points': points})
        if response.status_code == 200:
            return [WeatherModel(**item) for item in response.json()]
        else:
            raise Exception("Ой беда беда...")


@dataclass
class WeatherModel:
    city: str
    day: int
    humidity: int
    lat: float
    lon: float
    precipitation_probability: int
    temperature: float
    wind_speed: float

    @staticmethod
    def format_weather_data(weather_data_list) -> str:
        result = []
        for weather in weather_data_list:
            result.append(
                f"Город: {weather.city}\n"
                f"День: {weather.day}\n"
                f"Температура: {weather.temperature}°C\n"
                f"Влажность: {weather.humidity}%\n"
                f"Скорость ветра: {weather.wind_speed} м/с\n"
                f"Вероятность осадков: {weather.precipitation_probability}%\n"
                f"Широта: {weather.lat}\n"
                f"Долгота: {weather.lon}\n"
                "-------------------------"
            )
        return "\n".join(result)

