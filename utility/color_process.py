def hex_decode(r,g,b):
    r = int(r)
    g = int(g)
    b = int(b)
    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return hex_color
def rgb_decode(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb