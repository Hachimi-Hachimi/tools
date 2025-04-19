import json
from sys import argv

def main():
    (static_dict_path, localize_dump_path, out_path) = argv[1:]

    with open(static_dict_path, 'r', encoding='utf8') as f:
        static_dict = json.load(f)

    with open(localize_dump_path, 'r', encoding='utf8') as f:
        localize_dump = json.load(f)

    def swap(obj):
        return {value: key for key, value in obj.items()}

    localize_ids = swap(localize_dump)

    localize_dict = {}
    for orig_content, tl_content in static_dict.items():
        id_ = localize_ids.get(orig_content)
        if not id_:
            print(f"WARNING: Couldn't find ID for '{orig_content}'")
            continue
        localize_dict[id_] = tl_content

    with open(out_path, 'w', encoding='utf8', newline='\n') as f:
        json.dump(localize_dict, f, ensure_ascii=False, indent=4)

main()