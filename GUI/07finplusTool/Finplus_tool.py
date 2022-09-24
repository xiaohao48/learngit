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
    'db': 'test',
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
"""脚本列表"""
scripts = {
    '展期生成新订单': 'php /home/rong/www/time-core/webroot/batch.php push VirtualOrderNotify',
    'uatas放款拉取': "php /home/rong/www/time-pay/webroot/batch.php TimePayLoan PollingLoanResult --payHandel='UP'",
    'uatas还款拉取': "php /home/rong/www/time-pay/webroot/batch.php TimePayRepay PollingRepayResult --orderNo='' --payHandel='UP'",
    "uatas入贷后": "php /home/rong/www/time-cuishou/webroot/batch.php Daihouivr GetDaihouIvr --day=",
    "uatas逾期费": "php /home/rong/www/time-core/webroot/batch.php FqRepayment CalDayFee --loanId=",
    "uatas入催收": "php /home/rong/www/time-core/webroot/batch.php RepayPlanTask IncuiShouTask",
    "用户storage目录查询": 'php -r "echo crc32() % 10;"',
    "uatas api绑定银行卡": "php /home/rong/www/time-order/webroot/command.php Customer ConsumeBankCard",
    "oppo打包放款": "php /home/rong/UatasPay/yii batch-disbursement/batch-loan",
    "贷后自动分单": "php /home/rong/www/time-cuishou/webroot/batch.php Daihouivr AssignDaihouTask --mid=10",
    "催收自动分单": "php /home/rong/www/time-cuishou/webroot/batch.php cuishou AssignCuishouTask --mid=10",
    "贷后任务扭转": "php /home/rong/www/time-cuishou/webroot/batch.php Daihouivr Sds",
    "催收任务扭转": "php /home/rong/www/time-cuishou/webroot/batch.php cuishou Sds",
}
encrypt_dict = {
    'zeus前端加密': {'key': 'Ckgx3U1QufHbcQns', 'iv': 'so8RhHi4jkaci4ze', 'way': 1},
    'zeus前端解密': {'key': 'Ckgx3U1QufHbcQns', 'iv': 'so8RhHi4jkaci4ze', 'way': 2},
    'zeus后端加密': {'key': '93LJ7sxQALXuMgLj', 'iv': 'jlsfjiosmhosl5db', 'way': 1},
    'zeus后端解密': {'key': '93LJ7sxQALXuMgLj', 'iv': 'jlsfjiosmhosl5db', 'way': 2},
    'uatas前端加密': {'key': 'daDtbXYkhhnHi1XF', 'iv': 'H9Rlows19wkBSx3w', 'way': 1},
    'uatas前端解密': {'key': 'daDtbXYkhhnHi1XF', 'iv': 'H9Rlows19wkBSx3w', 'way': 2},
    'uatas后端加密': {'key': 'z1aXNVB4JJw4ZZ0r', 'iv': 'LzsCmdfFbAvQ1fbD', 'way': 1},
    'uatas后端解密': {'key': 'z1aXNVB4JJw4ZZ0r', 'iv': 'LzsCmdfFbAvQ1fbD', 'way': 2}
}
rc_request_dict = {
    "测试Uatas请求风控": [
        "http://test-rc.uatas.id/rc/check", '{"data": "{\\\"order_no\\\": \\\"276688849607429\\\" }"}'
    ],
    "正式Uatas请求风控": [
        "http://rc.uatas.id/rc/check", '{"data":{"order_no":"276688849607429"}}'
    ],
    "测试UatasFly请求风控": [
        "https://test-rc.modalandalan.site/rc/check", '{"data":{"order_no":"276688849607429"}}'
    ],
    "正式UatasFly请求风控": [
        "http://rc.modalandalan.site/rc/check", '{"data":{"order_no":"276688849607429"}}'
    ],
    "测试finplus请求风控": [
        "http://test-rc.finplusid.com/rc/check", '{"data": "{\\\"order_no\\\": \\\"276688849607429\\\" }"}'
    ],
    "正式finplus请求风控": [
        "https://rc.finplus.id/rc/check", '{"data":{"order_no":"276688849607429"}}'
    ],
    "测试uatas设备信息": [
        "http://test-api.uatas.id/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'
    ],
    "正式uatas设备信息": [
        "http://api.uatas.id/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'
    ],
    "测试uatasfly设备信息": [
        "http://test-api.modalandalan.site/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'
    ],
    "正式uatasfly设备信息": [
        "http://api.modalandalan.site/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'
    ],
    "测试finplus设备信息": [
        "http://test-api.finplusid.com/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'
    ],
    "正式finplus设备信息": [
        "http://api.finplus.id/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'
    ],
    "moneypay放款": [
        "http://sandbox-pay.moneypaynow.com/sand-box/notify",
        '{"order_type":"loan","order_no":"22072313395637251675","order_status":1,"e_msg":""}'
    ],
    "moneypay还款": [
        "http://sandbox-pay.moneypaynow.com/sand-box/notify",
        '{"order_type":"repay","order_no":"22072313395637251675","order_status":1,"e_msg":""}'
    ],
    "monetapay还款": [
        "http://sandbox-api.monetapay.net/simulation/payForVa",
        '{"mch_id":100018,"order_no":22072313284035627786,"amount":1095000}'
    ]
}
system = {
    "uatas": "http://test-api.uatas.id",
    "uatasfly": "http://test-api.modalandalan.site",
    "finplus": "https://rc.finplus.id"
}
rc_url_list = {
    "check": "/rc/check",
    "getdeviceinfo": "/api/thirdapi/getdeviceinfo"
}


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
    if len(order_no.get()) == 15:
        password = aes_key_iv['uatas_rc']['key']
        iv = aes_key_iv['uatas_rc']['iv']
        way = 1
        text = "{\"code\":0,\"data\":{\"code\":200,\"feature_list\":[{\"featureValue\":500.0,\"featureName\":\"model_fst_score_v2_s7\",\"featureType\":\"number\"},{\"featureValue\":426.0,\"featureName\":\"model_fst_score_v2_s6\",\"featureType\":\"number\"}],\"forbidApplyUntil\":1647746861000,\"loan_type\":0," \
               "\"order_no\":\"%s\",\"partner_id\":9000,\"passed\":\"false\",\"risk_amount\":\"0\",\"risk_loan_level\":\"%s\"," \
               "\"sign\":\"4e32c73dafe476209843fd916a5cccb0\",\"user_idcard\":\"1141210809980028\",\"user_level\":\"%s\"," \
               "\"user_name\":\"twenty seven\",\"user_phone\":\"82112341028\",\"zeus_order_no\":\"%s\"},\"msg\":\"\"}" \
               % (order_no.get(), risk_loan_level_var.get(), user_level_var.get(), order_no.get())
        aes = aes_encrypt(url_crypt, password, iv, way, text)
        return aes
    else:
        show_lb['text'] = '请输入订单号'


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
    if len(order_no.get()) == 15:
        url = 'http://test-rc.uatas.id/rc/decisions/cloudun'
        data = json.dumps({"data": "%s" % (aes_rc())})
        try:
            result = requests.post(url, data, proxies=proxies)
            html = result.text
            show_lb['text'] = f'{html} {order_no.get()}回调成功'
        except:
            show_lb['text'] = f'{order_no.get()}模拟cloudun风控回调失败'
    else:
        show_lb['text'] = '请输入订单号'


