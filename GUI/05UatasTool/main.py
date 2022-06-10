import tkinter as tk
import requests
import json
import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko

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
    "http": 'http://127.0.0.1:1080'
    # "https": 'https://vhk.toolscash.top:52999'
}


def aes_encrypt():
    """AES加密"""
    url = 'https://tool.lmeee.com/jiami/crypt128inter'
    data = {
        "mode": "CBC",
        "padding": "pkcs5",
        "block": 128,
        "password": "uaRZnvZoJZ8KSTuE",
        "iv": "IFwDpMo01xY05ovH",
        "encode": "base64",
        "way": 1,
        "text": "{\"code\":0,\"data\":{\"code\":200,\"feature_list\":[],\"forbidApplyUntil\":1647746861000,\"loan_type\":0,\"order_no\":\"%s\",\"partner_id\":9000,\"passed\":\"false\",\"risk_amount\":\"0\",\"risk_loan_level\":\"%s\",\"sign\":\"4e32c73dafe476209843fd916a5cccb0\",\"user_idcard\":\"1141210809980028\",\"user_level\":\"%s\",\"user_name\":\"twenty seven\",\"user_phone\":\"82112341028\",\"zeus_order_no\":\"%s\"},\"msg\":\"\"}"%(order_no.get(),risk_loan_level_var.get(),user_level_var.get(),order_no.get()),
        "method": "aes"
    }
    try:
        result = requests.post(url=url, data=data)
        html = result.text
        encrypt_date = json.loads(html)['d']['r']
        show_lb['text'] = encrypt_date
        return encrypt_date
    except:
        show_lb['text'] = f'{order_no.get()}加密失败'


def mock_cloudun_callback():
    """模拟cloudun风控回调"""
    url = 'http://test-rc.uatas.id/rc/decisions/cloudun'
    data = {'data': "%s" % (aes_encrypt())}
    # show_lb['text'] = data
    print(data)
    # result = requests.post(url, data)
    # html = result.text
    # print(html)


def control_request():
    """订单请求风控"""
    url = 'http://test-rc.uatas.id/rc/check'
    data = {'data': '{"order_no": "%s" }' % order_no.get()}
    show_lb['text'] = data
    # result = requests.post(url, data)
    # html = result.text
    # print(html)


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
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='jump-sz1.toolscash.top', port=22203, username='xiaohao', password='rOub8bWwc3mxhpjj')
    stdin, stdout, stderr = client.exec_command('df -h')
    print(stdout.read().decode('utf-8'))
    client.close()


def clear_data():
    order_no.set(value='')
    show_lb['text'] = '已清空'


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
    aes_encrypt_bt = tk.Button(frame02, text='AES加密', command=aes_encrypt)
    aes_encrypt_bt.pack(side='left')
    control_callback_bt = tk.Button(frame02, text='模拟cloudun回调', command=control_request)
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

    frame_show = tk.Frame(master=root)
    frame_show.pack()
    # 展示标签
    show_lb = tk.Label(frame_show, text='show', wraplength=800)
    show_lb.pack(side='left')

    root.mainloop()
