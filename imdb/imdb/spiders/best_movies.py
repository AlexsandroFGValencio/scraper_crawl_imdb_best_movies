# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies' 
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[position()=2]"), process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': (response.xpath("//div[@class='title_wrapper']/h1/text()").get()).strip(),
            'year': (response.xpath("//div[@class='title_wrapper']//h1/span/a/text()").get()).strip(),
            'duration': (response.xpath("//div[@class='title_wrapper']/div[@class='subtext']/time/text()").get()).strip(),
            'genre': (response.xpath("//div[@class='title_wrapper']/div[@class='subtext']/a/text()").get()).strip(),
            'rating': (response.xpath("//div[@class='ratingValue']/strong/span/text()").get()).strip(),
            'movie_url': (response.urljoin(response.xpath("//h3[@class='lister-item-header']/a").get())).strip(),
        }