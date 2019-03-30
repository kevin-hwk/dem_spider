# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re

class CarPipeline(object):
    def table_exists(self,con,table_name):
        #判断数据表是否已经创建
        sql='show tables;'
        con.execute(sql)
        tables=[con.fetchall()]
        table_list=re.findall('(\'.*?\')',str(tables))
        table_list=[re.sub("'" ,'',each) for each in table_list]        #遍历并获得数据库表
        if table_name in table_list:
            return 1            #创建了返回1
        else:
            return 0            #不创建返回0

    def process_item(self, item, spider):
        connect=pymysql.connect(
            user='root',  # 用户名
            password='root1234',  # 密码
            db='lgweb',  # 数据库名
            host='127.0.0.1',  # 地址
            port=3306,  # 端口
            charset='utf8')

        conn=connect.cursor()           #创建一个数据游标
        conn.execute('use lgweb')       #选择指定的数据库
        table_name='db_suv'             #指定数据表

        ranking=item['ranking']                #取出管道里的数据
        car_name=item['car_name']
        price=item['price']
        hot=item['hot']
        brand=item['brand']
        style=item['style']
        dispt=item['dispt']
        gear=item['gear']

        if (self.table_exists(conn,table_name)!=1):
            sql='create table db_suv(排名 VARCHAR (20),车名 VARCHAR (50),价格 VARCHAR (40),人气度 VARCHAR (30),品牌 VARCHAR (40),车型 VARCHAR (40),排量 VARCHAR (50),变速箱 VARCHAR (50))'
            conn.execute(sql)              #不存在则创建数据库表

        try:
            sql="insert into db_suv(排名,车名,价格,人气度,品牌,车型,排量,变速箱)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(ranking,car_name,price,hot,brand,style,dispt,gear)
            conn.execute(sql)       #执行插入数据操作
            connect.commit()        #提交保存

        finally:
            conn.close()        #关闭数据库链接

        return item
