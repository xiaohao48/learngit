import json
import time
import logging
import pandas as pd
from db_config import uatas_bi_db, uatas_bi_cursor, conn_engine
import tkinter as tk
from tkinter import filedialog
import re

Timestamp = int(time.time())
print(Timestamp)


def create_widget(master):
    global show_text
    bt_frame = tk.Frame(master=master)
    bt_frame.pack()
    choose_file_bt = tk.Button(bt_frame, text='选择文件', command=choose_file)
    choose_file_bt.pack(side="left")
    print(Timestamp)
    # loan_choose_bt = tk.Button(bt_frame, text="放款上传", command=loan_update)
    # loan_choose_bt.pack(side="left")
    # pay_OTC_bt = tk.Button(bt_frame, text="OTC还款上传", command=OTC_update)
    # pay_OTC_bt.pack(side="left")
    # pay_VA_bt = tk.Button(bt_frame, text="VA还款上传", command=VA_update)
    # pay_VA_bt.pack(side="left")
    check_bt = tk.Button(bt_frame, text="上传校对", command=check_file)
    print(Timestamp)
    check_bt.pack(side="left")
    out_bt = tk.Button(bt_frame, text="输出txt", command=out_put)
    out_bt.pack(side="left")

    text_frame = tk.Frame(master=master)
    text_frame.pack()
    show_text = tk.Text(text_frame, width=110, height=20)
    show_text.pack()


def choose_file():
    global files,Timestamp
    Timestamp = int(time.time())
    print(Timestamp)
    # matchObj = re.match(r'dogs', line, re.M | re.I)
    files = {}
    file = filedialog.askopenfilenames(title='选择文件')
    for file_element in file:
        if re.search("Disbursement", file_element, re.M | re.I):
            files["loan"] = file_element
        if re.search("OTC", file_element, re.M | re.I):
            files["OTC"] = file_element
        if re.search("VA", file_element, re.M | re.I):
            files["VA"] = file_element
    print(files)
    if file:
        show_text.delete(1.0, tk.END)
        show_text.insert(1.0, file)
    return file


# def loan_update():
#     excel_import(file=files["loan"], column='F,G', type='loan')
#     show_text.insert(tk.INSERT, "\n" + files["loan"] + "loan")
#     data_comparison(Timestamp)
#     data = export(Timestamp)
#     uatas_bi_db.close()
#     show_text.delete(1.0, tk.END)
#     show_text.insert(1.0, data)
#
#
# def OTC_update():
#     excel_import(file=files["OTC"], column='B,H', type='repay')
#     show_text.insert(tk.INSERT, "\n" + files["OTC"] + "OTC")
#     data_comparison(Timestamp)
#     data = export(Timestamp)
#     uatas_bi_db.close()
#     show_text.delete(1.0, tk.END)
#     show_text.insert(1.0, data)
#
#
# def VA_update():
#     excel_import(file=files["VA"], column='F,G', type='repay')
#     show_text.insert(tk.INSERT, "\n" + files["VA"] + "VA")
#     data_comparison(Timestamp)
#     data = export(Timestamp)
#     uatas_bi_db.close()
#     show_text.delete(1.0, tk.END)
#     show_text.insert(1.0, data)


def check_file():
    if "loan" in files.keys():
        excel_import(file=files["loan"], column='F,G', type='loan')
    if "OTC" in files.keys():
        excel_import(file=files["OTC"], column='B,H', type='repay')
    if "VA" in files.keys():
        excel_import(file=files["VA"], column='F,G', type='repay')
    print(Timestamp)
    data_comparison(Timestamp)
    print(Timestamp)
    data = export(Timestamp)
    uatas_bi_db.close()
    show_text.delete(1.0, tk.END)
    show_text.insert(1.0, data)


def out_put():
    text = show_text.get(1.0, tk.END)
    print(text)
    print(type(text))
    with open("error.txt", "w") as outfile:
        outfile.write(text)


