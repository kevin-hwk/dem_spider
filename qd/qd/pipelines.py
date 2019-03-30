# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,re
from scrapy.exceptions import DropItem

class QdPipeline(object):

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
        table_name = 'db_read'  # 数据库表

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing %s of blogpost from %s' % (data, item['url']))
        if valid:  # 如果item里面有数据则取出来
            book_name = item['book_name']
            author = item['author']
            state = item['state']
            type = item['type']
            about = item['about']
            # number = item['number']
            score = item['score']
            story = item['story']
            news = item['news']
            photo = item['photo']

        # 没有对应数据库表则创建
        if (self.table_exists(conn, table_name) != 1):
            sql = 'create table db_read(书名 VARCHAR (30),作者 VARCHAR (30),评分 VARCHAR (10),类型 VARCHAR (30),状态 VARCHAR (30),简介 VARCHAR (50),详情 VARCHAR (1000),最新章节 VARCHAR (50),封面 VARCHAR (100))'
            conn.execute(sql)  # 不存在则创建数据库表

        try:
            # 有数据则插入数据表
            sql = "insert into db_read(书名,作者,评分,类型,状态,简介,详情,最新章节,封面)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                book_name,author,score,type,state,about,story,news, photo)
            conn.execute(sql)  # 执行插入数据操作
            self.connect.commit()  # 提交保存
        finally:
            conn.close()

        return item
