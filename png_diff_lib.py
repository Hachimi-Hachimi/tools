from PIL import Image

def png_diff(old_img, new_img):
    width = old_img.width
    height = old_img.height
    if width != new_img.width or height != new_img.height:
        print("[Error] Image size mismatch")
        return None

    old_pixels = old_img.load()
    new_pixels = new_img.load()

    out_img = Image.new("RGBA", (width, height), None)
    out_pixels = out_img.load()
    for x in range(width):
        for y in range(height):
            old_pixel = old_pixels[x,y]
            new_pixel = new_pixels[x,y]
            if old_pixel != new_pixel:
                if new_pixel[3] == 0 and old_pixel[3] != 0:
                    new_pixel = (255, 0, 255, 255)
                elif new_pixel == (255, 0, 255, 255):
                    new_pixel = (255, 0, 255, 254)
                out_pixels[x,y] = new_pixel
    return out_img