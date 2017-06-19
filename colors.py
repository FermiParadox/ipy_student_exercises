class Color(str):
    def __new__(cls, hex_val=None, rgb=None):
        representations = dict(hex_val=hex_val, rgb=rgb)
        if rgb:
            if not isinstance(rgb, (tuple, list)):
                raise TypeError('Rgb must be a list or tuple with exactly 3 elements.')
            if len(rgb) != 3:
                raise ValueError('Rgb must be a list or tuple with exactly 3 elements.')
        if not any(representations.values()):
            raise ValueError('No color representation provided. At least one needed.')

        inst = str.__new__(cls, hex_val)
        provided_representations = {k: v for k, v in representations.items() if v}
        inst.__dict__.update(provided_representations)
        return inst


red = Color(hex_val='FF3232')
gold = Color(hex_val='FFAA00')
green = Color(hex_val='00FF00')
blue = Color(hex_val='1a1aff')
black = Color(hex_val='000000')


def paint_text(text_str, color_str):
    """
    Adds markup around given text.
    Supports some colors by name instead of hexadecimal.

    :param text_str:
    :param color_str: (str) Hexadecimal color.
    :return: (str)
    """
    return '[color={color_str}]{text_str}[/color]'.format(text_str=text_str,
                                                          color_str=color_str)


