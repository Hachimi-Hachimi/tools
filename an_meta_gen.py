from pathlib import Path
import json
from sys import argv
import sqlite3
from meta_db_lib import MetaDb

def main():
    (windows_meta, android_meta, ld_assets_dir) = argv[1:]

    windows_meta = MetaDb(sqlite3.connect(windows_meta))
    android_meta = MetaDb(sqlite3.connect(android_meta))
    ld_assets_dir = Path(ld_assets_dir)
    an_dir = ld_assets_dir / "an_texture_sets"

    for child in Path(an_dir).iterdir():
        if child.is_dir() and child.name.startswith("as_uMeshParam_fl_"):
            base_name = child.name[len("as_uMeshParam_fl_"):]
            (asset_name, windows_hash) = windows_meta.find_flash_prefab(base_name) or (None, None)
            (_, android_hash) = android_meta.find_flash_prefab(base_name) or (None, None)

            print(base_name)

            if not windows_hash and not android_hash:
                print("[Warn] Asset not found, skipping")
                continue

            meta = {}

            meta_path = ld_assets_dir / (asset_name + ".json")
            if meta_path.is_file():
                with open(meta_path) as f:
                    meta = json.load(f)

            if windows_hash:
                meta["windows"] = {'bundle_name': windows_hash}
            else:
                print("[Warn] Asset not found for Windows")

            if android_hash:
                meta["android"] = {'bundle_name': android_hash}
            else:
                print("[Warn] Asset not found for Android")

            meta_path.parent.mkdir(parents=True, exist_ok=True)
            with open(meta_path, "w", encoding="utf-8", newline='\n') as f:
                json.dump(meta, f, ensure_ascii=False, indent=4)

main()