# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pandas import Series, DataFrame
import pandas as pd
from scrapy.exceptions import DropItem
import re

data = DataFrame(columns = ['job', 'company', 'city', 'salary', 'date'])
class WuyouPipeline(object):
    #def __init__(self):
    #    self.data = DataFrame(columns = ['job', 'company', 'city', 'salary', 'date'])
          
    def process_item(self, item, spider):
        #print(dict(item))
        #data.append(dict(item),ignore_index=True)
        #print(data)
        pass
           

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
    def process_item(self, item, spider):
        job_name = item['job']
        salary = item['salary']
        city = item['city']
        
        dirty_job_name = re.compile(r'(\*|在家|试用|体验|无需|无须|试玩|红包)+')
        dirty_salary = re.compile(r'(小时|天)+')
        
        
        #根据职业名进行数据清洗
        if(dirty_job_name.search(str(job_name))):
            raise DropItem("Dirty data %s" % item)
        if(dirty_salary.search(str(salary))):
            raise DropItem("Dirty data %s" % item)
        if(city.find("-") == -1):
            raise DropItem("Dirty data %s" % item)
        if(salary is None):
            raise DropItem("Dirty data %s" % item)
        if(job_name is None):
            raise DropItem("Dirty data %s" % item)
        
        #将薪资统一为以千为单位的月薪
        if (salary.find("万") != -1):
            p1 = salary.find("-")
            p2 = salary.find("万")
            if (salary.find("年") == -1):               
                salary_mid = (float(salary[:p1]) + float(salary[p1+1: p2])) / 2 * 10
                item['salary'] = round(salary_mid, 3)
            elif (salary.find("年") != -1):
                salary_mid = (float(salary[:p1]) + float(salary[p1+1: p2])) / 24 * 10
                item['salary'] = round(salary_mid, 3)                
        elif (salary.find("千") != -1):
            p1 = salary.find("-")
            p2 = salary.find("千")
            if (salary.find("年") == -1):               
                salary_mid = (float(salary[:p1]) + float(salary[p1+1: p2])) / 2
                item['salary'] = round(salary_mid, 3)
            elif (salary.find("年") != -1):
                salary_mid = (float(salary[:p1]) + float(salary[p1+1: p2])) / 24
                item['salary'] = round(salary_mid, 3)
        else:
            raise DropItem("Dirty data %s" % item)
               
        self.db[item.collection].insert_one(dict(item))
        return item
        
    def close_spider(self, spider):
        self.client.close()
        
        