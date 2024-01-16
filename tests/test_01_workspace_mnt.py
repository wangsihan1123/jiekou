# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 14:25
# @Author   : qtf
# File      : test_01_workspace_mnt.py
import pytest, requests, json, allure, os
from jsonpath import jsonpath

from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('插件管理')


# case_ids = tuple([id["case_id"] for id in excel_datas])

@allure.title("插件管理-查询用户默认场景")
@pytest.mark.parametrize('datas', excel_datas)
def test_01_workspace_mnt(datas, a_login):
    """插件管理-查询用户默认场景"""
    datas = json.dumps(datas)

    if '#now_time_stamp#' in datas:
        datas = datas.replace('#now_time_stamp#', str(Handler.now_time_stamp))

    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    allure.dynamic.title(datas["title"])
    allure.dynamic.description("测试{}接口.".format(datas["title"]))

    headers = json.loads(datas["headers"])
    headers["Cookie"] = a_login["cookie"]

    with allure.step('请求方式'):
        allure.attach('{}'.format(datas["method"]), name='{}请求方式'.format(datas["title"]))

    with allure.step('请求路径'):
        allure.attach('{}'.format(datas["path"]), name='{}请求路径'.format(datas["title"]))

    with allure.step('请求体'):
        allure.attach('{}'.format(datas["data"]), name='{}请求体'.format(datas["title"]))
    logger.info("{}请求路径为:{},请求体为:{}".format(datas["title"], datas["path"], datas["data"]))

    files = json.loads(datas["files"])
    if "上传2" in datas["title"]:
        files = [
            ("pmIconFile", (
                files[0]["file_name"],
                open(Handler.upload_files_path + files[0]["file_path"], "rb"),
                files[0]["content_type"]
            )),
            ("pdIconFile", (
                files[1]["file_name"],
                open(Handler.upload_files_path + files[1]["file_path"], "rb"),
                files[1]["content_type"],
            ))
        ]
    elif "上传1" in datas["title"]:
        files = {"file": (
            files["file_name"], open(Handler.upload_files_path + files["file_path"], "rb"), files["content_type"])}
    try:
        resp = requests.request(method=datas["method"],
                                url=Handler.env_config["env_url"] + datas["path"],
                                headers=headers,
                                files=files,
                                data=json.loads(datas["data"]),
                                json=json.loads(datas["json"]),
                                verify=False)
    except requests.exceptions.RequestException as e:
        logger.error("发出请求时出错: {}".format(e))
        raise e

    with allure.step('响应'):
        allure.attach('{}'.format(resp.status_code), name='状态码')
    logger.info("{}状态码：{}，响应结果:{}".format(datas["title"], resp.status_code, resp.text))
    # logger.info("{}状态码：{}，响应结果:{}".format(datas["title"], resp.status_code, resp.json()))

    expected = json.loads(datas['expected'])
    # 状态码断言
    with allure.step('断言'):
        for key, value in expected.items():
            assert resp.status_code == value
            allure.attach('OK', name='{}断言'.format(key))
    # 多值断言
    # with allure.step('断言'):
    #     for key, value in expected.items():
    #         assert str(jsonpath(resp.json(), key)[0]) == value
    #         allure.attach('OK', name='{}断言'.format(key))

    # 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            setattr(Handler, prop, value)
