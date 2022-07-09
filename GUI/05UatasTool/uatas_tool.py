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
url_crypt = 'https://tool.lmeee.com/jiami/crypt128inter'

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
    "front_end_zeus": {"key": "Ckgx3U1QufHbcQns", "iv": "so8RhHi4jkaci4ze"},  # zeus前端
    "back_end_zeus": {"key": "93LJ7sxQALXuMgLj", "iv": "jlsfjiosmhosl5db"},  # zeus后台
    "front_end_uatas": {"key": "daDtbXYkhhnHi1XF", "iv": "H9Rlows19wkBSx3w"},  # uatas前端
    "back_end_uatas": {"key": "z1aXNVB4JJw4ZZ0r", "iv": "LzsCmdfFbAvQ1fbD"}  # uatas后台
}
scripts = {
    '展期生成新订单': 'php /home/rong/www/time-core/webroot/batch.php push VirtualOrderNotify',
    'uatas放款拉取': "php /home/rong/www/time-pay/webroot/batch.php TimePayLoan PollingLoanResult --payHandel='UP'",
    'uatas还款拉取': "php /home/rong/www/time-pay/webroot/batch.php TimePayRepay PollingRepayResult --orderNo='' --payHandel='UP'",
    "uatas入贷后": "php /home/rong/www/time-cuishou/webroot/batch.php Daihouivr GetDaihouIvr --day=",
    "uatas逾期费": "php /home/rong/www/time-core/webroot/batch.php FqRepayment CalDayFee --loanId=",
    "uatas入催收": "php /home/rong/www/time-core/webroot/batch.php RepayPlanTask IncuiShouTask",
    "用户storage目录查询": 'php -r "echo crc32() % 10;"',
    "uatas api绑定银行卡": "php /home/rong/www/time-order/webroot/command.php Customer ConsumeBankCard",
    "oppo打包放款": "php /home/rong/UatasPay/yii batch-disbursement/batch-loan"
}

encrypt_list = [
    ['zeus前端加密', {'key': 'Ckgx3U1QufHbcQns', 'iv': 'so8RhHi4jkaci4ze', 'way': 1}],
    ['zeus前端解密', {'key': 'Ckgx3U1QufHbcQns', 'iv': 'so8RhHi4jkaci4ze', 'way': 2}],
    ['zeus后端加密', {'key': '93LJ7sxQALXuMgLj', 'iv': 'jlsfjiosmhosl5db', 'way': 1}],
    ['zeus后端解密', {'key': '93LJ7sxQALXuMgLj', 'iv': 'jlsfjiosmhosl5db', 'way': 2}],
    ['uatas前端加密', {'key': 'daDtbXYkhhnHi1XF', 'iv': 'H9Rlows19wkBSx3w', 'way': 1}],
    ['uatas前端解密', {'key': 'daDtbXYkhhnHi1XF', 'iv': 'H9Rlows19wkBSx3w', 'way': 2}],
    ['uatas后端加密', {'key': 'z1aXNVB4JJw4ZZ0r', 'iv': 'LzsCmdfFbAvQ1fbD', 'way': 1}],
    ['uatas后端解密', {'key': 'z1aXNVB4JJw4ZZ0r', 'iv': 'LzsCmdfFbAvQ1fbD', 'way': 2}]
]
encrypt_dict = dict(encrypt_list)


def data_encrypt():
    """业务加解密功能"""
    # encrypt_dict = dict(encrypt_list)
    if encrypt_var.get() in encrypt_dict.keys():
        data = aes_encrypt(
            url=url_crypt,
            password=encrypt_dict[encrypt_var.get()]['key'],
            iv=encrypt_dict[encrypt_var.get()]['iv'],
            way=encrypt_dict[encrypt_var.get()]['way'],
            text=data_encrypt_text.get(1.0, tk.END)
        )
        show_lb['text'] = data


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
    password = aes_key_iv['uatas_rc']['key']
    iv = aes_key_iv['uatas_rc']['iv']
    way = 1
    text = "{\"code\":0,\"data\":{\"code\":200,\"feature_list\":[],\"forbidApplyUntil\":1647746861000,\"loan_type\":0,\"order_no\":\"%s\",\"partner_id\":9000,\"passed\":\"false\",\"risk_amount\":\"0\",\"risk_loan_level\":\"%s\",\"sign\":\"4e32c73dafe476209843fd916a5cccb0\",\"user_idcard\":\"1141210809980028\",\"user_level\":\"%s\",\"user_name\":\"twenty seven\",\"user_phone\":\"82112341028\",\"zeus_order_no\":\"%s\"},\"msg\":\"\"}" % (
        order_no.get(), risk_loan_level_var.get(), user_level_var.get(), order_no.get())
    aes = aes_encrypt(url_crypt, password, iv, way, text)
    return aes


