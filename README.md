# Translation tools
Some miscellaneous tools to help with the translation process. These are all command line tools.

Install dependencies in `requirements.txt` before running these tools.

- `an_diff_gen.py`: Try to generate PNG diffs from all replacement textures in the `an_texture_sets` folder. Since some of these textures cannot be directly mapped back to their uianimation bundle, it will skip files on those occasions. Arguments: `(meta_path, an_texture_sets_dir)`
- `an_meta_gen.py`: Try to generate uianimation meta files for each set in `an_texture_sets`. Since some of these textures cannot be directly mapped back to their uianimation bundle, it will skip files on those occasions. Arguments: `(windows_meta, android_meta, ld_assets_dir)`
- `apply_png_diff.py`: Applies a PNG diff. Arguments: `(orig_path, diff_path, out_path)`
- `atlas_diff_gen.py`: Generate PNG diffs for all replacement textures in the `atlas` folder. Arguments: `(meta_path, atlas_dir)`
- `atlas_diff_janitor.py`: Try to clean up an atlas PNG diff with garbage pixels, which includes sprite areas with no opaque pixels and areas that are not within any sprite boundaries. Arguments: `(bundle_path, in_path, out_path)`
- `atlas_janitor.py`: Clean up an atlas texture by cropping off areas that are not within any sprite boundaries. Arguments: `(bundle_path, in_path, out_path)`
- `atlas_meta_gen.py`: Generate meta files for atlas replacements. Arguments: `(windows_meta, android_meta, atlas_dir)`
- `atlas_update.py`: Update a (translated) atlas texture to match a newer atlas by creating a new atlas texture with the sprites remapped to their new location.
- `bundle_dl.py`: Download an asset bundle. Resulting file is saved at `{output_dir}/{bundle_name}_{bundle_hash}`. Arguments: `(output_dir, meta_path, bundle_name)`
- `mattegen.py`: Generate a matte from an AtlasReference texture asset bundle.
- `png_diff.py`: Generate a PNG diff based on two images. Arguments: `(old_path, new_path, out_path)`
- `uianimation_meta_update.py`: Update existing uianimation meta files. Arguments: `(windows_meta, android_meta, anim_dir)`

Other Python scripts are libraries and do not have any functionality on their own.