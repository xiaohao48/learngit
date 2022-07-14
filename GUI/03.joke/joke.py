import tkinter as tk
from tkinter import messagebox
import random


def on_exit():
    messagebox.showwarning(title='提示', message='回答错误')


def move(event):
    no_btn.place(relx=random.random(), rely=random.random())


def sure():
    frame1.pack_forget()
    frame2.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x300+100+100')
    root.title('辞职信')

    frame1 = tk.Frame(root)
    frame1.pack()

    tk.Label(frame1, text='告诉我，你是不是大佬！！！！！！', font=30, padx=30, pady=30, width=50, height=30).pack(side='left',
                                                                                                   anchor='n')

    # img = tk.PhotoImage(file='多啦A梦_11_爱给网_aigei_com.gif')
    # label_img = tk.Label(frame1, image=img, padx=30, pady=30, bd=0)
    # label_img.pack()

    yes_btn = tk.Button(frame1, text='肯定是', command='')
    yes_btn.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
    no_btn = tk.Button(frame1, text='不是', command='')
    no_btn.place(relx=0.8, rely=0.9, anchor=tk.CENTER)
    # tk.Label(frame1, text='辞职人：正心', font=24, padx=30, pady=30, anchor='s').place(relx=0.8, rely=0.8)

    frame2 = tk.Frame(root)
    # frame2.pack()
    tk.Label(
        frame2,
        text='看吧，终于承认了吧！！！\n'
             '大佬，请赐教！',
        font=('黑体', 18),
        height=300,
        fg='red',
        padx=50
    ).pack()
    tk.Button(frame2, text='退出', command=root.quit).place(relx=0.8, rely=0.8)

    root.protocol('WM_DELETE_WINDOW', on_exit)
    no_btn.bind('<Enter>', move)
    yes_btn.config(command=sure)

    root.mainloop()
