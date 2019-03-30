# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,re
from scrapy.exceptions import DropItem

class ZhPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            user='root',  # 用户名
            password='root1234',  # 密码
            db='lgweb',  # 数据库名
            host='127.0.0.1',  # 地址
            port=3306,
            charset='utf8'
        )

    def table_exists(self, con, table_name):
        # 判断数据表是否已经创建
        sql = 'show tables;'
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]  # 遍历并获得数据库表
        if table_name in table_list:
            return 1  # 创建了返回1
        else:
            return 0  # 不创建返回0

    def process_item(self, item, spider):
        conn = self.connect.cursor()  # 创建该链接的游标
        conn.execute('use lgweb')  # 指定数据库
        table_name = 'db_book'  # 数据库表

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing %s of blogpost from %s' % (data, item['url']))
        if valid:  # 如果item里面有数据则取出来
            book_name = item['book_name']
            state = item['state']
            type = item['type']
            label = item['label']
            author = item['author']
            number = item['number']
            about = item['about']
            news = item['news']
            photo = item['photo']
        # 没有对应数据库表则创建
        if (self.table_exists(conn, table_name) != 1):
            sql = 'create table db_book(书名 VARCHAR (30),当前状态 VARCHAR (30),类型 VARCHAR (30),特点 VARCHAR (100),作者 VARCHAR (30),字数 VARCHAR (20),简介 VARCHAR (1000),最新章节 VARCHAR (20),封面 VARCHAR (100))'
            conn.execute(sql)  # 不存在则创建数据库表

        try:
            # 有数据则插入数据表
            sql = "insert into db_book(书名,当前状态,类型,特点,作者,字数,简介,最新章节,封面)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                book_name,state,type,label,author,number,about,news,photo)
            conn.execute(sql)  # 执行插入数据操作
            self.connect.commit()  # 提交保存
        finally:
            conn.close()

        return item
