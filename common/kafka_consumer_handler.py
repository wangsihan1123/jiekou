# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 17:51
# @Author   : qtf
# File      : kafka_consumer_handler.py
import json
import os

from kafka import KafkaConsumer
from common.logger_handler import logger
from common.yaml_handler import read_yaml
from config import path


class KafkaConsumerHandler:
    def __init__(self,
                 topic='',
                 bootstrap_servers=''):
        self.consumer = KafkaConsumer(topic,
                                      bootstrap_servers=bootstrap_servers,
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=10000  # 超时处理
                                      )
        logger.info("连接Kafka数据库成功.")

    def consumer_kafka_data(self):
        """消费数据"""
        db_path = os.path.join(path.config_path, 'mysql_config.yaml')
        db_config = read_yaml(db_path)
        logger.info("开始消费Kafka数据。")
        kafka_datas = []
        for message in self.consumer:
            try:
                if message.key != None and str(message.key, encoding='utf-8') == db_config["device_infos"]["device_uuid"]:
                    value = json.loads(str(message.value, encoding='utf-8'))
                    kafka_datas.append(value)
            except:
                continue
        self.consumer.close()
        logger.info("Kafka数据消费完成.")
        return kafka_datas

    def consumer_kafka_single_model(self):
        """消费数据"""
        db_path = os.path.join(path.config_path, 'db_config.yaml')
        db_config = read_yaml(db_path)
        logger.info("开始消费Kafka数据。")
        kafka_datas = []
        for message in self.consumer:
            try:
                value = json.loads(str(message.value, encoding='utf-8'))
                if value["device_uuid"] == db_config["device_infos"]["single_model_device_uuid"]:
                    kafka_datas.append(value)
            except:
                continue
        self.consumer.close()
        logger.info("Kafka数据消费完成.")
        return kafka_datas


# kafka = KafkaConsumerHandler("DEVICE_METRIC_2_DRUID", '10.70.40.94:9092')
# print(kafka.consumer_kafka_data())
# print(kafka.consumer_kafka_single_model())