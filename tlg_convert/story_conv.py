from pathlib import Path
import json
from sys import argv

def main():
    story_dir = Path(argv[1])

    for child in story_dir.rglob("*.json"):
        print(child)

        with open(child) as f:
            tlg_dict = json.load(f)

        hc_dict = {}

        hc_dict['no_wrap'] = True

        if v := tlg_dict.get("Title"):
            if v != '0':
                hc_dict['title'] = v

        if tlg_tbl := tlg_dict.get("TextBlockList"):
            text_block_list = []

            for tlg_block in tlg_tbl[1:]:
                if tlg_block is None:
                    text_block_list.append({})
                    continue

                hc_block = {}
                if v := tlg_block.get("Name"):
                    hc_block['name'] = v

                if v := tlg_block.get("Text"):
                    hc_block['text'] = v

                if v := tlg_block.get("ChoiceDataList"):
                    hc_block['choice_data_list'] = v

                if v := tlg_block.get("ColorTextInfoList"):
                    hc_block['color_text_info_list'] = v

                text_block_list.append(hc_block)

            hc_dict['text_block_list'] = text_block_list

        with open(child, "w", encoding="utf-8", newline='\n') as f:
            json.dump(hc_dict, f, ensure_ascii=False, indent=4)

main()