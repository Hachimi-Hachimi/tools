import UnityPy
from UnityPy.classes import Sprite
from PIL import Image, ImageDraw
from common import *
from pathlib import Path

def main():
    old_atlas_path = input("Enter atlas path: ").strip()
    old_bundle_path = input("Enter old bundle path: ").strip()
    new_bundle_path = input("Enter new bundle path: ").strip()

    old_env = UnityPy.load(old_bundle_path)
    new_env = UnityPy.load(new_bundle_path)

    new_texture = find_first_texture_2d(new_env)
    if not new_texture:
        print("[Error] Texture not found in new bundle (invalid or failed to load asset bundle)")
        return
    new_texture_im = new_texture.image
    
    old_sprites = read_sprites_to_dict(old_env)
    new_sprites = read_sprites_to_dict(new_env)

    if not old_sprites:
        print("[Error] No sprites found in old bundle")
        return

    if not new_sprites:
        print("[Error] No sprites found in new bundle")
        return
    
    old_atlas_im = Image.open(old_atlas_path)
    
    width = new_texture.m_Width
    height = new_texture.m_Height
    im = Image.new("RGBA", (width, height), None)
    for (name, new_data) in new_sprites.items():
        new_rect = new_data.m_Rect
        new_rect_coords = rect_to_coords(new_rect, height)

        # Prefer to use sprites from the old translated atlas
        source_im = None
        source_rect_coords = None
        old_data = old_sprites.get(name)
        if old_data:
            old_rect = old_data.m_Rect
            if old_rect.width == new_rect.width and old_rect.height == new_rect.height:
                source_rect_coords = rect_to_coords(old_rect, height)
                source_im = old_atlas_im
            else:
                print("[Warn] {} has changed its size, using new sprite instead".format(name))
        
        if not source_im or not source_rect_coords:
            print("{}: new".format(name))
            source_im = new_texture_im
            source_rect_coords = new_rect_coords
        else:
            print("{}: old".format(name))

        # Crop the source image to the sprite
        sprite_im = source_im.crop(source_rect_coords)

        # Paste sprite on new atlas
        im.paste(sprite_im, (new_rect_coords[0], new_rect_coords[1]))

    last_dot_pos = old_atlas_path.rfind(".")
    out_path = old_atlas_path[:last_dot_pos] + "_new.png"
    im.save(out_path, "PNG", compress_level=9)


main()