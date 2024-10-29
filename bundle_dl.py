from sys import argv
import sqlite3
from pathlib import Path
import requests
from meta_db_lib import MetaDb

def main():
    (output_dir, meta_path, bundle_name) = argv[1:]

    meta = MetaDb(sqlite3.connect(meta_path))

    asset_hash = meta.get_asset_hash(bundle_name)
    print(asset_hash)
    if asset_hash == None:
        return

    path = output_dir / Path(bundle_name)
    path = path.with_name(path.name + "_" + asset_hash)
    path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(meta.get_asset_bundle_url(asset_hash))
    status = response.status_code

    if status == 200:
        with open(path, "wb") as file:
            file.write(response.content)
        print("Done")
    else:
        print("Got status code {}".format(status))

main()