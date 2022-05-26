import tkinter as tk
from tkinter import messagebox
import requests
import re
from PIL import ImageTk, Image
import io

fonts = {
    '艺术签': '1.ttf',
    '个性签': '3.ttf',
    '连笔签': 'zql.ttf',
    '潇洒签': 'bzcs.ttf',
    '草体签': 'lfc.ttf',
    '商务签': '8.ttf',
    '可爱签': 'yqk.ttf',
    '楷书签': '6.ttf',
    '行书签': '2.ttf'
}


def createWidget(master):
    global name_var, font_var, image, im_label

    bt_frame = tk.Frame(master=master)
    bt_frame.pack()
    # 姓名标签
    name_label = tk.Label(bt_frame, text='姓名')
    name_label.pack(side='left')
    # 输入姓名
    name_var = tk.StringVar(bt_frame)
    name_entry = tk.Entry(bt_frame, textvariable=name_var)
    name_entry.pack(side='left')
    # 样式提示
    style_label = tk.Label(bt_frame, text='样式')
    style_label.pack(side='left')
    # 样式选择
    font_var = tk.StringVar(bt_frame)
    font_om = tk.OptionMenu(bt_frame, font_var, *fonts.keys())
    font_om['width'] = 10
    font_om.pack(side='left')
    # 图片展示
    im_frame = tk.Frame(master=master)
    im_frame.pack()
    image = None
    im_label = tk.Label(im_frame, image=image)
    im_label.pack()
    # 生成签名按钮
    confirm_bt = tk.Button(bt_frame, text='确定', command=showSign)
    confirm_bt.pack(side='left')
    save_bt = tk.Button(bt_frame, text='另存为', command=saveImage)
    save_bt.pack(side='left')


def showSign():
    global tk_image
    if name_var.get():
        response = createSign(name_var.get())
        data_stream = io.BytesIO(response)
        pil_img = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_img)
        # image = createSign(name_var.get())
        im_label.configure(image=tk_image)
        root.update_idletasks()
    else:
        messagebox.showinfo('提示', '请输入姓名')


def saveImage():
    response = createSign(name_var.get())
    with open(f'{name_var.get()}.gif', 'wb') as f:
        f.write(response)
    messagebox.showinfo('提示', '保存成功')


def createSign(name):
    url = 'http://www.uustv.com/'
    # if not name:
    #     messagebox.showinfo('提示', '请输入姓名')
    # else:
    date = {
        'word': name,
        'sizes': 60,
        'fonts': fonts[font_var.get()],
        'fontcolor': '#000000'
    }
    result = requests.post(url, data=date)
    result.encoding = 'utf-8'
    html = result.text
    reg = '<div class="tu">.*?<img src="(.*?)"/></div>'
    img_path = re.findall(reg, html)
    img_url = url + img_path[0]
    response = requests.get(img_url).content
    return response
    # data_stream = io.BytesIO(response)
    # pil_image = Image.open(data_stream)
    # tk_image = ImageTk.PhotoImage(pil_image)
    # return tk_image


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title('Art Sign V1.0.1')
    createWidget(root)
    root.mainloop()
