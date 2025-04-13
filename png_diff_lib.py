from PIL import Image
import os

def rgb_to_lab(r, g, b):
    # Convert RGB (0-255) to XYZ
    r = r / 255
    g = g / 255
    b = b / 255

    r = ((r + 0.055) / 1.055) ** 2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / 1.055) ** 2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / 1.055) ** 2.4 if b > 0.04045 else b / 12.92

    r *= 100
    g *= 100
    b *= 100

    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    # Convert XYZ to L*a*b*
    x /= 95.047
    y /= 100.000
    z /= 108.883

    x = x ** (1/3) if x > 0.008856 else (7.787 * x) + (16/116)
    y = y ** (1/3) if y > 0.008856 else (7.787 * y) + (16/116)
    z = z ** (1/3) if z > 0.008856 else (7.787 * z) + (16/116)

    L = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)

    return L, a, b

def rgba_difference(color1, color2, alpha_weight=1.0):
    # Extract RGBA
    r1, g1, b1, alpha1 = color1
    r2, g2, b2, alpha2 = color2

    # Convert RGB to L*a*b* for CIE76 Delta-E
    L1, a1, b1 = rgb_to_lab(r1, g1, b1)
    L2, a2, b2 = rgb_to_lab(r2, g2, b2)

    # Calculate Delta-E (CIE76) for color
    delta_L = L1 - L2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_e = math.sqrt(delta_L**2 + delta_a**2 + delta_b**2)

    # Calculate normalized alpha difference (0-255 -> 0-1 scale)
    delta_alpha = abs(alpha1 - alpha2) / 255

    # Combine color and alpha differences
    # Alpha weight allows tuning the importance of transparency vs. color
    total_difference = math.sqrt(delta_e**2 + (alpha_weight * delta_alpha * 100)**2)

    return total_difference

def is_pixel_similar(old_pixel, new_pixel):
    if os.environ.get('PNG_DIFF_FUZZY'):
        return rgba_difference(old_pixel, new_pixel, 4.0) < 8.0
    else:
        return old_pixel == new_pixel

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
            if not is_pixel_similar(old_pixel, new_pixel):
                if new_pixel[3] == 0 and old_pixel[3] != 0:
                    new_pixel = (255, 0, 255, 255)
                elif new_pixel == (255, 0, 255, 255):
                    new_pixel = (255, 0, 255, 254)
                out_pixels[x,y] = new_pixel
    return out_img