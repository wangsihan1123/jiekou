# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 21:36
# @Author   : qtf
# File      : yaml_handler.py
import yaml

def read_yaml(fpath):
    with open(fpath, encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data
