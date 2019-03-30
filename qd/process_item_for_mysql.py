import redis
import pymysql
import json,re


def table_exists(con, table_name):
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


def process_item():
    #redis数据库创建连接池对象 并实例化一个连接
    pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0,password='123456')
    redis_cli=redis.Redis(connection_pool=pool)

    #创建mysql数据库连接
    conn=pymysql.connect(user='root',  # 用户名
            password='root1234',  # 密码
            db='lgweb',  # 数据库名
            host='127.0.0.1',  # 地址
            port=3306,
            charset='utf8')


    table_name = 'db_read'  # 数据库表
    # 没有对应数据库表则创建
    if (table_exists(conn.cursor(),table_name) != 1):
        sql = 'create table db_read(书名 VARCHAR (30),作者 VARCHAR (30),评分 VARCHAR (10),类型 VARCHAR (30),状态 VARCHAR (30),简介 VARCHAR (50),详情 VARCHAR (1000),最新章节 VARCHAR (50),封面 VARCHAR (100))'
        conn.cursor().execute(sql)  # 不存在则创建数据库表

    offset=0
    while True:

        #将数据从redis里pop出来
        source,data=redis_cli.blpop("read:items")
        #将redis字符串转为格式化的字典
        item=json.loads(data)
        #创建数据库游标
        cursor=conn.cursor()
        sql = "insert into db_read(书名,作者,评分,类型,状态,简介,详情,最新章节,封面)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            item['book_name'],item['author'],item['score'],item['type'],item['state'],item['about'],item['story'],item['news'],item['photo'])
        cursor.execute(sql)     #执行数据插入
        conn.commit()           #提交记录

        cursor.close()          #关闭游标

        offset+=1
        print("正在保存第："+str(offset)+"条记录")

if __name__ == '__main__':
    process_item()