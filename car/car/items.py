# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarItem(scrapy.Item):
    # define the fields for your item here like:

    ranking=scrapy.Field()          #排名
    car_name = scrapy.Field()       #车名
    price=scrapy.Field()            #价格
    hot=scrapy.Field()              #热度
    brand=scrapy.Field()            #品牌
    style=scrapy.Field()            #类型
    dispt=scrapy.Field()            #排量
    gear=scrapy.Field()             #变速箱


