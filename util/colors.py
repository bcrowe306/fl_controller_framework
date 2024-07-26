import math

def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v

def ColorToRGB(color: int) -> tuple[int, int, int]:
    """Converts from int value to an RGB tuple"""
    return color >> 16, (color & 0x00FF00) >> 8, color & 0x0000FF

def BGRIntToRGB(color: int) -> tuple[int, int, int]:
    """
    Converts a BGR integer color value to an RGB tuple.

    Args:
        color (int): The BGR color value to convert.

    Returns:
        tuple[int, int, int]: The RGB color tuple.

    """
    blue: int = color >> 16
    green: int = (color & 0x00FF00) >> 8
    red: int = color & 0x0000FF
    return red, green, blue

def RGBToColor(R,G,B):
    return (R << 16) | (G << 8) | B

def FadeColor(StartColor, EndColor, Value):
  rStart, gStart, bStart = ColorToRGB(StartColor)
  rEnd, gEnd, bEnd = ColorToRGB(EndColor)
  ratio = Value / 255
  rEnd = round(rStart * (1 - ratio) + (rEnd * ratio))
  gEnd = round(gStart * (1 - ratio) + (gEnd * ratio))
  bEnd = round(bStart * (1 - ratio) + (bEnd * ratio))
  return RGBToColor(rEnd, gEnd, bEnd)

def LightenColor(Color, Value):
    r, g, b = ColorToRGB(Color)
    ratio = Value / 255
    return RGBToColor(round(r + (1.0 - r) * ratio), round(g + (1.0 - g) * ratio) , round(b + (1.0 - b) * ratio))


def hsv_to_rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value) color representation to RGB (Red, Green, Blue) color representation.

    Args:
        h (float): Hue value in the range [0, 1].
        s (float): Saturation value in the range [0, 1].
        v (float): Value (brightness) value in the range [0, 1].

    Returns:
        tuple: RGB color representation as a tuple of three values (red, green, blue) in the range [0, 1].

    """
    if s == 0.0:
        return v, v, v
    i = int(h*6.0)  # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def pad_color(rgb_8bit_tuple: tuple[int, int, int], brightness: int = 5, min: int = 2, max: int = 110) -> tuple[int, int, int]:
    """
    Adjusts the brightness of an RGB color tuple.

    Args:
        rgb_8bit_tuple (tuple[int, int, int]): The RGB color tuple to adjust.
        brightness (int, optional): The desired brightness level. Defaults to 5.
        min (int, optional): The minimum brightness level allowed. Defaults to 2.
        max (int, optional): The maximum brightness level allowed. Defaults to 110.

    Returns:
        tuple[int, int, int]: The adjusted RGB color tuple in 7bit integers.

    """
    r, g, b = rgb_8bit_tuple
    if brightness > max:
        brightness = max
    elif brightness < min:
        brightness = min
    unit_color = (r/255, g/255, b/255)
    hsv = rgb_to_hsv(*unit_color)
    red, green, blue  = hsv_to_rgb(hsv[0], hsv[1], brightness/127)
    red = round(red * 127)
    green = round(green * 127)
    blue = round(blue * 127)
    return (int(red), int(green), int(blue))

def RGB8_to_RGB7(rgb8: tuple[int, int, int]) -> tuple[int, int, int]:
    """Converts a RGB tuple from 8bit, 255 max, to 7 bit 127 max. This is useful for sending rgb value over Sysex messages, which may only support 7 bit, 127 max values."""
    return ( int(rgb8[0]/2), int(rgb8[1]/2), int(rgb8[2]/2) )


def RGB24ToHSV(R: int, G: int, B: int) -> tuple[float, float ,float]:
    """
    Converts an RGB color value to its corresponding HSV representation.

    Args:
        R (int): The red component of the RGB color (0-255).
        G (int): The green component of the RGB color (0-255).
        B (int): The blue component of the RGB color (0-255).

    Returns:
        tuple[float, float, float]: The HSV representation of the input RGB color, where:
            - H (float): The hue component (0-360).
            - S (float): The saturation component (0-1).
            - V (float): The value component (0-1).
    """
    
    Min = min(min(R, G), B)
    V = max(max(R, G), B)

    Delta = V - Min

    if V == 0:
        S = 0
    else:
        S = Delta / V

    if S == 0.0:
        H = 0.0 
    else:
        if R == V:
            H = 60.0 * (G - B) / Delta
        elif G == V:
            H = 120.0 + 60.0 * (B - R) / Delta
        elif B == V:
            H = 240.0 + 60.0 * (R - G) / Delta

        if H < 0.0:
            H = H + 360.0

    return H, S, V

def RGBIntegerToHSVColor(Color: int) -> tuple[float, float, float]:
    """
    Converts an RGB color value to its corresponding HSV color value.

    Args:
        Color (int): The RGB color value to convert.

    Returns:
        tuple[float, float, float]: The corresponding HSV color value as a tuple of floats (H, S, V).
    """
    r = ((Color & 0xFF0000) >> 16) / 255
    g = ((Color & 0x00FF00) >> 8) / 255
    b = ((Color & 0x0000FF) >> 0) / 255
    H, S, V = RGB24ToHSV(r, g, b)
    return H, S, V

def HSVtoRGB(H: int, S: float, V: int) -> tuple[int, int ,int]:
    """
    Converts a color from HSV (Hue, Saturation, Value) color space to RGB (Red, Green, Blue) color space.

    Args:
        H (int): The hue value in the range of 0 to 360.
        S (float): The saturation value in the range of 0.0 to 1.0.
        V (int): The value (brightness) value in the range of 0 to 255.

    Returns:
        tuple[int, int, int]: The RGB color values as a tuple of integers in the range of 0 to 255.

    """
    hTemp = 0
    if S == 0.0:
        R = V
        G = V
        B = V
    else:
        if H == 360.0:
            hTemp = 0.0
        else:
            hTemp = H

        hTemp = hTemp / 60
        i = math.trunc(hTemp)
        f = hTemp - i

        p = V * (1.0 - S)
        q = V * (1.0 - (S * f))
        t = V * (1.0 - (S * (1.0 - f)))

        if i == 0:
            R = V
            G = t
            B = p
        elif i == 1:
            R = q
            G = V
            B = p
        elif i == 2:
            R = p
            G = V
            B = t
        elif i == 3:
            R = p
            G = q
            B = V
        elif i == 4:
            R = t
            G = p
            B = V
        elif i == 5:
            R = V
            G = p
            B = q
    return int(R), int(G), int(B)

NoteNameT = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
