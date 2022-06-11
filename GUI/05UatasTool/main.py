import tkinter as tk
import requests
import json
import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko
import pyperclip
import sys
import time

order_no = None
risk_loan_level = ['LEVEL_ONE', 'LEVEL_TWO', 'LEVEL_THREE']
user_level = ['L-0', 'L-1']
system = ['uatas test', 'zeus test', 'uatasfly test']

uatas_mysql_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'uatas',
    'password': 'c8CMsFW7pHmpjRss',
    'db': 'test_uatas',
    'charset': 'utf8'
}
SSH_mysql_config = {
    'ssh_password': 'rOub8bWwc3mxhpjj',
    'ssh_username': 'xiaohao',
    'remote_bind_address': ('149.129.214.137', 3306)
}
proxies = {
    "http": None,
    "https": None
}
aes_key_iv = {
    "uatas_rc": {"key": "uaRZnvZoJZ8KSTuE", "iv": "IFwDpMo01xY05ovH"},  # uatas风控
    "front_end": {"key": "THi8cml8EPlcdkfh", "iv": "1Q2ik8vpod90lhTg"},  # 前端
    "back_end": {"key": "k169flxzbooneepf", "iv": "abc123rty456nji7"}  # 后台
}


def aes_encrypt(url, password, iv, way, text):
    """AES加密"""
    data = {
        "mode": "CBC",
        "padding": "pkcs5",
        "block": 128,
        "password": password,
        "iv": iv,
        "encode": "base64",
        "way": way,  # 1-加密，2-解密
        "text": text,
        "method": "aes"
    }
    try:
        result = requests.post(url=url, data=data, proxies=proxies)
        html = result.text
        encrypt_date = json.loads(html)['d']['r']
        show_lb['text'] = encrypt_date
        return encrypt_date
    except:
        show_lb['text'] = f'{order_no.get()}加解密失败'


def aes_rc():
    url = 'https://tool.lmeee.com/jiami/crypt128inter'
    password = aes_key_iv['uatas_rc']['key']
    iv = aes_key_iv['uatas_rc']['iv']
    way = 1
    text = "{\"code\":0,\"data\":{\"code\":200,\"feature_list\":[],\"forbidApplyUntil\":1647746861000,\"loan_type\":0,\"order_no\":\"%s\",\"partner_id\":9000,\"passed\":\"false\",\"risk_amount\":\"0\",\"risk_loan_level\":\"%s\",\"sign\":\"4e32c73dafe476209843fd916a5cccb0\",\"user_idcard\":\"1141210809980028\",\"user_level\":\"%s\",\"user_name\":\"twenty seven\",\"user_phone\":\"82112341028\",\"zeus_order_no\":\"%s\"},\"msg\":\"\"}" % (
        order_no.get(), risk_loan_level_var.get(), user_level_var.get(), order_no.get())
    aes_encrypt(url, password, iv, way, text)


def front_end_encrypt():
    """前端加密"""
    url = 'https://tool.lmeee.com/jiami/crypt128inter'
    password = aes_key_iv['front_end']['key']
    iv = aes_key_iv['front_end']['iv']
    way = 1
    text = data_encrypt_var.get()
    aes_encrypt(url, password, iv, way, text)


def front_end_decrypt():
    """前端解密"""
    url = 'https://tool.lmeee.com/jiami/crypt128inter'
    password = aes_key_iv['front_end']['key']
    iv = aes_key_iv['front_end']['iv']
    way = 2
    text = data_encrypt_var.get()
    aes_encrypt(url, password, iv, way, text)


def back_end_encrypt():
    """后台加密"""
    url = 'https://tool.lmeee.com/jiami/crypt128inter'
    password = aes_key_iv['back_end']['key']
    iv = aes_key_iv['back_end']['iv']
    way = 1
    text = data_encrypt_var.get()
    aes_encrypt(url, password, iv, way, text)


def back_end_decrypt():
    """后台解密"""
    url = 'https://tool.lmeee.com/jiami/crypt128inter'
    password = aes_key_iv['back_end']['key']
    iv = aes_key_iv['back_end']['iv']
    way = 2
    text = data_encrypt_var.get()
    aes_encrypt(url, password, iv, way, text)


def mock_cloudun_callback():
    """模拟cloudun风控回调"""
    url = 'http://test-rc.uatas.id/rc/decisions/cloudun'
    data = {'data': "%s" % (aes_rc())}
    try:
        result = requests.post(url, data, proxies=proxies)
        html = result.text
        show_lb['text'] = f'{html} {order_no.get()}回调成功'
    except:
        show_lb['text'] = f'{order_no.get()}模拟cloudun风控回调失败'


