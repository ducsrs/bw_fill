patterns = {
    'brackets': lambda x, y: (x % 10 == 0 and y % 10 < 5) or (y % 10 == 0 and x % 10 < 5),

    'diamonds': lambda x, y: patterns['slash_wide'](x, y) and patterns['backslash_wide'](x, y),

    'dots': lambda x, y: patterns['vertical'](x, y) and patterns['horizontal'](x, y),

    'tall_rect': lambda x, y: patterns['vertical_wide'](x, y) and patterns['horizontal'](x, y),

    'squares': lambda x, y: patterns['vertical_wide'](x, y) and patterns['horizontal_wide'](x, y),

    'slash_wide': lambda x, y: (y - x) % 20 < 6,

    'crosses': lambda x, y: (x % 10 == 2 and y % 10 < 5) or (y % 10 == 2 and x % 10 < 5),

    'wide_rect': lambda x, y: patterns['vertical'](x, y) and patterns['horizontal_wide'](x, y),

    'slash': lambda x, y: (y - x) % 10 < 2,

    'backslash_wide': lambda x, y: (y + x) % 20 < 6,

    'backslash': lambda x, y: (y + x) % 10 < 2,

    'horizontal_wide': lambda x, y: y % 20 < 6,

    'horizontal': lambda x, y: y % 10 < 2,

    'vertical_wide': lambda x, y: x % 20 < 6,

    'vertical': lambda x, y: x % 10 < 2,

    'bucket': lambda x, y: True
                     }


# patterns = [diamonds, dots, crosses, squares, brackets, tall_rect, wide_rect, slash_wide, backslash, backslash_wide,
#             horizontal, horizontal_wide, vertical, vertical_wide, bucket]
