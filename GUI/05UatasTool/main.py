import tkinter as tk
import requests
import json

order_no = None


def aes_encrypt(order_no):
    url = 'http://tool.chacuo.net/cryptaes/'
    data = {
        'data': '{"code":0,"data":{"code":200,"feature_list":[],"forbidApplyUntil":1647746861000,"loan_type":0,"order_no":{order_no},"partner_id":9000,"passed":"false","risk_amount":"0","risk_loan_level":"LEVEL_THREE","sign":"4e32c73dafe476209843fd916a5cccb0","user_idcard":"1141210809980028","user_level":"L-1","user_name":"twenty seven","user_phone":"82112341028","zeus_order_no":{order_no}},"msg":""}',
        'type': 'aes',
        'arg': 'm=cbc_pad=pkcs5_block=128_p=uaRZnvZoJZ8KSTuE_i=IFwDpMo01xY05ovH_o=0_s=gb2312_t=0'
    }
    print(f"[{order_no} asdfg}")
       # {"code":0,"data":{"code":200,"feature_list":[],"forbidApplyUntil":1647746861000,"loan_type":0,"order_no":{order_no},"partner_id":9000,"passed":"false","risk_amount":"0","risk_loan_level":"LEVEL_THREE","sign":"4e32c73dafe476209843fd916a5cccb0","user_idcard":"1141210809980028","user_level":"L-1","user_name":"twenty seven","user_phone":"82112341028","zeus_order_no":{order_no}},"msg":""}
# """        )
#     result = requests.post(url, data)
#     html = result.text
#     encrypt_date = json.loads(html)['data'][0]
#     print(encrypt_date)
#     return encrypt_date


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('uatas tool')

    fengkong_frame = tk.Frame(master=root)
    fengkong_frame.pack(side='left')
    # 订单号标签
    order_no_label = tk.Label(fengkong_frame, text='order_no')
    order_no_label.pack(side='left')
    # 输入订单号
    order_no = tk.StringVar(fengkong_frame)
    order_no_entry = tk.Entry(fengkong_frame, text=order_no)
    order_no_entry.pack(side='left')
    # 加密按钮
    bt_01 = tk.Button(fengkong_frame, text='加密', command=lambda: aes_encrypt(order_no.get()))
    bt_01.pack(side='left')
    print(order_no.get())

    root.mainloop()
