import UnityPy
from UnityPy.classes import Sprite
from PIL import Image, ImageDraw
from unitypy_utils import find_first_texture_2d, rect_to_coords

def main():
    bundle_path = input("Enter bundle path: ").strip()
    env = UnityPy.load(bundle_path)

    texture = find_first_texture_2d(env)
    if not texture:
        print("[Error] Texture not found (invalid or failed to load asset bundle)")
        return
    
    width = texture.m_Width
    height = texture.m_Height
    im = Image.new("RGBA", (width, height), None)
    im_draw = ImageDraw.Draw(im, "RGBA")
    for obj in env.objects:
        if obj.type.name == "Sprite":
            data: Sprite = obj.read()
            coords = rect_to_coords(data.m_Rect, height)
            im_draw.rectangle(coords, "#ff00ff")

    out_path = bundle_path + "_matte.png"
    im.save(out_path, "PNG", compress_level=9)


main()