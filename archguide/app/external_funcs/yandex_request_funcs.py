import requests

from config import get_yandex_geocode_apikey


def get_address(lat: float, lon: float) -> str:
    URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={get_yandex_geocode_apikey()}&lang=ru_RU&sco=latlong&geocode={lat},{lon}&format=json"
    result: dict = requests.get(URL).json()
    return result["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