# def front_end_encrypt():
#     """前端加密"""
#     url = 'https://tool.lmeee.com/jiami/crypt128inter'
#     password = aes_key_iv['front_end_zeus']['key']
#     iv = aes_key_iv['front_end_zeus']['iv']
#     way = 1
#     text = data_encrypt_var.get()
#     aes_encrypt(url, password, iv, way, text)


# def front_end_decrypt():
#     """前端解密"""
#     url = 'https://tool.lmeee.com/jiami/crypt128inter'
#     password = aes_key_iv['front_end_zeus']['key']
#     iv = aes_key_iv['front_end_zeus']['iv']
#     way = 2
#     text = data_encrypt_var.get()
#     aes_encrypt(url, password, iv, way, text)


# def back_end_encrypt():
#     """后台加密"""
#     url = 'https://tool.lmeee.com/jiami/crypt128inter'
#     password = aes_key_iv['back_end_zeus']['key']
#     iv = aes_key_iv['back_end_zeus']['iv']
#     way = 1
#     text = data_encrypt_var.get()
#     aes_encrypt(url, password, iv, way, text)


# def back_end_decrypt():
#     """后台解密"""
#     url = 'https://tool.lmeee.com/jiami/crypt128inter'
#     password = aes_key_iv['back_end_zeus']['key']
#     iv = aes_key_iv['back_end_zeus']['iv']
#     way = 2
#     text = data_encrypt_var.get()
#     aes_encrypt(url, password, iv, way, text)


def mock_cloudun_callback():
    """模拟cloudun风控回调"""
    url = 'http://test-rc.uatas.id/rc/decisions/cloudun'
    data = json.dumps({"data": "%s" % (aes_rc())})
    try:
        result = requests.post(url, data, proxies=proxies)
        html = result.text
        show_lb['text'] = f'{html} {order_no.get()}回调成功'
    except:
        show_lb['text'] = f'{order_no.get()}模拟cloudun风控回调失败'


def control_request():
    """订单请求风控"""
    sql = f'UPDATE cash_order.orders as o SET o.create_time=FROM_UNIXTIME(UNIX_TIMESTAMP(o.create_time)-3600) ' \
          f'WHERE o.order_no={order_no.get()};'
    mysql_modify(mysql_connect(), sql)

    # time.sleep(2)
    ssh_sever_end()
    url = 'http://test-rc.uatas.id/rc/check'
    data = {'data': '{"order_no": "%s" }' % order_no.get()}
    print(data)
    try:
        result = requests.post(url, data)
        html = result.text
        show_lb['text'] = html
    except:
        show_lb['text'] = f'{order_no.get()}请求风控失败'


def ssh_sever_start():
    """跳板服务开启"""
    global ssh_sever
    ssh_sever = SSHTunnelForwarder(
        ('jump-sz1.toolscash.top', 22201),
        ssh_password='rOub8bWwc3mxhpjj',
        ssh_username='xiaohao',
        remote_bind_address=('149.129.214.137', 3306)
    )
    ssh_sever.start()


def ssh_sever_end():
    """跳板服务关闭"""
    db.close()
    ssh_sever.close()


def mysql_connect():
    """数据库连接"""
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
    """数据库查询操作"""
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        show_lb['text'] = result
        return result
    except:
        show_lb['text'] = f'{order_no.get()}查询错误'


def mysql_modify(db, sql):
    """数据库更新操作"""
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        show_lb['text'] = f'{order_no.get()}修改成功'
    except:
        db.rollback()
        show_lb['text'] = f'{order_no.get()}修改失败'


