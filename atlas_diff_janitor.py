from PIL import Image
from sys import argv
from unitypy_utils import *
import UnityPy

def main():
    (bundle_path, in_path, out_path) = argv[1:]

    bundle_env = UnityPy.load(bundle_path)
    sprites = read_sprites_to_dict(bundle_env)
    if not sprites:
        print("[Error] No sprites found in bundle")
        return

    img = Image.open(in_path)
    pixels = img.load()
    width = img.width
    height = img.height

    out_img = Image.new("RGBA", (width, height), None)
    out_pixels = out_img.load()

    for (name, data) in sprites.items():
        rect = data.m_Rect
        rect_coords = rect_to_coords(rect, height)
        (x0, y0, x1, y1) = rect_coords

        got_opaque = False
        for x in range(x0, x1):
            for y in range(y0, y1):
                p = pixels[x,y]
                if p[3] == 255:
                    got_opaque = True
                    break

        if got_opaque:
            sprite_img = img.crop(rect_coords)
            out_img.paste(sprite_img, (x0, y0))

    out_img.save(out_path, "PNG", compress_level=9)

main()