from pathlib import Path
from unitypy_utils import *
import json
from sys import argv
import sqlite3
import requests
import UnityPy
from PIL import Image
from meta_db_lib import MetaDb
from png_diff_lib import png_diff
from utils import load_ignore_list

def main():
    (meta_path, atlas_dir) = argv[1:]
    atlas_dir = Path(atlas_dir)

    meta = MetaDb(sqlite3.connect(meta_path))
    ignore_list = load_ignore_list(atlas_dir)

    for child in atlas_dir.iterdir():
        if child.is_dir():
            texture_path = child / (child.name + ".png")
            if "/".join(texture_path.parts[-2:]) in ignore_list:
                continue

            if texture_path.is_file():
                rep_img = Image.open(texture_path)

                bundle_name = "atlas/{0}/{0}_tex".format(child.name)
                bundle_url = meta.get_asset_bundle_url_from_name(bundle_name)
                print(bundle_name)

                if not bundle_url:
                    print("[Warn] Asset not found, skipping")
                    continue

                bundle_res = requests.get(bundle_url)
                status = bundle_res.status_code
                if status == 200:
                    env = UnityPy.load(bundle_res.content)
                    texture = find_first_texture_2d(env)
                    if not texture:
                        print("[Error] Texture not found (invalid or failed to load asset bundle)")
                        continue

                    diff_img = png_diff(texture.image, rep_img)
                    diff_path = child / (child.name + ".diff.png")
                    diff_img.save(diff_path, "PNG", compress_level=9)
                else:
                    print("Got status code {}".format(status))

main()