# -*- coding: utf-8 -*-
import scrapy
from wuyou.items import WuyouItem
import datetime
from scrapy import Request

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['search.51job.com']
    start_urls = ['https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html']

    def parse(self, response):
        item = WuyouItem()
        jobs = response.xpath('//div[@class="el"]')
        for job in jobs:
            item['job'] = job.xpath('.//p[@class="t1 "]/span/a/@title').extract_first()
            item['company'] = job.xpath('.//span[@class="t2"]/a/text()').extract_first()
            item['city'] = job.xpath('.//span[@class="t3"]/text()').extract_first()
            item['salary'] = job.xpath('.//span[@class="t4"]/text()').extract_first()
            item['date'] = job.xpath('.//span[@class="t5"]/text()').extract_first()
            #day = ''.join(item['date'])
            #day = datetime.datetime.strptime(day, '%m-%d')
            #day = day.replace(datetime.date.today().year)
            #item['date'] = day
            #yield item
         #'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,2.html'   
        
        next_url = response.xpath('//div[@class="p_in"]/ul/li[8]/a/@href').extract_first()
        print(next_url)
        print(type(next_url))
        if next_url:
            #注意extract是list，所以要转化为str
            yield Request(url=next_url, callback=self.parse)