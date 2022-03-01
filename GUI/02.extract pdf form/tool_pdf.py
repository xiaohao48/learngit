import tkinter as tk
from tkinter import filedialog
import os
import pdfplumber
from openpyxl import Workbook
import pyperclip
from tkinter import simpledialog


def create_widget():
    global show
    btn_frame = create_frame(root)
    create_button(btn_frame, "选择文件", ask_file)
    create_button(btn_frame, "获取目录文件清单", get_file_names)
    create_button(btn_frame, "提取pdf表格", extract_pdf_table)
    create_button(btn_frame, "提取pdf文本", extract_pdf_text)
    create_button(btn_frame, "复制", copy_file)

    leb_frame = create_frame(root)
    show = create_label(leb_frame, '', 100, 10, 'pink')


def create_frame(master):
    create_new_frame = tk.Frame(master=master)
    create_new_frame.pack()
    return create_new_frame


def create_label(master, text, width, height, bg):
    create_new_label = tk.Label(master=master, text=text, width=width, height=height, bg=bg, justify='left')
    create_new_label.pack(side='left')
    return create_new_label


def create_button(master, text, command):
    create_new_button = tk.Button(master=master, text=text, command=command)
    create_new_button.pack(side='left')


def create_text(master, width, height):
    create_new_text = tk.Text(master=master, width=width, height=height)
    create_new_text.pack()
    return create_new_text


def choose_file():
    f = filedialog.askopenfilename(title='选择文件')
    return f


def ask_file():
    f = choose_file()
    show["text"] = f


def get_file_names():
    path = filedialog.askdirectory()
    filenames = os.listdir(path)
    show["text"] = "目录下文件：\n" + '\n'.join(filenames)


def get_pages():
    page = simpledialog.askinteger(title='page of table', prompt='请输入表格所在页码', initialvalue=1)
    return page


def extract_pdf_table():
    path = choose_file()
    page = get_pages() - 1
    with pdfplumber.open(path) as pdf:
        page01 = pdf.pages[page]
        table = page01.extract_table()
    tables = []
    for row in table:
        tables.append(','.join(row))
    show['text'] = '\n'.join(tables)


def extract_pdf_text():
    path = choose_file()
    page = get_pages() - 1
    with pdfplumber.open(path) as pdf:
        page01 = pdf.pages[page]
        text = page01.extract_text()
    show['text'] = text

    # with pdfplumber.open(
    #         'C:/Users/xh411/Documents/WXWork/1688851257484603/Cache/File/2022-02/12. DESEMBER 2021/12. REKENING KORAN - BNI ESCROW - 01 DES 2021.pdf') as pdf:
    #     all_table = []
    #     for page in range(1):
    #         page01 = pdf.pages[page]
    #         table = page01.extract_table()
    #         all_table.append(table)
    #     workbook = Workbook()
    #     sheet = workbook.active
    #     for table in all_table:
    #         for row in table:
    #             print(row[-1])
    #             sheet.append(row)
    #     workbook.save(
    #         filename='C:/Users/xh411/Documents/WXWork/1688851257484603/Cache/File/2022-02/12. DESEMBER 2021/12. REKENING KORAN - BNI ESCROW - 01 DES 2021.xlsx')


def copy_file():
    text = show['text']
    return pyperclip.copy(text)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title("pdf tools")
    create_widget()
    root.mainloop()
