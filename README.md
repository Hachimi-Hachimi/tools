# Translation tools
Some miscellaneous tools to help with the translation process.

Install dependencies in `requirements.txt` before running these tools.

- `mattegen.py`: Generate a matte from an AtlasReference texture asset bundle.
- `update_atlas.py`: Update a (translated) atlas texture to match a newer atlas by creating a new atlas texture with the sprites remapped to their new location.
- `png_diff.py`: Generate a PNG diff based on two images. Takes 3 command line arguments: `(old_path, new_path, out_path)`
- `apply_png_diff.py`: Applies a PNG diff. Takes 3 command line arguments: `(orig_path, diff_path, out_path)`