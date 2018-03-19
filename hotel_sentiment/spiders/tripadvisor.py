# -*- coding: utf-8 -*-
import scrapy
from hotel_sentiment.items import HotelSentimentItem
import re

class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"
    start_urls = [
        "https://www.tripadvisor.in/Hotels-g35805-Chicago_Illinois-Hotels.html"
    ]

    def parse(self, response):
        for href in response.xpath('//a[@class="property_title"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_hotel)
    def parse_hotel(self, response):
        for href in response.xpath('//div[starts-with(@class,"quote")]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_review)

        # haha fuck you tripadvisor pagination I'm better than you
        url = response.url
        if not re.findall(r'or\d', url):
            next_page = re.sub(r'(-Reviews-)', r'\g<1>or5-', url)
        else:
            pagenum = int(re.findall(r'or(\d+)-', url)[0])
            pagenum_next = pagenum + 5
            next_page = url.replace('or' + str(pagenum), 'or' + str(pagenum_next))
        yield scrapy.Request(
            next_page,
            meta={'dont_redirect': True},
            callback=self.parse_hotel
        )

    def parse_review(self, response):
        item = HotelSentimentItem()
        item['title'] = response.xpath('//div[@class="quote"]/text()').extract()[0][1:-1]  # strip the quotes
        item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract()[0]
        item['stars'] = response.xpath('//span[starts-with(@class, "rating")]/span/@alt').extract()[0].replace('bubble', 'star')
        return item

