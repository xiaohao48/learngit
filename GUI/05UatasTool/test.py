from paramiko import SFTPClient, Transport
from sshtunnel import SSHTunnelForwarder
import paramiko

host = 'jump-sz1.toolscash.top'
port = 22203
name = 'xiaohao'
passwd = 'N2RjMmVjZTVhNDFi'
host_uatas = '149.129.214.137'

# server = SSHTunnelForwarder(
#     (host, port),  # 跳板机
#     ssh_username=name,
#     ssh_password=passwd,
#     remote_bind_address=(host_uatas, 22))  # 远程服务器
# server.start()  # 开启隧道
# print(server.local_bind_port)
# transport = Transport(('127.0.0.1', server.local_bind_port))
#
# print(1)
# transport.connect(username=name, password=passwd)
#
# print('hello')
# transport.close()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# print(server.local_bind_port)
ssh.connect(hostname=host, port=22203, username=name, password=passwd)
print('hello')
ssh.close()
