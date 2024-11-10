from ..schemas import GeoData
from exif import Image

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(src) -> GeoData|None:
    if src:
        img = Image(src)
    if img.has_exif:
        try:
            coords = (decimal_coords(img.gps_latitude,
                                     img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                                     img.gps_longitude_ref))
            return GeoData(lat=coords[0], lon=coords[1])
        except AttributeError:
            return None
    else:
        return None