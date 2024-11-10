from typing import Annotated

from fastapi import FastAPI, Body, UploadFile, HTTPException

from external_funcs.location_extractor import image_coordinates
from schemas import GeoData
from app.external_funcs.gg_chat_prompt_funcs import do_prompt
from app.external_funcs.yandex_request_funcs import get_address


types_streets = ("улица", "проспект", "аллея", "бульвар", "переулок", "тупик", "вал")

app = FastAPI()

def get_and_check_location(coords: GeoData) -> str|None:
    address_of_coords: str = get_address(coords.lat, coords.lon)
    if any(ext in address_of_coords for ext in types_streets):
        return address_of_coords
    return None

def try_prompt(coords: GeoData) -> tuple[str, str]|None:
    loc: str|None = get_and_check_location(coords)
    if loc:
        return (loc, do_prompt(loc))
    return None


@app.post("/building/image/")
async def get_building_info_by_photo(image_file: UploadFile = None):
    if image_file:
        coords = image_coordinates(image_file.file.read())
        geodata: GeoData = GeoData(lat=coords.lat, lon=coords.lon)
        resp_prompt = try_prompt(geodata)
        if resp_prompt:
            return {"address": resp_prompt[0], "coordinates":{"latitude": geodata.lat, "longitude":geodata.lon}, "description": resp_prompt[1]}
    return HTTPException(
        status_code=404, detail="Местоположение в метаданных фото не найдены"
    )

@app.post("/building/coords/")
async def get_building_info_by_coord(geodata: Annotated[GeoData|None, Body()] = None):
    if geodata:
        if geodata.lat and geodata.lon:
            resp_prompt = try_prompt(geodata)
            if resp_prompt:
                return {"address": resp_prompt[0], "coordinates":{"latitude": geodata.lat, "longitude":geodata.lon}, "description": resp_prompt[1]}
    return HTTPException(
        status_code=404, detail="Координат не найдено"
    )
