# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ZhItem(scrapy.Item):
    # define the fields for your item here like:

    book_name=scrapy.Field()        #书名
    state=scrapy.Field()            #当前状态
    type=scrapy.Field()             #所属类型
    label=scrapy.Field()            #标签
    author=scrapy.Field()           #作者
    number=scrapy.Field()           #字数
    about=scrapy.Field()            #简介
    news=scrapy.Field()             #最新章节
    photo=scrapy.Field()            #封面

