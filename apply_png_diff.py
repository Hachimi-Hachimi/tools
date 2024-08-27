from PIL import Image
from sys import argv

def main():
    (orig_path, diff_path, out_path) = argv[1:]
    orig_img = Image.open(orig_path)
    diff_img = Image.open(diff_path)
    width = orig_img.width
    height = orig_img.height
    if width != diff_img.width or height != diff_img.height:
        print("[Error] Image size mismatch")

    orig_pixels = orig_img.load()
    diff_pixels = diff_img.load()

    out_img = Image.new("RGBA", (width, height), None)
    out_pixels = out_img.load()
    for x in range(width):
        for y in range(height):
            orig_pixel = orig_pixels[x,y]
            diff_pixel = diff_pixels[x,y]
            if diff_pixel[3] == 0:
                out_pixels[x,y] = orig_pixel
            elif diff_pixel != (255, 0, 255, 255):
                out_pixels[x,y] = diff_pixel
            # else leave the pixel as transparent

    out_img.save(out_path, "PNG", compress_level=9)

main()