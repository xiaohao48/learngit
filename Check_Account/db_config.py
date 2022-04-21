import pymysql
import json
import time
import logging
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine

server = SSHTunnelForwarder(
    ('jump-sz1.toolscash.top', 22201),  # B机器的配置
    ssh_password='uJZvhwsgp89rizpu',
    ssh_username='zhangyihao',
    remote_bind_addresses=[('94.74.88.70', 3306)]
)
server.start()

config = {
    "host": "127.0.0.1",  # 地址
    "port": server.local_bind_ports[0],  # 端口
    "user": "cloudun2",  # 用户名
    "password": "9EI4NtL8Ccmh^!mX",  # 密码
    "db": 'uatas_bi',
    "charset": "utf8"
}
uatas_bi_db = pymysql.connect(**config)
uatas_bi_cursor = uatas_bi_db.cursor(cursor=pymysql.cursors.DictCursor)

conn_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
config['user'], config['password'], config['host'], config['port'], config['db']))