def control_request():
    """订单请求风控"""
    if len(order_no.get()) == 15:
        # sql = f'UPDATE cash_order.orders as o SET o.create_time=FROM_UNIXTIME(UNIX_TIMESTAMP(o.create_time)-3600) ' \
        #       f'WHERE o.order_no={order_no.get()};'
        # mysql_modify(mysql_connect(), sql)
        #
        # # time.sleep(2)
        # ssh_sever_end()
        url = 'http://test-rc.uatas.id/rc/check'
        data = {'data': '{"order_no": "%s" }' % order_no.get()}
        print(data)
        try:
            result = requests.post(url, data)
            html = result.text
            show_lb['text'] = html
        except:
            show_lb['text'] = f'{order_no.get()}请求风控失败'
    else:
        show_lb['text'] = '请输入订单号'


def ssh_sever_start():
    """跳板服务开启"""
    global ssh_sever
    ssh_sever = SSHTunnelForwarder(
        ('jump-sz1.toolscash.top', 22202),
        ssh_password='jqeVwuIdoc27bkcg',
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
    if len(order_no.get()) == 15:
        db = mysql_connect()
        sql = f'SELECT o.order_no,o.`status` FROM cash_order.orders as o WHERE o.order_no ={order_no.get()};'
        mysql_select(db, sql)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def modify_machine_status():
    """修改机审状态"""
    if len(order_no.get()) == 15:
        db = mysql_connect()
        sqls = [
            f'UPDATE cash_order.orders as o SET o.status=45 WHERE o.order_no={order_no.get()};',
            f'UPDATE cash_approve.approve as a SET a.machine_status=1 WHERE a.order_no={order_no.get()};'
        ]
        for sql in sqls:
            mysql_modify(db, sql)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def order_change_reloan():
    """修改订单状态未待重新放款"""
    if len(order_no.get()) == 15:
        db = mysql_connect()
        sqls = [
            f'UPDATE cash_order.orders as o SET o.`status`=85 WHERE o.order_no={order_no.get()};',
            f'UPDATE cash_core.loan as l SET l.`status`=3 WHERE l.order_No={order_no.get()};',
            f'UPDATE cash_core.pay_record_log as g SET g.order_status=3 WHERE g.loan_id in '
            f'(SELECT l.id FROM cash_core.loan as l WHERE l.order_No={order_no.get()});',
            f'UPDATE cash_pay.timepay_loan_order as p SET p.`status`=3 WHERE p.loan_no ={order_no.get()};'
        ]
        for sql in sqls:
            mysql_modify(db, sql)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def order_overdue_sql1():
    """向前修改到期日(逾期)"""
    if len(order_no.get()) == 15 and len(overduedays_var.get()) > 0:
        db = mysql_connect()
        sqls = [
            f'DELETE FROM `cash_core`.`day_order_acc` WHERE `loan_id` in (select id from cash_core.`loan` '
            f'where order_No ={order_no.get()});',
            f'UPDATE cash_core.`loan` SET loan_time =loan_time-86400*{overduedays_var.get()} where order_No={order_no.get()};',
            f'UPDATE cash_core.repayment_plan_detail SET  due_time=due_time-86400*{overduedays_var.get()} where loan_id in '
            f'(select id from cash_core.`loan` where order_No = {order_no.get()});',
            f'UPDATE cash_order.orders as o SET o.loan_time=o.loan_time-86400*{overduedays_var.get()} WHERE o.order_no={order_no.get()};'
        ]
        for sql in sqls:
            mysql_modify(db, sql)
        select_sql = f'select id from cash_core.`loan` where order_No = {order_no.get()};'
        mysql_select(db, select_sql)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def order_overdue_sql2():
    """向后修改到期日"""
    if len(order_no.get()) == 15 and len(overduedays_var.get()) > 0:
        db = mysql_connect()
        sqls = [
            f'DELETE FROM `cash_core`.`day_order_acc` WHERE `loan_id` in (select id from cash_core.`loan` '
            f'where order_No ={order_no.get()});',
            f'UPDATE cash_core.`loan` SET loan_time =loan_time+86400*{overduedays_var.get()} where order_No={order_no.get()};',
            f'UPDATE cash_core.repayment_plan_detail SET  due_time=due_time+86400*{overduedays_var.get()} where loan_id in '
            f'(select id from cash_core.`loan` where order_No = {order_no.get()});',
            f'UPDATE cash_order.orders as o SET o.loan_time=o.loan_time+86400*{overduedays_var.get()} WHERE o.order_no={order_no.get()};'
        ]
        for sql in sqls:
            mysql_modify(db, sql)
        select_sql = f'select id from cash_core.`loan` where order_No = {order_no.get()};'
        mysql_select(db, select_sql)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


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
    scripts['uatas还款拉取'] = f"php /home/rong/www/time-pay/webroot/batch.php TimePayRepay PollingRepayResult " \
                           f"--orderNo='{order_no_entry.get()}' --payHandel='UP'"
    scripts["用户storage目录查询"] = f'php -r "echo crc32({order_no_entry.get()}) % 10;"'
    if script_var.get() in scripts.keys():
        show_lb['text'] = scripts[script_var.get()]
    else:
        show_lb['text'] = '输入错误'


def view_request_parameters():
    """查看请求参数"""
    if rc_op_var.get() in rc_request_dict.keys():
        data_encrypt_text.delete(1.0, tk.END)
        data_encrypt_text.insert(tk.INSERT, rc_request_dict[rc_op_var.get()][1])


def request_interface():
    """请求接口"""
    url = rc_request_dict[rc_op_var.get()][0]
    data=data_encrypt_text.get(1.0, tk.END)
    data_dic = json.loads(data)
    # ssh_sever_end()
    # url = 'http://test-rc.uatas.id/rc/check'
    # data = {'data': '{"order_no": "%s" }' % order_no.get()}
    print(url, data,data_dic)
    try:
        result = requests.post(url, data_dic)
        html = result.text
        show_lb['text'] = html
    except:
        show_lb['text'] = '请求接口失败'


def check_oppo_order():
    db = mysql_connect()
    sql = f'SELECT l.partner_loan_id,l.`status`,FROM_UNIXTIME(l.create_time) FROM cash_partner_pay.loan as l WHERE ' \
          f'l.partner_loan_id in ({data_encrypt_text.get(1.0, tk.END)});'
    mysql_select(db, sql)
    ssh_sever_end()


def modify_oppo_order():
    db = mysql_connect()
    sql = f'UPDATE cash_partner_pay.loan as l SET l.create_time=UNIX_TIMESTAMP(NOW())-86400*3 ' \
          f'WHERE l.partner_loan_id in ({data_encrypt_text.get(1.0, tk.END)});'
    mysql_modify(db, sql)
    ssh_sever_end()


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

    """修改订单到期日"""
    row = row + 1
    modify_duedays_lb = tk.Label(root, text='到期日向前/向后移动()天')
    modify_duedays_lb.grid(row=row, column=column + 1)
    overduedays_var = tk.StringVar()
    overdueday_entry = tk.Entry(root, text=overduedays_var)
    overdueday_entry.grid(row=row, column=column + 2, sticky='ew')
    # 订单逾期sql
    order_overdue_bt = create_button(root, text='向前修改到期日(逾期)', command=order_overdue_sql1, row=row, column=column + 3)
    order_overdue_bt = create_button(root, text='向后修改到期日', command=order_overdue_sql2, row=row, column=column + 4)

    """oppo订单查看修改"""
    row = row + 1
    create_button(root, text='查看oppo订单信息', command=check_oppo_order, row=row, column=column + 1)
    create_button(root, text='修改oppo订单创建时间', command=modify_oppo_order, row=row, column=column + 2)

    """加解密输入行"""
    row = row + 1
    data_encrypt_text = tk.Text(root, width=120, height=4)
    data_encrypt_text.grid(row=row, column=column, columnspan=5)

    """加解密行"""
    row = row + 1
    encrypt_lb = tk.Label(root, text='待加解密数据↑')
    encrypt_lb.grid(row=row, column=column + 1)
    encrypt_var = tk.StringVar(value="请选择加解密方式")
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

    """模拟风控请求"""
    row += 1
    rc_op_var = tk.StringVar(value="选择请求")
    rc_op = tk.OptionMenu(root, rc_op_var, *rc_request_dict.keys())
    rc_op.grid(row=row, column=column + 1, sticky='ew')
    check_bt = create_button(root, text='查看请求参数', command=view_request_parameters, row=row, column=column + 2)
    request_interface_bt = create_button(root, text='请求接口', command=request_interface, row=row, column=column + 3)

    """展示行"""
    row = row + 1
    show_lb = tk.Label(root, text='show', wraplength=800, background='green')
    show_lb.grid(row=row, column=column + 1, columnspan=5, sticky='ew')

    root.mainloop()
