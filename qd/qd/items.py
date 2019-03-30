# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class QdItem(scrapy.Item):
    # define the fields for your item here like:

    book_name = scrapy.Field()          #书名
    author=scrapy.Field()               #作者
    state=scrapy.Field()                #状态
    type=scrapy.Field()                 #类型
    about=scrapy.Field()                #简介
    # number=scrapy.Field()               #字数
    score=scrapy.Field()                #评分
    story=scrapy.Field()                #故事
    news=scrapy.Field()                 #最新章节
    photo=scrapy.Field()                #封面
