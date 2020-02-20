# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WuyouItem(scrapy.Item):
    # 定义爬取得字段
    collection = 'jobs'
    #职位名
    job = scrapy.Field()
    #职位所在城市
    city = scrapy.Field()
    #公司名
    company = scrapy.Field()
    #薪资
    salary = scrapy.Field()
    #发布日期
    date = scrapy.Field()

