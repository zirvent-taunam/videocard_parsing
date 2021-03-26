import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from videocard_parsing.items import VideocardItem
from videocard_parsing.itemloaders import VideocardLoader


class RozetkaSpider(CrawlSpider):
    name = 'rozetka'
    allowed_domains = ['hard.rozetka.com.ua']
    start_urls = ['https://hard.rozetka.com.ua/videocards/c80087/21330=geforce-rtx-3080/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="goods-tile__heading"]',)), callback='parse_item'),
    )

    def parse_item(self, response):
        card_itemloader = VideocardLoader(item=VideocardItem(), selector=response)
        card_itemloader.add_xpath('title', './/h1[@class="product__title"]/text()')
        card_itemloader.add_value('link', response.url)
        card_itemloader.add_xpath('price', './/div[@class="product-prices__big"]')
        card_itemloader.add_xpath('availability', './/p[contains(@class, "product__status")]/text()')
        # item['availability'] = response.xpath('string(//div[@class="product-about__right"]/product-main-info)')
        return card_itemloader.load_item()


class RozetkaLoaderSpider(Spider):
    custom_settings = {
        'DUPEFILTER_DEBUG': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    name = 'rozetka2'
    allowed_domains = ['hard.rozetka.com.ua']
    start_urls = ['https://hard.rozetka.com.ua/videocards/c80087/21330=geforce-rtx-3080/']

    def parse(self, response, **kwargs):
        for tile in response.xpath('//ul[@class="catalog-grid"]//li[contains(@class, "catalog-grid__cell")]'):
            card_itemloader = VideocardLoader(item=VideocardItem(), selector=tile)
            card_itemloader.add_xpath('title', './/a[@class="goods-tile__heading"]/@title')
            card_itemloader.add_xpath('link', './/a[@class="goods-tile__heading"]/@href')
            card_itemloader.add_xpath('price', './/span[@class="goods-tile__price-value"]/text()')
            card_itemloader.add_xpath('availability', './/div[contains(@class, "goods-tile__availability")]/text()')

            yield card_itemloader.load_item()


class RozetkaPrimitiveSpider(Spider):
    name = 'rozetka3'
    allowed_domains = ['hard.rozetka.com.ua']
    start_urls = ['https://hard.rozetka.com.ua/videocards/c80087/21330=geforce-rtx-3080/']

    def parse(self, response):
        a = response.xpath('//div[@class="goods-tile"]')
        card_item = VideocardItem()
        # leave it with error .
        card_item['title'] = a.xpath('//a[@class="goods-tile__heading"]/@title').extract()
        card_item['link'] = a.xpath('//a[@class="goods-tile__heading"]/@href').extract()
        card_item['price'] = a.xpath('//span[@class="goods-tile__price-value"]/text()').extract()
        card_item['availability'] = a.xpath('//div[contains(@class, "goods-tile__availability")]/text()').extract()

        yield card_item
