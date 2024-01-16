# -*- coding: utf-8 -*-
# @Time     : 2023/1/10 19:56
# @Author   : qtf
# File      : sftp_handler.py
import paramiko
from common.logger_handler import logger

class SFTP:
    def __init__(self,
                 host='',
                 port=22,
                 username='',
                 password=''):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def sftp_exec_command(self,command):
        try:
            # 1.创建SSH对象
            ssh_client = paramiko.SSHClient()
            # 2.允许连接不在know_hosts文件中的主机
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 3.连接Linux服务器
            ssh_client.connect(hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password)
            std_in, std_out, std_err = ssh_client.exec_command(command)
            # result = stdout.read()
            for line in std_out:
                print(line.strip("\n"))
            ssh_client.close()
        except Exception as e:
            logger.error(e)

    def sftp_upload_file(self,server_path, local_path):
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(local_path, server_path)
            transport.close()
        except Exception as e:
            logger.info(e)

    def sftp_down_file(self,server_path, local_path):
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username='user', password='password')
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(server_path, local_path)
            transport.close()
        except Exception as e:
            logger.info(e)