def excel_import(file, column, type):
    newcol = ['external_id', 'amount']
    df1 = pd.read_excel(file, names=newcol, sheet_name=0, usecols=column)
    df1.insert(loc=0, column='timestamp', value=Timestamp)
    df1_format = df1.rename(columns=str.strip).dropna()
    df1_format['type'] = type
    print(df1_format)
    df1_format.to_sql('temp_check_account', con=conn_engine, if_exists='append', index=False)


def data_comparison(ctime):
    uatas_bi_db.ping(reconnect=True)
    repaysql_1 = """UPDATE uatas_bi.temp_check_account tca JOIN  uatas_pay_3.repay_order ro on ro.repay_external_id=
    tca.external_id JOIN cash_pay_1.timepay_repay_order tro on ro.partner_transaction_no=tro.order_no AND 
    ro.plat_transaction_no=transaction_No AND ro.pay_no=tro.user_pay_no AND ro.payer_user_id=tro.payer_user_id JOIN 
    cash_core_1.pay_record_log prl on tro.source=prl.source AND tro.source_order_id=prl.source_order_id AND tro.core_no
    =prl.id AND tro.user_pay_no=prl.pay_account_no SET tca.partner_id = ro.partner_id, tca.channel=ro.channel, 
    tca.pay_no=ro.pay_no, tca.payment_status=ro.status, tca.payment_amount=ro.amount, tca.loan_id=prl.loan_id, 
    tca.source=prl.source, tca.core_status=prl.order_status, tca.core_amount=prl.amount WHERE tca.type='repay' AND 
    tca.timestamp= %s ;"""
    uatas_bi_cursor.execute(repaysql_1 % ctime)
    uatas_bi_db.commit()

    repaysql_2 = """UPDATE uatas_bi.temp_check_account tca
    JOIN  uatas_pay_3.repay_order ro on ro.repay_external_id=tca.external_id
    JOIN cash_pay_2.timepay_repay_order tro on ro.partner_transaction_no=tro.order_no AND ro.plat_transaction_no=transaction_No AND ro.pay_no=tro.user_pay_no AND ro.payer_user_id=tro.payer_user_id
    JOIN cash_core_2.pay_record_log prl on tro.source=prl.source AND tro.source_order_id=prl.source_order_id AND tro.core_no=prl.id AND tro.user_pay_no=prl.pay_account_no
    SET tca.partner_id = ro.partner_id, tca.channel=ro.channel, tca.pay_no=ro.pay_no, tca.payment_status=ro.status, tca.payment_amount=ro.amount, tca.loan_id=prl.loan_id, tca.source=prl.source, tca.core_status=prl.order_status, tca.core_amount=prl.amount
    WHERE tca.type='repay' AND tca.timestamp= %s 
    ;"""
    uatas_bi_cursor.execute(repaysql_2 % ctime)
    uatas_bi_db.commit()

    repaysql_3 = """UPDATE uatas_bi.temp_check_account tca
    JOIN cash_pay_1.timepay_repay_order tro on tca.external_id = tro.order_no
    JOIN cash_core_1.pay_record_log prl on tro.source=prl.source AND tro.source_order_id=prl.source_order_id AND tro.core_no=prl.id AND tro.user_pay_no=prl.pay_account_no
    SET tca.channel=tro.channel, tca.pay_no=tro.user_pay_no,tca.loan_id=prl.loan_id, tca.source=prl.source, tca.core_status=prl.order_status, tca.core_amount=prl.amount
    WHERE tca.type='repay' AND tca.timestamp= %s 
;"""
    uatas_bi_cursor.execute(repaysql_3 % ctime)
    uatas_bi_db.commit()

    repaysql_4 = """UPDATE uatas_bi.temp_check_account tca
        JOIN cash_pay_2.timepay_repay_order tro on tca.external_id = tro.order_no
        JOIN cash_core_2.pay_record_log prl on tro.source=prl.source AND tro.source_order_id=prl.source_order_id AND tro.core_no=prl.id AND tro.user_pay_no=prl.pay_account_no
        SET tca.channel=tro.channel, tca.pay_no=tro.user_pay_no,tca.loan_id=prl.loan_id, tca.source=prl.source, tca.core_status=prl.order_status, tca.core_amount=prl.amount
        WHERE tca.type='repay' AND tca.timestamp= %s 
    ;"""
    uatas_bi_cursor.execute(repaysql_4 % ctime)
    uatas_bi_db.commit()

    repaysql_payment = """UPDATE uatas_bi.temp_check_account tca
JOIN uatas_pay_3.repay_order ro on ro.repay_external_id=tca.external_id and ro.partner_id in (1,2,14)
SET tca.partner_id = ro.partner_id, tca.channel=ro.channel, tca.pay_no=ro.pay_no, tca.payment_status=ro.status, tca.payment_amount=ro.amount
WHERE tca.type='repay' AND tca.timestamp= %s 
        ;"""
    uatas_bi_cursor.execute(repaysql_payment % ctime)
    uatas_bi_db.commit()

    loansql_payment = """UPDATE uatas_bi.temp_check_account tca
JOIN uatas_pay_3.loan payl on tca.external_id=payl.step_loan_external_id and payl.partner_id in (1,2,14)
SET tca.partner_id=payl.partner_id, tca.channel=payl.pay_channel, tca.payment_status=payl.status, tca.payment_amount=payl.loan_actual_amount
WHERE tca.type='loan' AND tca.timestamp= %s 
    ;"""
    uatas_bi_cursor.execute(loansql_payment % ctime)
    uatas_bi_db.commit()

    loansql_1 = """UPDATE uatas_bi.temp_check_account tca
JOIN uatas_pay_3.loan payl on tca.external_id=payl.step_loan_external_id
JOIN cash_pay_1.timepay_loan_order tlo on payl.uid =tlo.payee_user_id AND payl.partner_loan_id=tlo.core_no AND payl.order_no=tlo.transaction_No
JOIN cash_core_1.loan l on tlo.source_order_id=l.id AND l.user_id=tlo.payee_user_id 
SET tca.partner_id=payl.partner_id, tca.channel=payl.pay_channel, tca.payment_status=payl.status, tca.payment_amount=payl.loan_actual_amount
, tca.loan_id=l.id, tca.source=tlo.source, tca.core_status=l.status, tca.core_amount=l.loan_actual_amount
WHERE tca.type='loan' AND tca.timestamp= %s
;"""
    uatas_bi_cursor.execute(loansql_1 % ctime)
    uatas_bi_db.commit()

    loansql_2 = """UPDATE uatas_bi.temp_check_account tca
    JOIN uatas_pay_3.loan payl on tca.external_id=payl.step_loan_external_id
    JOIN cash_pay_2.timepay_loan_order tlo on payl.uid =tlo.payee_user_id AND payl.partner_loan_id=tlo.core_no AND payl.order_no=tlo.transaction_No
    JOIN cash_core_2.loan l on tlo.source_order_id=l.id AND l.user_id=tlo.payee_user_id 
    SET tca.partner_id=payl.partner_id, tca.channel=payl.pay_channel, tca.payment_status=payl.status, tca.payment_amount=payl.loan_actual_amount
    , tca.loan_id=l.id, tca.source=tlo.source, tca.core_status=l.status, tca.core_amount=l.loan_actual_amount
    WHERE tca.type='loan' AND tca.timestamp= %s
    ;"""
    uatas_bi_cursor.execute(loansql_2 % ctime)
    uatas_bi_db.commit()


def export(ctime):
    export_sql = """SELECT * FROM temp_check_account tca 
            WHERE tca.timestamp= %s and
            ((partner_id is null AND channel is null ) OR
            (partner_id in (1,2,14) AND payment_status not in (2,12)) OR
            (partner_id not in (1,2,14) AND (payment_status not in (2,12) OR core_status!=2)) OR
            (partner_id is null AND core_status!=2))"""
    uatas_bi_cursor.execute(export_sql % ctime)
    export_db = uatas_bi_cursor.fetchall()
    export_df = pd.DataFrame(export_db)
    pd.set_option('display.max_columns', None)
    print(export_df)
    # export_df.to_excel('error.xlsx')
    return export_df


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('对账工具 V1.0.0')
    create_widget(root)
    root.mainloop()
