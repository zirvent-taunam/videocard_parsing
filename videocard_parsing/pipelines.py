import json

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from videocard_parsing.helpers import is_available, is_cheaper_then_max


class VideocardLocalParsingPipeline:
    def open_spider(self, spider):
        self.file = open('loaded/cards_rozetka.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            if is_cheaper_then_max(adapter.get('price')) and is_available(adapter.get('availability')):
                line = json.dumps(ItemAdapter(item).asdict()) + "\n"
                self.file.write(line)
                return item
        else:
            raise DropItem(f"Missing price or item is not available")


class VideocardCloudParsingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            if is_cheaper_then_max(adapter.get('price')) and is_available(adapter.get('availability')):
                return item
        else:
            raise DropItem(f"Missing price or item is not available")