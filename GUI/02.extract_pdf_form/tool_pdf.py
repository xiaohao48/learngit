import tkinter as tk
from tkinter import filedialog
import os
import pdfplumber
from openpyxl import Workbook
import pyperclip
from tkinter import simpledialog
from tkinter import messagebox


def create_widget():
    global show
    btn_frame = create_frame(root)
    create_button(btn_frame, "选择文件", ask_file)
    create_button(btn_frame, "获取目录文件清单", get_file_names)
    create_button(btn_frame, "提取pdf表格", extract_pdf_table)
    create_button(btn_frame, "保存pdf表格", save_table)
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
    page = simpledialog.askinteger(title='page of table', prompt='请输入表格所在页码(0表示所有)', initialvalue=1)
    return page


def get_save_file():
    file = simpledialog.askstring(title='name of table', prompt='请输入文件名', initialvalue='test.xlsx')
    return file


def showinfo():
    messagebox.showinfo(title='tips', message='输入错误或文件类型错误')


def extract_pdf_table():
    path = choose_file()
    page = get_pages() - 1
    try:
        with pdfplumber.open(path) as pdf:
            page01 = pdf.pages[page]
            table = page01.extract_table()
        tables = []
        for row in table:
            tables.append(','.join(row))
        show['text'] = '\n'.join(tables)
    except:
        showinfo()


def extract_pdf_text():
    path = choose_file()
    page = get_pages()
    try:
        if page == 0:
            page_texts = []
            with pdfplumber.open(path) as pdf:
                for page_text in pdf.pages:
                    text = page_text.extract_text()
                    page_texts.append(text)
            show['text'] = '\n'.join(page_texts)
        elif page > 0:
            page = page - 1
            with pdfplumber.open(path) as pdf:
                page_text = pdf.pages[page]
                text = page_text.extract_text()
            show['text'] = text
    except:
        showinfo()


def save_table():
    workbook = Workbook()
    sheet = workbook.active
    table = show['text'].split('\n')
    for row in table:
        sheet.append(row.split(','))
    f = get_save_file()
    workbook.save(filename=f)


def copy_file():
    text = show['text']
    return pyperclip.copy(text)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600')
    root.title("pdf tools")
    create_widget()
    root.mainloop()
