# coding=utf-8
from scrapy import cmdline
import os
import time

job_name = input("职位：")
city = input("地点:")
text_width = len(job_name)+len(city)
sentence = 20 - text_width

area_top = {'北京': '010000' , '上海':'020000' , '广州':'030200' , '深圳':'040000' , \
            '西安':'200200' , '武汉':'180200' , '杭州':'080200' , '南京':'070200' , '成都':'090200' ,\
            '重庆':'060000' , '沈阳':'230200', '青岛':'120300' , '宁波':'080300' , '郑州':'170200' , \
            '天津':'050000' , '苏州':'070300' , '长沙':'190200' , '无锡':'070400' , '东莞':'030800', '珠三角':'01', '全国':'000000' }
            
if city not in area_top:
    print('系统还未录入该城市，请重新输入！')
    city = input("地点:")
    
print()
print('+' + '-' *  11 +'爬虫信息'+ '-' *  13  + '+')
print('| ' + ' ' * 30 + ' |')
print('| ' + '职位名\t地点' + ' '* 12 + ' |')
print('| ' +  job_name + '\t' + city + sentence * ' '+ ' |')

print('| ' + ' ' * 30 + ' |')
print('+' + '-' *  11 +'开始爬取'+ '-' *  13  + '+')
print()


with open('field.txt', 'w') as f:
    f.write(job_name + ',' + city)

os.system("pause")

cmdline.execute("scrapy crawl 51job".split())
