import PIL.Image
from patterns import p as patterns
from text_protector import Protector

if __name__ == '__main__':
    import ui

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# img = PIL.Image.open('pie_chart.png')

def bw_fill(img, protect=True):
    img.convert('RGB')

    replacements = get_regions(img)

    color_list = sorted(replacements.items(), key=lambda c: c[1]['count'], reverse=True)
    # List of ((r, g, b), dict) tuples sorted high->low by count
    assign_replacements(color_list)

    return process(color_list, img, protect)


def process(color_list, img, protect):
    protector = Protector(img) if protect else False

    for (color, info) in color_list:
        if not info['replacement']:
            break
        else:
            pattern = info['replacement']
            for (x, y) in info['pixels']:
                if not protect or not protector.check_boxes(x, y):
                    new_color = BLACK if pattern(x, y) else WHITE
                    img.putpixel((x, y), new_color)

    return img.convert('L')


def assign_replacements(color_list):
    """Mutates color_list by assigning a replacement function to each of the most frequent colors."""
    prev_count = 0
    for (p, c) in zip(patterns.values(), color_list):
        if c[1]['count'] < prev_count / 50:
            break
        c[1]['replacement'] = p
        prev_count = c[1]['count']


def get_regions(img):
    """Makes a dict with counts and pixels for each color"""
    replacements = {}
    # {(r, g, b) : {
    #                               count: i,
    #                               replacement: pattern,
    #                               pixels: [(x,y),...]}}
    for x in range(img.width):
        for y in range(img.height):
            color = img.getpixel((x, y))
            if color not in replacements.keys():
                replacements[color] = {'count': 1,
                                       'pixels': [(x, y)],
                                       'replacement': None}
            else:
                replacements[color]['count'] += 1
                replacements[color]['pixels'].append((x, y))
    return replacements


# bw_fill('bar_graph.png', protect=True).show()
