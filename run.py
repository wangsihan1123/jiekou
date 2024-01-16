# -*- coding: utf-8 -*-
# @Time     : 2021/1/18 21:20
# @Author   : qtf
# File      : run.py
"""
项目入口，主程序
收集用例，运行用例，生成报告
"""
import os,pytest
from datetime import datetime
from config.path import reports_path

# pytest 收集用例
def run_case():
    # timestamp = str(datetime.now().strftime("%Y-%m-%d %H_%M_%S"))
    # reportfilename = 'report_%s.html' % timestamp
    # htmlreport = os.path.join(reports_path, reportfilename)
    # pytest.main(['--html={}'.format(htmlreport)])

    # allure的安装和使用：https://blog.csdn.net/lixiaomei0623/article/details/120185069

    pytest.main(['--alluredir', 'reports/allure-report'])
    os.system(r'allure generate reports/allure-reports -o reports/html --clean')

    # jenkins配置
    # pytest -s -q --alluredir reports/allure-reports
    # allure generate reports/allure-reports -o reports/html --clean
    # 需要在终端运行命令：allure generate ./report/result -o ./report/html --clean 生成html文件

run_case()
