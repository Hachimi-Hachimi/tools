import UnityPy
from UnityPy.classes import Texture2D, Sprite
from UnityPy.math import Rectangle

def find_first_texture_2d(env: UnityPy.Environment) -> Texture2D:
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            return obj.read()

def read_sprites_to_dict(env: UnityPy.Environment) -> dict[str, Sprite]:
    d = {}
    for obj in env.objects:
        if obj.type.name == "Sprite":
            data: Sprite = obj.read()
            d[data.m_Name] = data
    return d

def rect_to_coords(rect: Rectangle, max_y: int):
    x0 = rect.x
    y0 = max_y - rect.y - rect.height
    x1 = rect.x + rect.width
    y1 = max_y - rect.y
    return (int(x0), int(y0), int(x1), int(y1))