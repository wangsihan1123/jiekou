# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 11:35
# @Author   : qtf
# File      : handler.py
import datetime
import os, re
import time

from pymysql.cursors import DictCursor

from common.yaml_handler import read_yaml
from common.excel_handler import ExcelHandler
from common.mysql_handler import MySQLHandler
from common.oracle_handler import OracleHandler
from config import path


class MidMySQLHandler(MySQLHandler):
    """连接MySQL数据库"""

    def __init__(self):
        mysql_path = os.path.join(path.config_path, 'mysql_config.yaml')
        mysql_config = read_yaml(mysql_path)

        super().__init__(host=mysql_config['db']['host'],
                         port=mysql_config['db']['port'],
                         user=mysql_config['db']['user'],
                         password=mysql_config['db']['password'],
                         charset=mysql_config['db']['charset'],
                         # 指定数据库
                         database=mysql_config['db']['database'],
                         cursorclass=DictCursor)


class MidOracleHandler(OracleHandler):
    """连接Oracle数据库"""

    def __init__(self):
        oracle_path = os.path.join(path.config_path, 'oracle_config.yaml')
        oracle_config = read_yaml(oracle_path)
        super().__init__(host=oracle_config['db']['host'],
                         port=oracle_config['db']['port'],
                         user=oracle_config['db']['user'],
                         password=oracle_config['db']['password'],
                         # 指定数据库
                         database=oracle_config['db']['database'])


class Handler():
    """任务：中间层。 common 和 调用层。
    使用项目的配置数据，填充common模块
    """
    # 环境信息
    env_path = os.path.join(path.config_path, 'env_config.yaml')
    env_config = read_yaml(env_path)

    # 用户信息
    user_path = os.path.join(path.config_path, 'user_config.yaml')
    user_config = read_yaml(user_path)
    # mysql
    mysql_path = os.path.join(path.config_path, 'mysql_config.yaml')
    mysql_config = read_yaml(mysql_path)

    # excel对象
    excel_file = os.path.join(path.data_path, 'case_datas.xlsx')
    excel = ExcelHandler(excel_file)

    # 上传文件路径
    upload_files_path = os.path.join(path.root_path, 'upload_files')

    # MySQL数据库
    # db_class = MidMySQLHandler()

    # 需要动态替换#...# 的数据
    before_day = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天
    now_day = datetime.datetime.now().strftime("%Y-%m-%d")  # 今天
    next_day = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")  # 明天
    week_day = (datetime.datetime.now() + datetime.timedelta(days=-6)).strftime("%Y-%m-%d")  # 近一周
    month_day = (datetime.datetime.now() + datetime.timedelta(days=-28)).strftime("%Y-%m-%d")  # 近一月

    now_time_stamp = int(time.time())  # 获取当前时间戳，单位：秒
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
    # P组
    p_numbering = "P-87104"  # P组用户-位号
    p_doc_category_numbers = "D07-01-N_设备/材料变更、代用单"  # P组用户-分类号
    p_category_names = "柱塞泵"  # P组用户-工厂对象分类名称

    # E组/C组
    e_c_numbering = "F-87104"  # E组/C组用户-位号
    e_c_category_names = "管道过滤器"  # E组/C组用户-工厂对象分类名称

    @classmethod
    def replace_data(cls, string, pattern='#(.*?)#'):
        """数据动态替换"""
        # pattern = '#(.*?)#'
        results = re.finditer(pattern=pattern, string=string)
        for result in results:
            old = result.group()
            key = result.group(1)
            new = str(getattr(cls, key, ''))
            string = string.replace(old, new)
        return string
