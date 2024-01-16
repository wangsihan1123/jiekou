# -*- coding: utf-8 -*-
# @Time     : 2023/02/08 10:49
# @Author   : qtf
# File      : oracle_handler.py
import cx_Oracle
from common.logger_handler import logger


class OracleHandler:
    def __init__(self,
                 host='',
                 port='',
                 user='',
                 password='',
                 database='ORCL',
                 ):
        self.conn = cx_Oracle.connect(user=user,
                                      password=password,
                                      dsn='{}:{}/{}'.format(host, port, database))
        logger.info("连接Oracle数据库成功.")

    def query_one(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        # 事务提交
        self.conn.commit()
        data = self.cursor.fetchone()
        logger.info("查询Oracle一条数据.")
        self.cursor.close()
        return data

    def query_all(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        # 事务提交
        self.conn.commit()
        data = self.cursor.fetchall()
        logger.info("查询Oracle多条数据.")
        self.cursor.close()
        return data

    def query(self, sql, one=False):
        # 结果是个list
        if one:
            return self.query_one(sql)
        return self.query_all(sql)

    def delete_cursor(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        # 事务提交
        self.conn.commit()
        logger.info("成功删除Oracle数据.")
        self.cursor.close()

    def close(self):
        # self.cursor.close()
        self.conn.close()
        logger.info("关闭Oracle数据库成功.")

# db_sql = OracleHandler().query("SELECT * FROM EDC.QUESTION_TYPES WHERE ID = '97532617-2e02-441d-9a2e-5f2ee4e0399a'",one=True)
# print(db_sql)
