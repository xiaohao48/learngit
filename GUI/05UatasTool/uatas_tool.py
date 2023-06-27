import ast
import tkinter as tk
import requests
import json
import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko
import pyperclip
# import sys
import time
# from requests.auth import HTTPBasicAuth
import base64

risk_loan_level = ['LEVEL_ONE', 'LEVEL_TWO', 'LEVEL_THREE']
user_level = ['L-0', 'L-1']
system = ['uatas', 'finplus', 'uatasfly']
url_crypt = 'https://tool.lmeee.com/jiami/crypt128inter'
# 代理
proxies = {
    "http": None,
    "https": None
}
# 加解密key
aes_key_iv = {
    "uatas": {"key": "uaRZnvZoJZ8KSTuE", "iv": "IFwDpMo01xY05ovH"},  # uatas风控
    "uatasfly": {"key": "uaRZnvZoJZ8KSTuE", "iv": "IFwDpMo01xY05ovH"},  # uatasfly风控
    "finplus": {"key": "tdRFVNCrVI7hS1tk", "iv": "aT5in1s04xTbb8i6"},  # finplus风控
    # "front_end_zeus": {"key": "Ckgx3U1QufHbcQns", "iv": "so8RhHi4jkaci4ze"},  # zeus前端
    # "back_end_zeus": {"key": "93LJ7sxQALXuMgLj", "iv": "jlsfjiosmhosl5db"},  # zeus后台
    # "front_end_uatas": {"key": "daDtbXYkhhnHi1XF", "iv": "H9Rlows19wkBSx3w"},  # uatas前端
    # "back_end_uatas": {"key": "z1aXNVB4JJw4ZZ0r", "iv": "LzsCmdfFbAvQ1fbD"}  # uatas后台
}
# 脚本列表
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
# 前后端加解密key
encrypt_dict = {
    # 'zeus前端加密': {'key': 'Ckgx3U1QufHbcQns', 'iv': 'so8RhHi4jkaci4ze', 'way': 1},
    # 'zeus前端解密': {'key': 'Ckgx3U1QufHbcQns', 'iv': 'so8RhHi4jkaci4ze', 'way': 2},
    # 'zeus后端加密': {'key': '93LJ7sxQALXuMgLj', 'iv': 'jlsfjiosmhosl5db', 'way': 1},
    # 'zeus后端解密': {'key': '93LJ7sxQALXuMgLj', 'iv': 'jlsfjiosmhosl5db', 'way': 2},
    'uatas前端加密': {'key': 'daDtbXYkhhnHi1XF', 'iv': 'H9Rlows19wkBSx3w', 'way': 1},
    'uatas前端解密': {'key': 'daDtbXYkhhnHi1XF', 'iv': 'H9Rlows19wkBSx3w', 'way': 2},
    'uatas后端加密': {'key': 'z1aXNVB4JJw4ZZ0r', 'iv': 'LzsCmdfFbAvQ1fbD', 'way': 1},
    'uatas后端解密': {'key': 'z1aXNVB4JJw4ZZ0r', 'iv': 'LzsCmdfFbAvQ1fbD', 'way': 2}
}
# post请求列表
request_list = {
    "uatas": ["http://test-rc.uatas.id", "http://test-api.uatas.id"],
    "uatasfly": ["https://test-rc.modalandalan.site", "http://test-api.modalandalan.site"],
    "finplus": ["http://test-rc.finplusid.com", "http://test-api.finplusid.com"],
}
rc_request_dict = {
    "请求风控": ["/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    "设备信息": [
        "/api/thirdapi/getdeviceinfo",
        '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    # "测试uatas请求风控": ["http://test-rc.uatas.id/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    # "正式uatas请求风控": ["http://rc.uatas.id/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    # "测试uatasfly请求风控": ["https://test-rc.modalandalan.site/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    # "正式uatasFly请求风控": ["http://rc.modalandalan.site/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    # "测试finplus请求风控": ["http://test-rc.finplusid.com/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    # "正式finplus请求风控": ["https://rc.finplus.id/rc/check", {"data": "{\"order_no\": \"276688849607429\" }"}],
    # "测试uatas设备信息": [
    # "http://test-api.uatas.id/api/thirdapi/getdeviceinfo",
    # '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    # "正式uatas设备信息": ["http://api.uatas.id/api/thirdapi/getdeviceinfo",
    # '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    # "测试uatasfly设备信息": [
    # "http://test-api.modalandalan.site/api/thirdapi/getdeviceinfo",
    # '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    # "正式uatasfly设备信息": ["http://api.modalandalan.site/api/thirdapi/getdeviceinfo",
    #                    '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    # "测试finplus设备信息": [
    # "http://test-api.finplusid.com/api/thirdapi/getdeviceinfo",
    # '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    # "正式finplus设备信息": ["http://api.finplus.id/api/thirdapi/getdeviceinfo",
    #                   '{"order_no":276688745040269,"sign":"7afb01aeb248529dc2d0816bbfe68adb","timestamp":1660132508,"type":2}'],
    "moneypay放款": ["http://sandbox-pay.moneypaynow.com/sand-box/notify",
                     '{"order_type":"loan","order_no":"22072313395637251675","order_status":1,"e_msg":""}'],
    "moneypay还款": ["http://sandbox-pay.moneypaynow.com/sand-box/notify",
                     '{"order_type":"repay","order_no":"22072313395637251675","order_status":1,"e_msg":""}'],
    "monetapay还款": ["http://sandbox-api.monetapay.net/simulation/payForVa",
                      '{"mch_id":100018,"order_no":22072313284035627786,"amount":1095000}'],
    "instamoney bank还款": [
        'https://api.instamoney.co/p2p-escrow-virtual-accounts/testing-payments',
        '{"external_id": "846ba2bc_03c6331a434acd5b","amount": "1683490.00"}',
        'sk_test_a4pgdm8dBr5xJvGDYpC0JTxC1sq530nmSnknXco1nb94ADrEGEqtfE0JkBa5Zz0',  # Username
        'ZHNhZHNhY3N4Y1pjYXM'  # Password
    ],
    "instamoney OTC还款": [
        'https://api.instamoney.co/fixed_payment_code/simulate_payment',
        '{"retail_outlet_name":"ALFAMART","payment_code":"TEST817586","transfer_amount":684356}',
        'sk_test_YYiLRZXuKQd6PsshmdIOXdpIHXqwf2QWNR09mK7JWLPqL2vzSh1QIu0eR0vURg2',  # Username
        '0ef77229ae1a4aba2e97bb5881660941724ec3ae8858ce287b879452544313c4'  # Password
    ],
    "cloudun_AES加密": [
        "https://tool.lmeee.com/jiami/crypt128inter",
        """{'mode': 'CBC',
        'padding': 'pkcs5',
        'block': '128',
        'password': 'uaRZnvZoJZ8KSTuE',
        'iv': 'IFwDpMo01xY05ovH',
        'encode': 'base64',
        'way': '1',
        'text': '{"code":0,"data":{"code":200,"feature_list":[{"featureValue":334.0,"featureName":"model_reb_score_v2_s2","featureType":"number"}],"forbidApplyUntil":1647746861000,"loan_type":0,"order_no":"274540645167919","partner_id":9000,"passed":"false","risk_amount":"0","risk_loan_level":"LEVEL_THREE","sign":"4e32c73dafe476209843fd916a5cccb0","user_idcard":"1141210809980028","user_level":"L-1","user_name":"twentyseven","user_phone":"82112341028","zeus_order_no":"274540645167919"},"msg":""}',
        'method': 'aes'}"""
    ],
    "plan_AES加密": [
        "https://tool.lmeee.com/jiami/crypt128inter",
        """{'mode': 'CBC',
        'padding': 'pkcs5',
        'block': '128',
        'password': 'uaRZnvZoJZ8KSTuE',
        'iv': 'IFwDpMo01xY05ovH',
        'encode': 'base64',
        'way': '1',
        'text': '{"code":0,"data":{"error_code":0,"is_defer":0,"model_id":"a6_new_v6","model_indicators":{},"model_offset":0,"model_per":"0.5000","order_no":"279551347234503","rule_name":"","score":460,"strategy_id":"uatas_super_20220409","uatas_new_user":1}}',
        'method': 'aes'}"""
    ],
    "cloudun模拟回调": ["/rc/decisions/cloudun", '{"data":""}'],
    "plan模拟回调": ["/rc/decisions/plan", '{"data":""}']

}
# 数据库账号密码
db_mysql = {
    "uatas": ["119.8.114.69", "uatas", "c8CMsFW7pHmpjRss", 9702],
    "uatasfly": ["159.138.99.17", "test-uatas_xiaohao", "NegYtW1rljEv", 3306],
    "finplus": ["149.129.255.222", "root", "3c07bcf6a961c032", 3306],
}


def data_encrypt(system_choose, data_crypt):
    """业务加解密功能"""
    if system_choose in encrypt_dict.keys():
        data = aes_encrypt(
            url=url_crypt,
            password=encrypt_dict[system_choose]['key'],
            iv=encrypt_dict[system_choose]['iv'],
            way=encrypt_dict[system_choose]['way'],
            text=data_crypt
        )
        show_lb['text'] = data
    else:
        show_lb['text'] = '加解密失败'


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
        show_lb['text'] = f'加解密失败'


def aes_rc(order_no, system_choose, loan_level, user_level):
    """cloudun回调数据aes加密"""
    if len(order_no) == 15:
        password = aes_key_iv[system_choose]['key']
        iv = aes_key_iv[system_choose]['iv']
        way = 1
        text = "{\"code\":0,\"data\":{\"code\":200,\"feature_list\":[{\"featureValue\":500.0,\"featureName\":" \
               "\"model_fst_score_v2_s7\",\"featureType\":\"number\"},{\"featureValue\":426.0,\"featureName\":" \
               "\"model_fst_score_v2_s6\",\"featureType\":\"number\"}],\"forbidApplyUntil\":1647746861000,\"loan_type\":0," \
               "\"order_no\":\"%s\",\"partner_id\":9000,\"passed\":\"false\",\"risk_amount\":\"0\",\"risk_loan_level\":\"%s\"," \
               "\"sign\":\"4e32c73dafe476209843fd916a5cccb0\",\"user_idcard\":\"1141210809980028\",\"user_level\":\"%s\"," \
               "\"user_name\":\"twenty seven\",\"user_phone\":\"82112341028\",\"zeus_order_no\":\"%s\"},\"msg\":\"\"}" \
               % (order_no, loan_level, user_level, order_no)
        aes = aes_encrypt(url_crypt, password, iv, way, text)
        return aes
    else:
        show_lb['text'] = '请输入订单号'


def mock_cloudun_callback(order_no, system_choose, loan_level, user_level):
    """模拟cloudun风控回调"""
    if len(order_no) == 15:
        url = request_list[system_choose][0] + '/rc/decisions/cloudun'
        data = json.dumps({"data": "%s" % (aes_rc(order_no, system_choose, loan_level, user_level))})
        try:
            result = requests.post(url, data, proxies=proxies)
            html = result.text
            show_lb['text'] = f'{html} {order_no}回调成功'
        except:
            show_lb['text'] = f'{order_no}模拟cloudun风控回调失败'
    else:
        show_lb['text'] = '请输入订单号'


def modify_order_ctime(order_no, system_choose):
    """修改订单创建时间"""
    if len(order_no) == 15:
        db = mysql_connect(system_choose)
        sql = f'UPDATE cash_order.orders as o SET o.create_time=FROM_UNIXTIME(UNIX_TIMESTAMP(o.create_time)-3600) ' \
              f'WHERE o.order_no={order_no};'
        mysql_modify(db, sql, order_no)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def control_request(order_no):
    """订单请求风控"""
    if len(order_no) == 15:
        # sql = f'UPDATE cash_order.orders as o SET o.create_time=FROM_UNIXTIME(UNIX_TIMESTAMP(o.create_time)-3600) ' \
        #       f'WHERE o.order_no={order_no.get()};'
        # mysql_modify(mysql_connect(), sql)
        #
        # # time.sleep(2)
        # ssh_sever_end()
        url = 'http://test-rc.uatas.id/rc/check'
        data = {'data': '{"order_no": "%s" }' % order_no}
        try:
            result = requests.post(url, data)
            html = result.text
            show_lb['text'] = html
        except:
            show_lb['text'] = f'{order_no}请求风控失败'
    else:
        show_lb['text'] = '请输入订单号'


def ssh_sever_start(system_choose):
    """跳板服务开启"""
    global ssh_sever
    ssh_sever = SSHTunnelForwarder(
        ('jump-sz3.toolscash.top', 22202),
        ssh_password='jqeVwuIdoc27bkcg',
        ssh_username='xiaohao',
        remote_bind_address=(db_mysql[system_choose][0], 3306)
    )
    ssh_sever.start()


def ssh_sever_end():
    """跳板服务关闭"""
    db.close()
    ssh_sever.close()


def mysql_connect(system_choose):
    """数据库连接"""
    global db
    try:
        ssh_sever_start(system_choose)
        db = pymysql.connect(
            host='127.0.0.1',
            port=ssh_sever.local_bind_port,
            user=db_mysql[system_choose][1],
            password=db_mysql[system_choose][2],
            db='cash_order',
            charset='utf8'
        )
    except:
        db = pymysql.connect(
            host=db_mysql[system_choose][0],
            port=db_mysql[system_choose][3],
            user=db_mysql[system_choose][1],
            password=db_mysql[system_choose][2],
            db='cash_order',
            charset='utf8'
        )
    return db


def mysql_select(db, sql, order_no):
    """数据库查询操作"""
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        show_lb['text'] = result
        return result
    except:
        show_lb['text'] = f'{order_no}查询错误'


def mysql_modify(db, sql, order_no):
    """数据库更新操作"""
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        show_lb['text'] = f'{order_no}修改成功'
    except:
        db.rollback()
        show_lb['text'] = f'{order_no}修改失败'


def select_order(order_no, system_choose):
    """数据库订单状态查询"""
    if len(order_no) == 15:
        db = mysql_connect(system_choose)
        sql = f'SELECT * FROM cash_order.orders as o WHERE o.order_no ={order_no};'
        mysql_select(db, sql, order_no)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def modify_machine_status(order_no, system_choose):
    """修改机审状态"""
    if len(order_no) == 15:
        db = mysql_connect(system_choose)
        sqls = [
            f'UPDATE cash_order.orders as o SET o.status=45 WHERE o.order_no={order_no};',
            f'UPDATE cash_approve.approve as a SET a.machine_status=1 WHERE a.order_no={order_no};'
        ]
        for sql in sqls:
            mysql_modify(db, sql, order_no)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def order_change_reloan(order_no, system_choose):
    """修改订单状态未待重新放款"""
    if len(order_no) == 15:
        db = mysql_connect(system_choose)
        sqls = [
            f'UPDATE cash_order.orders as o SET o.`status`=85 WHERE o.order_no={order_no};',
            f'UPDATE cash_core.loan as l SET l.`status`=3 WHERE l.order_No={order_no};',
            f'UPDATE cash_core.pay_record_log as g SET g.order_status=3,g.msg="Invalid Destination" WHERE g.loan_id in '
            f'(SELECT l.id FROM cash_core.loan as l WHERE l.order_No={order_no});',
            f'UPDATE cash_pay.timepay_loan_order as p SET p.`status`=3 WHERE p.loan_no ={order_no};'
        ]
        for sql in sqls:
            mysql_modify(db, sql, order_no)
        ssh_sever_end()
    else:
        show_lb['text'] = '请输入订单号'


def order_overdue_sql1(order_no, system_choose, overdue_days):
    """向前修改到期日(逾期)"""
    if len(order_no) == 15 and len(overdue_days) > 0:
        db = mysql_connect(system_choose)
        sqls = [
            f'DELETE FROM `cash_core`.`day_order_acc` WHERE `loan_id` in (select id from cash_core.`loan` '
            f'where order_No ={order_no});',
            f'UPDATE cash_core.`loan` SET loan_time =loan_time-86400*{overdue_days} where order_No={order_no};',
            f'UPDATE cash_core.repayment_plan_detail SET  due_time=due_time-86400*{overdue_days} where loan_id in '
            f'(select id from cash_core.`loan` where order_No = {order_no});',
            f'UPDATE cash_order.orders as o SET o.loan_time=o.loan_time-86400*{overdue_days} WHERE o.order_no={order_no};'
        ]
        for sql in sqls:
            mysql_modify(db, sql, order_no)
        select_sql = f'select id from cash_core.`loan` where order_No = {order_no};'
        loan_id = mysql_select(db, select_sql, order_no)
        ssh_sever_end()
        show_lb['text'] = f'订单已逾期{overdue_days}天，' \
                          f'php /home/rong/www/time-core/webroot/batch.php FqRepayment CalDayFee --loanId={loan_id}'
    else:
        show_lb['text'] = '请输入订单号'


def order_overdue_sql2(order_no, system_choose, overdue_days):
    """向后修改到期日"""
    if len(order_no) == 15 and len(overdue_days) > 0:
        db = mysql_connect(system_choose)
        sqls = [
            f'DELETE FROM `cash_core`.`day_order_acc` WHERE `loan_id` in (select id from cash_core.`loan` '
            f'where order_No ={order_no});',
            f'UPDATE cash_core.`loan` SET loan_time =loan_time+86400*{overdue_days} where order_No={order_no};',
            f'UPDATE cash_core.repayment_plan_detail SET  due_time=due_time+86400*{overdue_days} where loan_id in '
            f'(select id from cash_core.`loan` where order_No = {order_no});',
            f'UPDATE cash_order.orders as o SET o.loan_time=o.loan_time+86400*{overdue_days} WHERE o.order_no={order_no};'
        ]
        for sql in sqls:
            mysql_modify(db, sql, order_no)
        show_lb['text'] = f'订单已延期{overdue_days}天'
    else:
        show_lb['text'] = '请输入订单号'


def order_overdue_ssh():
    """脚本执行"""
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
    # command = 'df -h'
    # stdin, stdout, stderr = connection.exec_command(command)
    channel.close()
    connection.close()

    # trans = paramiko.Transport(('jump-sz1.toolscash.top', 22203))
    # # trans.start_client()
    # trans.auth_password(username='xiaohao', password='rOub8bWwc3mxhpjj')
    # channel = trans.open_session(11)
    # channel.get_pty()
    # a = channel.invoke_shell()
    #
    # channel.close()
    # trans.close()


def clear_data(order_no, data_encrypt):
    """清空功能"""
    order_no.set(value='')
    data_encrypt.delete(1.0, tk.END)
    show_lb['text'] = '已清空'


def copy():
    """复制功能"""
    return pyperclip.copy(show_lb['text'])


def create_button(master, text, command, row, column, width=30, sticky='ew'):
    """创建按钮功能"""
    new_button = tk.Button(master=master, text=text, command=command, width=width)
    new_button.grid(row=row, column=column, sticky=sticky)
    return new_button


def script(script_select, order_no):
    """查看脚本"""
    scripts['uatas还款拉取'] = f"php /home/rong/www/time-pay/webroot/batch.php TimePayRepay PollingRepayResult " \
                               f"--orderNo='{order_no}' --payHandel='UP'"
    scripts["用户storage目录查询"] = f'php -r "echo crc32({order_no}) % 10;"'
    if script_select in scripts.keys():
        show_lb['text'] = scripts[script_select]
    else:
        show_lb['text'] = '输入错误'


def view_request_parameters(request_choose, data_request):
    """查看请求参数"""
    if request_choose.get() in rc_request_dict.keys():
        data_request.delete(1.0, tk.END)
        data_request.insert(tk.INSERT, rc_request_dict[request_choose.get()][1])


def url_request(url, data, url_type, headers):
    """接口请求"""
    if url_type == 1:
        try:
            result = requests.post(url, data)
            html = result.text
            show_lb['text'] = html
        except:
            show_lb['text'] = '请求接口失败'
    elif url_type == 2:
        try:
            result = requests.post(url=url, data=data, proxies=proxies)
            html = result.text
            encrypt_date = json.loads(html)['d']['r']
            show_lb['text'] = encrypt_date
        except:
            show_lb['text'] = '请求接口失败'
    elif url_type == 3:
        try:
            result = requests.post(url, data, headers=headers, proxies=proxies)
            html = result.text
            show_lb['text'] = html
        except:
            show_lb['text'] = '请求接口失败'
    else:
        show_lb['text'] = '请求接口失败'


def request_interface(request_choose, order_no, data_request, system_choose):
    """请求接口按钮"""
    if request_choose in list(rc_request_dict.keys())[0:1] and len(order_no) == 15:
        """请求风控"""
        modify_order_ctime(order_no, system_choose)
        rc_request_dict[request_choose][1] = {'data': '{"order_no": "%s" }' % (order_no)}
        url = request_list[system_choose][0] + rc_request_dict[request_choose][0]
        data = rc_request_dict[request_choose][1]
        headers = ''
        url_type = 1
        url_request(url, data, url_type, headers)
    elif request_choose in list(rc_request_dict.keys())[1:2]:
        """设备信息"""
        url = request_list[system_choose][1] + rc_request_dict[request_choose][0]
        data = json.dumps(ast.literal_eval(data_request))
        headers = ''
        url_type = 1
        url_request(url, data, url_type, headers)
    elif request_choose in list(rc_request_dict.keys())[2:5]:
        """moneta放款还款"""
        url = rc_request_dict[request_choose][0]
        data = data_request
        headers = ''
        url_type = 1
        url_request(url, data, url_type, headers)
    elif request_choose in list(rc_request_dict.keys())[7:9]:
        """风控返回数据AES加密"""
        url = rc_request_dict[request_choose][0]
        data = ast.literal_eval(data_request)
        url_type = 2
        headers = ''
        url_request(url, data, url_type, headers)
    elif request_choose in list(rc_request_dict.keys())[5:7]:
        """instamoney还款"""
        url = rc_request_dict[request_choose][0]
        data = data_request
        auth = str(base64.b64encode(
            f"{rc_request_dict[request_choose][2]}:{rc_request_dict[request_choose][3]}".encode('utf-8')), 'utf-8')
        headers = {
            "Content-Type": "application/json",
            'Authorization': f'Basic {auth}',
        }
        url_type = 3
        url_request(url, data, url_type, headers)
    elif request_choose in list(rc_request_dict.keys())[9:11]:
        """模拟风控回调"""
        url = request_list[system_choose][0] + rc_request_dict[request_choose][0]
        data = json.dumps(ast.literal_eval(data_request))
        headers = ''
        url_type = 1
        url_request(url, data, url_type, headers)
    else:
        show_lb['text'] = '请求接口失败'


def check_oppo_order(order_no, system_choose):
    """查询oppo订单信息"""
    if system_choose == "uatas":
        db = mysql_connect(system_choose)
        sql = f'''SELECT l.partner_loan_id,l.`status`,FROM_UNIXTIME(l.create_time) FROM cash_partner_pay.loan as l 
        WHERE l.partner_loan_id in ({order_no});'''
        mysql_select(db, sql, order_no)
        ssh_sever_end()
    else:
        show_lb['text'] = '系统选择错误'


def modify_oppo_order(order_no, system_choose):
    """修改oppo订单信息"""
    if system_choose == "uatas":
        db = mysql_connect(system_choose)
        sql = f'UPDATE cash_partner_pay.loan as l SET l.create_time=UNIX_TIMESTAMP(NOW())-86400*3 ' \
              f'WHERE l.partner_loan_id in ({order_no});'
        mysql_modify(db, sql, order_no)
        ssh_sever_end()
    else:
        show_lb['text'] = '系统选择错误'


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('uatas tool')
    column = 0

    """第一行，参数行"""
    row = 0
    # 订单号标签
    order_no_label = tk.Label(root, text='order_no')
    order_no_label.grid(row=row, column=column + 1, sticky='ew')
    # 输入订单号
    order_no_var = tk.StringVar()
    order_no_entry = tk.Entry(root, text=order_no_var)
    order_no_entry.grid(row=row, column=column + 2, sticky='ew')
    # 系统选择
    system_var = tk.StringVar(value='uatas')
    system_op = tk.OptionMenu(root, system_var, *system)
    system_op.grid(row=row, column=column + 3, sticky='ew')

    """第二行，风控加解密"""
    row = row + 1
    # risk_loan_level选择
    risk_loan_level_var = tk.StringVar(value='LEVEL_ONE')
    risk_loan_level_op = tk.OptionMenu(root, risk_loan_level_var, *risk_loan_level)
    risk_loan_level_op.grid(row=row, column=column + 1, sticky='ew')
    # user_level选择
    user_level_var = tk.StringVar(value='L-0')
    user_level_op = tk.OptionMenu(root, user_level_var, *user_level)
    user_level_op.grid(row=row, column=column + 2, sticky='ew')
    # # 请求风控
    # control_request_bt = create_button(root, text='请求风控', command=control_request, row=row, column=column + 3)
    # 风控AES加密
    aes_encrypt_bt = create_button(root, text='风控AES加密',
                                   command=lambda: aes_rc(order_no_var.get(), system_var.get(),
                                                          risk_loan_level_var.get(), user_level_var.get()),
                                   row=row, column=column + 3)
    # 模拟cloudun回调
    control_callback_bt = create_button(root, text='模拟cloudun回调',
                                        command=lambda: mock_cloudun_callback(order_no_var.get(), system_var.get(),
                                                                              risk_loan_level_var.get(),
                                                                              user_level_var.get()),
                                        row=row, column=column + 4)

    """第三行，数据库查询修改"""
    row = row + 1
    # 订单信息查询
    select_order_bt = create_button(root, text='订单信息查询',
                                    command=lambda: select_order(order_no_var.get(), system_var.get()), row=row,
                                    column=column + 1)
    # 订单状态改为过机审
    machine_status_bt = create_button(root, text='订单过机审',
                                      command=lambda: modify_machine_status(order_no_var.get(), system_var.get()),
                                      row=row, column=column + 2)
    # 订单改为待重新放款
    reloan_bt = create_button(root, text='订单待重新放款',
                              command=lambda: order_change_reloan(order_no_var.get(), system_var.get()), row=row,
                              column=column + 3)

    """修改订单到期日"""
    row = row + 1
    # 逾期天数输入label
    modify_duedays_lb = tk.Label(root, text='到期日向前/向后移动()天')
    modify_duedays_lb.grid(row=row, column=column + 1)
    # 逾期天数输入entry
    overduedays_var = tk.StringVar()
    overdueday_entry = tk.Entry(root, text=overduedays_var)
    overdueday_entry.grid(row=row, column=column + 2, sticky='ew')
    # 订单逾期
    order_overdue_bt = create_button(root, text='向前修改到期日(逾期)',
                                     command=lambda: order_overdue_sql1(order_no_var.get(), system_var.get(),
                                                                        overduedays_var.get()), row=row,
                                     column=column + 3)
    # 订单延期
    order_overdue_bt = create_button(root, text='向后修改到期日',
                                     command=lambda: order_overdue_sql2(order_no_var.get(), system_var.get(),
                                                                        overduedays_var.get()), row=row,
                                     column=column + 4)

    """oppo订单查看修改"""
    row = row + 1
    create_button(root, text='查看oppo订单信息',
                  command=lambda: check_oppo_order(data_encrypt_text.get(1.0, tk.END), system_var.get()), row=row,
                  column=column + 1)
    create_button(root, text='修改oppo订单创建时间',
                  command=lambda: modify_oppo_order(data_encrypt_text.get(1.0, tk.END), system_var.get()), row=row,
                  column=column + 2)

    """加解密信息输入行"""
    row = row + 1
    data_encrypt_text = tk.Text(root, width=120, height=4)
    data_encrypt_text.grid(row=row, column=column, columnspan=5)

    """加解密行"""
    # 加解密label
    row = row + 1
    encrypt_lb = tk.Label(root, text='待加解密数据↑')
    encrypt_lb.grid(row=row, column=column + 1)
    # 加密方式
    encrypt_var = tk.StringVar(value="uatas后端解密")
    encrypt_op = tk.OptionMenu(root, encrypt_var, *encrypt_dict.keys())
    encrypt_op.grid(row=row, column=column + 2, sticky='ew')
    # 前后端加解密
    encrypt_bt = create_button(root, text='加解密',
                               command=lambda: data_encrypt(encrypt_var.get(), data_encrypt_text.get(1.0, tk.END)),
                               row=row, column=column + 3)

    """查看脚本"""
    row = row + 1
    # 脚本选择
    script_var = tk.StringVar(value='选择脚本')
    script_op = tk.OptionMenu(root, script_var, *scripts.keys())
    script_op.grid(row=row, column=column + 1, sticky='ew')
    # 查看脚本
    script_bt = create_button(master=root, text='查看脚本', row=row, column=column + 2,
                              command=lambda: script(script_var.get(), order_no_var.get()))
    # 复制按钮
    copy_bt = create_button(root, text='复制', command=copy, row=row, column=column + 3)
    # 清空按钮
    clear_bt = create_button(root, text='清空', command=lambda: clear_data(order_no_var, data_encrypt_text), row=row,
                             column=column + 4)

    """模拟请求"""
    row += 1
    # 请求选择
    req_op_var = tk.StringVar(value="请求风控")
    req_op = tk.OptionMenu(root, req_op_var, *rc_request_dict.keys())
    req_op.grid(row=row, column=column + 1, sticky='ew')
    # 查看请求参数
    check_bt = create_button(root, text='查看请求参数',
                             command=lambda: view_request_parameters(req_op_var, data_encrypt_text), row=row,
                             column=column + 2)
    # 请求接口
    request_interface_bt = create_button(root, text='请求接口',
                                         command=lambda: request_interface(req_op_var.get(), order_no_var.get(),
                                                                           data_encrypt_text.get(1.0, tk.END),
                                                                           system_var.get()),
                                         row=row, column=column + 3)

    """展示行"""
    row = row + 1
    show_lb = tk.Label(root, text='show', wraplength=800, background='green')
    show_lb.grid(row=row, column=column + 1, columnspan=5, sticky='ew')

    root.mainloop()