def select_order():
    """数据库订单状态查询"""
    db = mysql_connect()
    sql = f'SELECT o.order_no,o.`status` FROM cash_order.orders as o WHERE o.order_no ={order_no.get()};'
    mysql_select(db, sql)
    ssh_sever_end()


def modify_machine_status():
    """修改机审状态"""
    db = mysql_connect()
    sqls = [
        f'UPDATE cash_order.orders as o SET o.status=45 WHERE o.order_no={order_no.get()};',
        f'UPDATE cash_approve.approve as a SET a.machine_status=1 WHERE a.order_no={order_no.get()};'
    ]
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
        f'UPDATE cash_core.repayment_plan_detail SET  due_time=due_time-86400*1 where loan_id in (select id from cash_core.`loan` where order_No = {order_no.get()});',
        f'UPDATE cash_order.orders as o SET o.loan_time=o.loan_time-86400*1 WHERE o.order_no={order_no.get()};'
    ]
    for sql in sqls:
        mysql_modify(db, sql)
    ssh_sever_end()


def order_overdue_ssh():
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connection.connect(hostname='jump-sz1.toolscash.top', port=22203, username='xiaohao', password='N2RjMmVjZTVhNDFi')
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
    """清空功能"""
    order_no.set(value='')
    # data_encrypt_var.set(value='')
    data_encrypt_text.delete(1.0, tk.END)
    show_lb['text'] = '已清空'


def copy():
    """复制功能"""
    return pyperclip.copy(show_lb['text'])


def create_button(master, text, command, row, column, width=30, sticky='ew'):
    """创建按钮功能"""
    new_button = tk.Button(master=master, text=text, command=command, width=width)
    new_button.grid(row=row, column=column, sticky=sticky)
    return new_button


