from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit


class CardThumbnail(ImageSpec):
    processors = [ResizeToFit(400, 1000)]
    format = 'JPEG'
    options = {'quality': 90}

register.generator('warehouse:card_thumbnail', CardThumbnail)
