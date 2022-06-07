import tkinter as tk
import requests
import json
import pymysql
from sshtunnel import SSHTunnelForwarder

order_no = None
risk_loan_level = ['LEVEL_ONE', 'LEVEL_TWO', 'LEVEL_THREE']
user_level = ['L-0', 'L-1']

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


def aes_encrypt():
    """AES加密"""
    print(order_no.get(), order_no.get(), risk_loan_level_var.get(), user_level_var.get(), order_no.get())
    url = 'http://tool.chacuo.net/cryptaes/'
    data = {
        # 'data': '{"code":0,"data":{"code":200,"feature_list":[],"forbidApplyUntil":1647746861000,"loan_type":0,"order_no":"%s","partner_id":9000,"passed":"false","risk_amount":"0","risk_loan_level":"%s","sign":"4e32c73dafe476209843fd916a5cccb0","user_idcard":"1141210809980028","user_level":"%s","user_name":"twenty seven","user_phone":"82112341028","zeus_order_no":"%s"},"msg":""}' % (
            # order_no.get(), risk_loan_level_var.get(), user_level_var.get(), order_no.get()),
        'data': {"code":0,"data":{"code":200,"feature_list":[],"forbidApplyUntil":1647746861000,"loan_type":0,"order_no":"275765552729264","partner_id":9000,"passed":"false","risk_amount":"0","risk_loan_level":"LEVEL_ONE","sign":"4e32c73dafe476209843fd916a5cccb0","user_idcard":"1141210809980028","user_level":"L-0","user_name":"twenty seven","user_phone":"82112341028","zeus_order_no":"275765552729264"},"msg":""},
        'type': 'aes',
        'arg': 'm=cbc_pad=pkcs5_block=128_p=uaRZnvZoJZ8KSTuE_i=IFwDpMo01xY05ovH_o=0_s=gb2312_t=0'
    }
    # show_lb['text'] = data
    print(data)
    result = requests.post(url, data)
    print(result)
    html = result.text
    print(html)
    # encrypt_date = json.loads(html)['data']
    # print(encrypt_date)
    # show_lb['text'] = encrypt_date
    # return encrypt_date


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


def modify_machine_status():
    """修改机审状态"""
    ssh_sever = SSHTunnelForwarder(
        ('jump-sz1.toolscash.top', 22201),
        ssh_password='rOub8bWwc3mxhpjj',
        ssh_username='xiaohao',
        remote_bind_address=('149.129.214.137', 3306)
    )
    ssh_sever.start()
    db = pymysql.connect(
        host='127.0.0.1',
        port=ssh_sever.local_bind_port,
        user='uatas',
        password='c8CMsFW7pHmpjRss',
        db='cash_order',
        charset='utf8'
    )
    cursor = db.cursor()
    sql = 'select version();'
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    show_lb['text'] = data
    db.close()
    ssh_sever.close()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('uatas tool')

    frame01 = tk.Frame(master=root)
    frame01.pack()
    # 订单号标签
    order_no_label = tk.Label(frame01, text='order_no')
    order_no_label.pack(side='left')
    # 输入订单号
    order_no = tk.StringVar(frame01)
    order_no_entry = tk.Entry(frame01, text=order_no)
    order_no_entry.pack(side='left')
    # 系统选择

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
    control_callback_bt = tk.Button(frame02, text='模拟cloudun回调', command=aes_encrypt)
    control_callback_bt.pack(side='left')

    frame03 = tk.Frame(master=root)
    frame03.pack()
    # 订单状态改为过机审
    machine_status_bt = tk.Button(frame03, text='订单过机审', command=modify_machine_status)
    machine_status_bt.pack(side='left')
    # 订单改为待重新放款

    # 订单逾期

    # 根据uid查询在storage哪个表

    # 放款拉取
    # 还款拉取

    frame_show = tk.Frame(master=root)
    frame_show.pack()
    # 展示标签
    show_lb = tk.Label(frame_show, text='show', wraplength=800)
    show_lb.pack(side='left')

    root.mainloop()