def script():
    """查看脚本"""
    if script_var.get() in scripts.keys():
        show_lb['text'] = scripts[script_var.get()]
    else:
        show_lb['text'] = '输入错误'


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('uatas tool')
    column = 0

    """第一行，共15行5列"""
    row = 0
    # 订单号标签
    order_no_label = tk.Label(root, text='order_no')
    order_no_label.grid(row=row, column=column + 1, sticky='ew')
    # 输入订单号
    order_no = tk.StringVar()
    order_no_entry = tk.Entry(root, text=order_no)
    order_no_entry.grid(row=row, column=column + 2, sticky='ew')
    # 系统选择
    system_var = tk.StringVar(value='uatas test')
    system_op = tk.OptionMenu(root, system_var, *system)
    system_op.grid(row=row, column=column + 3, sticky='ew')
    aes_encrypt_bt = create_button(root, text='风控AES加密', command=aes_rc, row=row, column=column + 4)

    """第二行"""
    row = row + 1
    # risk_loan_level选择
    risk_loan_level_var = tk.StringVar(value='LEVEL_ONE')
    risk_loan_level_op = tk.OptionMenu(root, risk_loan_level_var, *risk_loan_level)
    risk_loan_level_op.grid(row=row, column=column + 1, sticky='ew')
    # user_level选择
    user_level_var = tk.StringVar(value='L-0')
    user_level_op = tk.OptionMenu(root, user_level_var, *user_level)
    user_level_op.grid(row=row, column=column + 2, sticky='ew')
    # 过风控按钮
    control_request_bt = create_button(root, text='请求风控', command=control_request, row=row, column=column + 3)
    # 加密按钮
    control_callback_bt = create_button(root, text='模拟cloudun回调', command=mock_cloudun_callback, row=row,
                                        column=column + 4)

    """第三行"""
    row = row + 1
    select_order_bt = create_button(root, text='订单信息查询', command=select_order, row=row, column=column + 1)
    # 订单状态改为过机审
    machine_status_bt = create_button(root, text='订单过机审', command=modify_machine_status, row=row, column=column + 2)
    # 订单改为待重新放款
    reloan_bt = create_button(root, text='订单待重新放款', command=order_change_reloan, row=row, column=column + 3)
    # 订单逾期sql
    order_overdue_bt = create_button(root, text='订单逾期', command=order_overdue_sql, row=row, column=column + 4)
    # 订单逾期脚本
    # order_overdue_ssh_bt = tk.Button(frame03, text='订单逾期脚本', command=order_overdue_ssh)
    # order_overdue_ssh_bt.pack(side='left')

    # 根据uid查询在storage哪个表

    """加解密输入行"""
    row = row + 1
    # 加解密数据输入
    # data_encrypt_var = tk.StringVar(root)
    # data_encrypt_entry = tk.Entry(root, text=data_encrypt_var, width=100)
    # data_encrypt_entry.grid(row=row, column=column + 1, columnspan=5)

    row = row + 1
    data_encrypt_text = tk.Text(root, width=120, height=4)
    data_encrypt_text.grid(row=row, column=column, columnspan=5)

    """加解密行"""
    row = row + 1
    encrypt_lb = tk.Label(root, text='待加解密数据↑')
    encrypt_lb.grid(row=row, column=column + 1)
    encrypt_var = tk.StringVar(value=encrypt_list[0][0])
    encrypt_op = tk.OptionMenu(root, encrypt_var, *encrypt_dict.keys())
    encrypt_op.grid(row=row, column=column + 2, sticky='ew')
    encrypt_bt = create_button(root, text='加解密', command=data_encrypt, row=row, column=column + 3)

    """zeus加解密行"""
    """
    row = row + 1
    front_end_encrypt_bt_z = create_button(root, text="zeus前端加密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['front_end_zeus']['key'],
        iv=aes_key_iv['front_end_zeus']['iv'],
        way=1,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 1, width=24)
    front_end_decrypt_bt_z = create_button(root, text="zeus前端解密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['front_end_zeus']['key'],
        iv=aes_key_iv['front_end_zeus']['iv'],
        way=2,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 2, width=24)
    back_end_encrypt_bt_z = create_button(root, text="zeus后台加密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['back_end_zeus']['key'],
        iv=aes_key_iv['back_end_zeus']['iv'],
        way=1,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 3, width=24)
    back_end_decrypt_bt_z = create_button(root, text="zeus后台解密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['back_end_zeus']['key'],
        iv=aes_key_iv['back_end_zeus']['iv'],
        way=2,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 4, width=24)

    '''uatas加解密行'''
    row = row + 1
    front_end_encrypt_bt_u = create_button(root, text="uatas前端加密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['front_end_uatas']['key'],
        iv=aes_key_iv['front_end_uatas']['iv'],
        way=1,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 1, width=24)
    front_end_decrypt_bt_u = create_button(root, text="uatas前端解密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['front_end_uatas']['key'],
        iv=aes_key_iv['front_end_uatas']['iv'],
        way=2,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 2, width=24)
    back_end_encrypt_bt_u = create_button(root, text="uatas后台加密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['back_end_uatas']['key'],
        iv=aes_key_iv['back_end_uatas']['iv'],
        way=1,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 3, width=24)
    back_end_decrypt_bt_u = create_button(root, text="uatas后台解密", command=lambda: aes_encrypt(
        url=url_crypt,
        password=aes_key_iv['back_end_uatas']['key'],
        iv=aes_key_iv['back_end_uatas']['iv'],
        way=2,
        text=data_encrypt_text.get(1.0, tk.END)
    ), row=row, column=column + 4, width=24)
    """

    """查看脚本"""
    row = row + 1
    script_var = tk.StringVar(value='选择脚本')
    script_op = tk.OptionMenu(root, script_var, *scripts.keys())
    script_op.grid(row=row, column=column + 1, sticky='ew')
    script_bt = create_button(master=root, text='查看脚本', row=row, column=column + 2, command=script)
    # 复制按钮
    copy_bt = create_button(root, text='复制', command=copy, row=row, column=column + 3)
    # 清空按钮
    clear_bt = create_button(root, text='清空', command=clear_data, row=row, column=column + 4)

    """展示行"""
    row = row + 1
    show_lb = tk.Label(root, text='show', wraplength=800, background='green')
    show_lb.grid(row=row, column=column + 1, columnspan=5, sticky='ew')

    root.mainloop()
