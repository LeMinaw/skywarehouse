from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit


class CardThumbnail(ImageSpec):
    processors = [ResizeToFit(400, 400)]
    format = 'JPEG'
    options = {'quality': 80}

register.generator('warehouse:card_thumbnail', CardThumbnail)
