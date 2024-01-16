# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 20:41
# @Author   : qtf
# File      : conftest.py
import pytest
import os, time
import requests
from middleware.handler import Handler, MidMySQLHandler, MidOracleHandler
from jsonpath import jsonpath


def login(username):
    """登录。 得到Cookie
    """
    resp = requests.request(method='POST',
                            url=Handler.env_config["env_url"] + '/UAMS/auth?username={}'.format(username),
                            headers={"Content-Type": "x-www-form-urlencoded"},
                            json={},
                            verify=False
                            )
    resp_json = resp.json()
    name_session = jsonpath(resp_json, '$..name')[0]
    value_session = jsonpath(resp_json, '$..value')[0]

    cookie = "=".join([name_session, value_session])
    return {"cookie": cookie}


@pytest.fixture()
def d_login():
    """数字化交付小组用户登录"""
    user = {
        "username": Handler.user_config['d_user']['username']
    }
    return login(user['username'])


@pytest.fixture()
def p_login():
    """P组用户登录"""
    user = {
        "username": Handler.user_config['p_user']['username']
    }
    return login(user['username'])


@pytest.fixture()
def c_login():
    """C组用户登录"""
    user = {
        "username": Handler.user_config['c_user']['username']
    }
    return login(user['username'])


@pytest.fixture()
def e_login():
    """E组用户登录"""
    user = {
        "username": Handler.user_config['e_user']['username']
    }
    return login(user['username'])


@pytest.fixture()
def k_login():
    """文控组用户登录"""
    user = {
        "username": Handler.user_config['k_user']['username']
    }
    return login(user['username'])


@pytest.fixture()
def a_login():
    """系统管理组组用户登录"""
    user = {
        "username": Handler.user_config['a_user']['username']
    }
    return login(user['username'])


@pytest.fixture()
def mysql_db():
    """管理MySQL数据库链接的夹具"""
    mysql_db_conn = MidMySQLHandler()
    # db_conn = Handler.db_class
    yield mysql_db_conn
    mysql_db_conn.close()


@pytest.fixture()
def oracle_db():
    """管理Oracle数据库链接的夹具"""
    oracle_db_conn = MidOracleHandler()
    yield oracle_db_conn
    oracle_db_conn.close()

# if __name__ == '__main__':
#     # print(oracle_db())
