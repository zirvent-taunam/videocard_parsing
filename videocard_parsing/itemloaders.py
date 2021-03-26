from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst

from .processors import strip_string, remove_spaces


class VideocardLoader(ItemLoader):
    default_output_processor = Compose(strip_string)

    price_out = Compose(remove_spaces)
