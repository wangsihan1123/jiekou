# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 21:38
# @Author   : qtf
# File      : mysql_handler.py
import pymysql
from pymysql.cursors import DictCursor
from common.logger_handler import logger

class MySQLHandler:
    def __init__(self,
                 host='',
                 port=3306,
                 user='',
                 password='',
                 charset='utf8',
                 # 指定数据库
                 database='',
                 cursorclass=DictCursor
                 ):
        try:
            self.conn.ping()
        except:
            self.conn = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   charset=charset,
                                   # 指定数据库
                                   database=database,
                                   cursorclass=cursorclass)
        logger.info("连接MySQL数据库成功.")


    def query_one(self,sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        # 事务提交
        self.conn.commit()
        data = self.cursor.fetchone()
        logger.info("查询MySQL一条数据.")
        self.cursor.close()
        return data

    def query_all(self,sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        # 事务提交
        self.conn.commit()
        data = self.cursor.fetchall()
        logger.info("查询MySQL多条数据.")
        self.cursor.close()
        return data

    def query(self,sql,one=False):
        # 结果是个list
        if one:
            return self.query_one(sql)
        return self.query_all(sql)

    def delete_cursor(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        # 事务提交
        self.conn.commit()
        logger.info("成功删除MySQL数据.")
        self.cursor.close()

    def close(self):
        # self.cursor.close()
        self.conn.close()
        logger.info("关闭MySQL数据库成功.")

# db_sql = DBHandle().query("select leave_amount from member where mobile_phone='15558191960'",one=True)
# print(db_sql)

