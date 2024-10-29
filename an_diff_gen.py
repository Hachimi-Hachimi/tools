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
    (meta_path, an_dir) = argv[1:]
    an_dir = Path(an_dir)

    meta = MetaDb(sqlite3.connect(meta_path))
    ignore_list = load_ignore_list(an_dir)

    for child in an_dir.iterdir():
        if child.is_dir() and child.name.startswith("as_uMeshParam_fl_"):
            png_files = list(child.glob("*.png"))
            if len(png_files) == 0 or all(path.name.endswith(".diff.png") for path in png_files):
                continue

            base_name = child.name[len("as_uMeshParam_fl_"):]
            print(base_name)

            # Prefer source resource because if flash prefab + src rsrc exists then only src rsrc has the texture
            (asset_name, asset_hash) = (meta.find_flash_source_resources(base_name) or meta.find_flash_prefab(base_name)) or (None, None)

            if not asset_hash:
                print("[Warn] Asset not found, skipping")
                continue

            print("Bundle: " + asset_name)

            bundle_url = meta.get_asset_bundle_url(asset_hash)
            bundle_res = requests.get(bundle_url)
            status = bundle_res.status_code
            if status == 200:
                env = UnityPy.load(bundle_res.content)
                for texture_path in png_files:
                    if texture_path.name.endswith(".diff.png") or "/".join(texture_path.parts[-2:]) in ignore_list:
                        continue

                    if texture_path.is_file():
                        rep_img = Image.open(texture_path)
                        texture_name = texture_path.stem + "_C"

                        texture = find_texture_2d_by_name(env, texture_name)
                        if not texture:
                            print("[Error] Failed to find texture: " + texture_name)
                            continue

                        diff_img = png_diff(texture.image, rep_img)
                        diff_path = texture_path.with_suffix(".diff.png")
                        diff_img.save(diff_path, "PNG", compress_level=9)
            else:
                print("Got status code {}".format(status))

main()