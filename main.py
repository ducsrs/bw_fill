import PIL.Image
from patterns import patterns
from text_protector import Protector
import ui

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# img = PIL.Image.open('pie_chart.png')

def bw_fill(filename, protect=True):
    img = PIL.Image.open(filename).convert('RGB')
    if protect:
        protector = Protector(img)
    colors = sorted(img.getcolors(maxcolors=10000), reverse=True)
    # if colors is None:
    #     raise ValueError('Too many colors.')

    prev_count = 0
    replacements = {}
    # key is (r,g,b) tuples, value is a function from the patterns set
    # [1:] slice assumes that the most common color is the background
    for pattern, color in zip(patterns, colors[1:]):
        if color[0] < prev_count / 50:
            break
        replacements[color[1]] = patterns[pattern]
        prev_count = color[0]

    for x in range(img.width):
        for y in range(img.height):
            if not protect or not protector.check_boxes(x, y):
                color = img.getpixel((x, y))
                if color in replacements:
                    if replacements[color](x, y):
                        new_color = BLACK
                    else:
                        new_color = WHITE
            # elif color == colors[0][1]:
            #     new_color = WHITE
            # else:
            #     new_color = BLACK
                    img.putpixel((x, y), new_color)

    return img.convert('L')



