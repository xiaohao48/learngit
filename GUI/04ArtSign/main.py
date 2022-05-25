import tkinter as tk
from tkinter import messagebox
import requests
import re
from PIL import ImageTk

fonts = {
    '个性签': 'jfcs.ttf',
    '连笔签': 'qmt.ttf',
    '潇洒签': 'bzcs.ttf',
    '草体签': 'lfc.ttf',
    '合文签': 'haku.ttf',
    '商务签': 'zql.ttf',
    '可爱签': 'yqk.ttf'
}


def createWidget(master):
    global name_var, font_var, image
    bt_frame = tk.Frame(master=master)
    bt_frame.pack()

    name_var = tk.StringVar(bt_frame)
    name_entry = tk.Entry(bt_frame, textvariable=name_var)
    name_entry.pack(side='left')

    font_var = tk.StringVar(bt_frame)
    font_om = tk.OptionMenu(bt_frame, font_var, *fonts.keys())
    font_om['width'] = 10
    font_om.pack(side='left')

    confirm_bt = tk.Button(bt_frame, text='确定', command=test)
    confirm_bt.pack(side='left')

    im_frame = tk.Frame(master=master)
    im_frame.pack()
    # image = createSign('肖昊')
    image = tk.PhotoImage(file='肖昊.gif')
    im_label = tk.Label(im_frame, image=image)
    im_label.pack()



def createSign(name):
    url = 'http://www.uustv.com/'
    if not name:
        messagebox.showinfo('提示：请输入姓名')
    else:
        date = {
            'word': name,
            'sizes': 60,
            'fonts': '1.ttf',
            'fontcolor': '#000000'
        }
        result = requests.post(url, data=date)
        result.encoding = 'utf-8'
        html = result.text
        reg = '<div class="tu">.*?<img src="(.*?)"/></div>'
        img_path = re.findall(reg, html)
        img_url = url + img_path[0]
        response = requests.get(img_url).content
        f = open(f'{name}.gif', 'wb')
        f.write(response)
        bm = ImageTk.PhotoImage(file=f'{name}.gif')
        return bm


def test():
    print(name_var.get())
    print(font_var.get())


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('Art Sign')
    createWidget(root)
    root.mainloop()
