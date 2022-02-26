import tkinter as tk
from tkinter import filedialog


def create_widget(root):
    create_label(root, "请选择文件", 10, 10, 10, 2, 'green')
    create_button(root, "选择文件", ask_file, 10, 50)


def create_label(root, text, x, y, width, height, bg):
    create_new_label = tk.Label(root, text=text, width=width, height=height, bg=bg)
    create_new_label.place(x=x, y=y)
    return create_new_label


def create_button(root, text, command, x, y):
    create_new_button = tk.Button(root, text=text, command=command)
    create_new_button.place(x=x, y=y)


def ask_file():
    f = filedialog.askopenfilename(title='选择文件')
    show = create_label(root, '', 10, 90, 50, 2, 'pink')
    show["text"] = f


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x300')
    root.title("pdf tools")
    create_widget(root)
    root.mainloop()
