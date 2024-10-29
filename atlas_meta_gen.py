from pathlib import Path
import json
from sys import argv
import sqlite3
from meta_db_lib import MetaDb

def main():
    (windows_meta, android_meta, atlas_dir) = argv[1:]

    windows_meta = MetaDb(sqlite3.connect(windows_meta))
    android_meta = MetaDb(sqlite3.connect(android_meta))

    for child in Path(atlas_dir).iterdir():
        if child.is_dir():
            bundle_name = "atlas/{0}/{0}".format(child.name)
            windows_hash = windows_meta.get_asset_hash(bundle_name)
            android_hash = android_meta.get_asset_hash(bundle_name)

            print(bundle_name)

            if not windows_hash and not android_hash:
                print("[Warn] Asset not found, skipping")
                continue

            meta = {}

            if windows_hash:
                meta["windows"] = {'bundle_name': windows_hash}
            else:
                print("[Warn] Asset not found for Windows")

            if android_hash:
                meta["android"] = {'bundle_name': android_hash}
            else:
                print("[Warn] Asset not found for Android")

            with open(child / (child.name + ".json"), "w", encoding="utf-8", newline='\n') as f:
                json.dump(meta, f, ensure_ascii=False, indent=4)

main()