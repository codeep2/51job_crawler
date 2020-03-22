# -*- coding: utf-8 -*-
import scrapy
from wuyou.items import WuyouItem
import datetime
from scrapy import Request

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['search.51job.com']

    def start_requests(self):
        with open('field.txt', 'r') as f:
            contents = f.read()
    
        area_top = {'北京': '010000' , '上海':'020000' , '广州':'030200' , '深圳':'040000' , \
            '西安':'200200' , '武汉':'180200' , '杭州':'080200' , '南京':'070200' , '成都':'090200' ,\
            '重庆':'060000' , '沈阳':'230200', '青岛':'120300' , '宁波':'080300' , '郑州':'170200' , \
            '天津':'050000' , '苏州':'070300' , '长沙':'190200' , '无锡':'070400' , '东莞':'030800', '珠三角':'01', '全国':'000000' }
    
        job_name = contents.split(',')[0]
        city = contents.split(',')[1]
    
        
        url = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,1.html'.format(area_top[city], job_name)
        
        yield Request(url)

    def parse(self, response):
        item = WuyouItem()
        jobs = response.xpath('//div[@class="el"]')
        for job in jobs:
            item['job'] = job.xpath('.//p[@class="t1 "]/span/a/@title').extract_first()
            item['company'] = job.xpath('.//span[@class="t2"]/a/text()').extract_first()
            item['city'] = job.xpath('.//span[@class="t3"]/text()').extract_first()
            item['salary'] = job.xpath('.//span[@class="t4"]/text()').extract_first()
            item['date'] = job.xpath('.//span[@class="t5"]/text()').extract_first()     
            yield item         
        
        next_url = response.xpath('//div[@class="p_in"]/ul/li[8]/a/@href').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse)