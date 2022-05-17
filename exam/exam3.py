import scrapy
from scrapy_splash import SplashRequest
from items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0, 'timeout': 60})

    def parse(self, response):
        authors = response.css('div.quote small.author::text').extract()
        quotes = response.css('div.quote span.text::text').extract()
        item = QuotesItem()
        item['authors'] = authors
        item['quotes'] = quotes
        yield from (dict(zip(['author', 'quote'], item)) for item in zip(authors, quotes))

        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            url = response.urljoin(next_url)
            yield SplashRequest(url, args={'images': 0, 'timeout': 60})