def control_request():
    """订单请求风控"""
    url = 'http://test-rc.uatas.id/rc/check'
    data = {'data': '{"order_no": "%s" }' % order_no.get()}
    try:
        result = requests.post(url, data)
        html = result.text
        show_lb['text'] = html
    except:
        show_lb['text'] = f'{order_no.get()}请求风控失败'


def ssh_sever_start():
    global ssh_sever
    ssh_sever = SSHTunnelForwarder(
        ('jump-sz1.toolscash.top', 22201),
        ssh_password='rOub8bWwc3mxhpjj',
        ssh_username='xiaohao',
        remote_bind_address=('149.129.214.137', 3306)
    )
    ssh_sever.start()


def ssh_sever_end():
    db.close()
    ssh_sever.close()


def mysql_connect():
    global db
    ssh_sever_start()
    db = pymysql.connect(
        host='127.0.0.1',
        port=ssh_sever.local_bind_port,
        user='uatas',
        password='c8CMsFW7pHmpjRss',
        db='cash_order',
        charset='utf8'
    )
    return db


def mysql_select(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        show_lb['text'] = result
        return result
    except:
        show_lb['text'] = f'{order_no.get()}查询错误'
        return


def mysql_modify(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        show_lb['text'] = f'{order_no.get()}修改成功'
    except:
        db.rollback()
        show_lb['text'] = f'{order_no.get()}修改失败'


def modify_machine_status():
    """修改机审状态"""
    db = mysql_connect()
    sqls = [
        f'UPDATE cash_order.orders as o SET o.status=45 WHERE o.order_no={order_no.get()};',
        f'UPDATE cash_approve.approve as a SET a.machine_status=1 WHERE a.order_no={order_no.get()};']
    for sql in sqls:
        mysql_modify(db, sql)
    ssh_sever_end()


def order_change_reloan():
    """修改订单状态未待重新放款"""
    db = mysql_connect()
    sqls = [
        f'UPDATE cash_order.orders as o SET o.`status`=85 WHERE o.order_no={order_no.get()};',
        f'UPDATE cash_core.loan as l SET l.`status`=3 WHERE l.order_No={order_no.get()};',
        f'UPDATE cash_core.pay_record_log as g SET g.order_status=3 WHERE g.loan_id in (SELECT l.id FROM cash_core.loan as l WHERE l.order_No={order_no.get()});',
        f'UPDATE cash_pay.timepay_loan_order as p SET p.`status`=3 WHERE p.loan_no ={order_no.get()};'
    ]
    for sql in sqls:
        mysql_modify(db, sql)
    ssh_sever_end()


def order_overdue_sql():
    """修改订单逾期"""
    db = mysql_connect()
    sqls = [
        f'DELETE FROM `cash_core`.`day_order_acc` WHERE `loan_id` in (select id from cash_core.`loan` where order_No ={order_no.get()});',
        f'UPDATE cash_core.`loan` SET loan_time =loan_time-86400*1 where order_No={order_no.get()};',
        f'UPDATE cash_core.repayment_plan_detail SET  due_time=due_time-86400*1 where loan_id in (select id from cash_core.`loan` where order_No = {order_no.get()});'
    ]
    for sql in sqls:
        mysql_modify(db, sql)
    ssh_sever_end()


def order_overdue_ssh():
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connection.connect(hostname='jump-sz1.toolscash.top', port=22203, username='xiaohao', password='rOub8bWwc3mxhpjj',
                       allow_agent=False, look_for_keys=False)
    channel = connection.invoke_shell()
    channel.settimeout(10)
    channel.send(1 + '\n')
    time.sleep(3)

    # command = '1'
    # stdin, stdout, stderr = connection.exec_command(command)
    # command = '11'
    # stdin, stdout, stderr = connection.exec_command(command)
    # command = 'df -h'
    # stdin, stdout, stderr = connection.exec_command(command)

    # loginInfo = channel.recv(1024).decode('utf-8')
    # print(loginInfo)
    # command = 'df -h'
    # stdin, stdout, stderr = connection.exec_command(command)
    # print(stdout.read().decode('utf-8'))
    channel.close()
    connection.close()

    # trans = paramiko.Transport(('jump-sz1.toolscash.top', 22203))
    # print(trans , str(sys._getframe().f_lineno))
    # # trans.start_client()
    # trans.auth_password(username='xiaohao', password='rOub8bWwc3mxhpjj')
    # channel = trans.open_session(11)
    # print(channel)
    # channel.get_pty()
    # a = channel.invoke_shell()
    # print(a)
    # print(channel.recv(65535).decode('utf-8'))
    #
    # channel.close()
    # trans.close()


def clear_data():
    order_no.set(value='')
    show_lb['text'] = '已清空'


def copy():
    return pyperclip.copy(show_lb['text'])


def create_button(master, text, command, side=''):
    new_button = tk.Button(master=master, text=text, command=command)
    new_button.pack(side=side)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('uatas tool')

    """第一行"""
    frame01 = tk.Frame(master=root)
    frame01.pack()
    # 订单号标签
    order_no_label = tk.Label(frame01, text='order_no')
    order_no_label.pack(side='left')
    # 输入订单号
    order_no = tk.StringVar(frame01)
    order_no_entry = tk.Entry(frame01, text=order_no)
    order_no_entry.pack(side='left')
    # 清空按钮
    clear_bt = tk.Button(frame01, text='清空', command=clear_data)
    clear_bt.pack(side='left')
    # 复制按钮
    copy_bt = tk.Button(frame01, text='复制', command=copy)
    copy_bt.pack(side='left')
    # 系统选择
    system_var = tk.StringVar(value='uatas test')
    system_op = tk.OptionMenu(frame01, system_var, *system)
    system_op.pack(side='left')

    """第二行"""
    frame02 = tk.Frame(master=root)
    frame02.pack()
    # risk_loan_level选择
    risk_loan_level_var = tk.StringVar(value='LEVEL_ONE')
    risk_loan_level_op = tk.OptionMenu(frame02, risk_loan_level_var, *risk_loan_level)
    risk_loan_level_op.pack(side='left')
    # user_level选择
    user_level_var = tk.StringVar(value='L-0')
    user_level_op = tk.OptionMenu(frame02, user_level_var, *user_level)
    user_level_op.pack(side='left')
    # 过风控按钮
    control_request_bt = tk.Button(frame02, text='请求风控', command=control_request)
    control_request_bt.pack(side='left')
    # 加密按钮
    aes_encrypt_bt = tk.Button(frame02, text='风控AES加密', command=aes_rc)
    aes_encrypt_bt.pack(side='left')
    control_callback_bt = tk.Button(frame02, text='模拟cloudun回调', command=mock_cloudun_callback)
    control_callback_bt.pack(side='left')

    """第三行"""
    frame03 = tk.Frame(master=root)
    frame03.pack()
    # 订单状态改为过机审
    machine_status_bt = tk.Button(frame03, text='订单过机审', command=modify_machine_status)
    machine_status_bt.pack(side='left')
    # 订单改为待重新放款
    reloan_bt = tk.Button(frame03, text='订单待重新放款', command=order_change_reloan)
    reloan_bt.pack(side='left')
    # 订单逾期sql
    order_overdue_bt = tk.Button(frame03, text='订单逾期', command=order_overdue_sql)
    order_overdue_bt.pack(side='left')
    # 订单逾期脚本
    order_overdue_ssh_bt = tk.Button(frame03, text='订单逾期脚本', command=order_overdue_ssh)
    order_overdue_ssh_bt.pack(side='left')
    # 订单进贷后
    # 订单进催收

    # 根据uid查询在storage哪个表

    # 放款拉取
    # 还款拉取

    """加解密行"""
    frame_encrypt = tk.Frame(master=root)
    frame_encrypt.pack()
    # 加解密数据输入
    data_encrypt_var = tk.StringVar(frame_encrypt)
    data_encrypt_entry = tk.Entry(frame_encrypt, text=data_encrypt_var)
    data_encrypt_entry.pack()
    front_end_encrypt_bt = create_button(frame_encrypt, text="前端加密", command=front_end_encrypt, side='left')
    front_end_decrypt_bt = create_button(frame_encrypt, text="前端解密", command=front_end_decrypt, side='left')
    back_end_encrypt_bt = create_button(frame_encrypt, text="后台加密", command=back_end_encrypt, side='left')
    back_end_decrypt_bt = create_button(frame_encrypt, text="后台解密", command=back_end_decrypt, side='left')

    """展示行"""
    frame_show = tk.Frame(master=root)
    frame_show.pack()
    # 展示标签
    show_lb = tk.Label(frame_show, text='show', wraplength=800, background='green')
    show_lb.pack(side='left')

    root.mainloop()
