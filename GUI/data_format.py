from tkinter import *
from tkinter import filedialog
import sys
import pyperclip


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createLabel(self, text, row, column):
        self.init_data_label = Label(self, text=text)
        self.init_data_label.grid(row=row, column=column)

    def createText(self, width, height, row, column, rowspan, columnspan):
        self.init_text = Text(self, width=width, height=height)
        self.init_text.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        return self.init_text

    def createButton(self, text, command, row, column):
        self.format_button = Button(self, text=text, bg='lightblue', width=10, command=command)
        self.format_button.grid(row=row, column=column)

    def createEntry(self, row, column, value=''):
        inputEntry = StringVar(value=value)
        self.inputEntry = Entry(self, textvariable=inputEntry)
        self.inputEntry.grid(row=row, column=column)
        return self.inputEntry

    def createCheckButton(self, value, text, row, column):
        self.checkButtonVar = IntVar(value=value)
        self.checkButton = Checkbutton(self, text=text, variable=self.checkButtonVar, onvalue=1, offvalue=0)
        self.checkButton.grid(row=row, column=column)
        return self.checkButtonVar

    def copy(self):
        with open(r'out_data.txt', 'r') as f:
            out_text = f.read()
        return pyperclip.copy(out_text)

    def createWidget(self):
        # label
        self.createLabel("待处理数据", 0, 0)
        self.createLabel('前面添加', 2, 11)
        self.createLabel('后台添加', 4, 11)
        self.createLabel('前后添加', 6, 11)
        self.createLabel('分隔符', 8, 11)
        self.createLabel('剔除字符', 10, 11)

        # text
        self.init_data_text = self.createText(70, 50, 1, 0, 16, 10)
        self.out_data_text = self.createText(70, 50, 1, 12, 16, 10)

        # button
        self.createButton("确定", self.confirm, 1, 11)
        self.createButton('另存为', self.newFile, 15, 11)
        self.createButton("复制", self.copy, 16, 11)

        # entry
        self.add_before = self.createEntry(3, 11)
        self.add_later = self.createEntry(5, 11)
        self.add_b_l = self.createEntry(7, 11)
        self.delimiter = self.createEntry(9, 11, value=',')
        self.del_char = self.createEntry(11, 11)

        # checkButton
        self.del_repeate = self.createCheckButton(0, '删除重复值', 12, 11)
        self.del_newline = self.createCheckButton(1, '删除换行', 13, 11)
        self.del_em_value = self.createCheckButton(1, '删除空值', 14, 11)

        # self.init_data_label = Label(self, text='待处理数据')
        # self.init_data_label.grid(row=0, column=0)
        # self.out_data_label = Label(self, text='输出结果')
        # self.out_data_label.grid(row=0, column=12)

        # self.init_data_text = Text(self, width=70, height=50)
        # self.init_data_text.grid(row=1, column=0, rowspan=15, columnspan=10)
        # self.out_data_text = Text(self, width=70, height=50)
        # self.out_data_text.grid(row=1, column=12, rowspan=15, columnspan=10)

        # self.format_button = Button(self, text='确定', bg='lightblue', width=10, command=self.confirm)
        # self.format_button.grid(row=1, column=11)

        # Label(self, text='前面添加').grid(row=2, column=11)
        # add_before = StringVar()
        # self.add_before = Entry(self, textvariable=add_before)
        # self.add_before.grid(row=3, column=11)

        # Label(self, text='后面添加').grid(row=4, column=11)
        # add_later = StringVar()
        # self.add_later = Entry(self, textvariable=add_later)
        # self.add_later.grid(row=5, column=11)
        #
        # Label(self, text='前后添加').grid(row=6, column=11)
        # add_b_l = StringVar()
        # self.add_b_l = Entry(self, textvariable=add_b_l)
        # self.add_b_l.grid(row=7, column=11)
        #
        # Label(self, text='分隔符').grid(row=8, column=11)
        # delimiter = StringVar(value=",")
        # self.delimiter = Entry(self, textvariable=delimiter)
        # self.delimiter.grid(row=9, column=11)
        #
        # Label(self, text='剔除字符').grid(row=10, column=11)
        # del_char = StringVar()
        # self.del_char = Entry(self, textvariable=del_char)
        # self.del_char.grid(row=11, column=11)

        # self.del_repeate = IntVar(value=0)
        # self.del_repeate_b = Checkbutton(self, text='删除重复值', variable=self.del_repeate, onvalue=1, offvalue=0)
        # self.del_repeate_b.grid(row=12, column=11)
        #
        # self.del_newline = IntVar(value=1)
        # self.del_newline_b = Checkbutton(self, text='删除换行', variable=self.del_newline, onvalue=1, offvalue=0)
        # self.del_newline_b.grid(row=13, column=11)
        #
        # self.del_em_value = IntVar(value=1)
        # self.del_em_value_b = Checkbutton(self, text='删除空值', variable=self.del_em_value, onvalue=1, offvalue=0)
        # self.del_em_value_b.grid(row=14, column=11)

        # self.format_button = Button(self, text='另存为', bg='lightblue', width=10, command=self.newFile)
        # self.format_button.grid(row=15, column=11)

    def newFile(self):
        self.out_data = filedialog.asksaveasfilename(title="另存为", initialfile='未命名.txt', filetypes=[("文本文档", "*.txt")],
                                                     defaultextension=".txt", initialdir='C:/Users')
        self.confirm()
        with open(self.out_data, "w") as f:
            f.writelines(self.init_data)

    def confirm(self):
        self.init_data = self.init_data_text.get(1.0, END).split("\n")
        self.init_data.pop()
        # 删除空值
        if self.del_em_value.get() == 1:
            # for i in range(0, len(init_data)):
            #     if "" in init_data:
            #         init_data.remove("")
            if "" in self.init_data:
                self.init_data.remove("")

        # 添加字符
        if len(self.add_before.get()) > 0:
            self.init_data = [self.add_before.get() + m for m in self.init_data]
        if len(self.add_later.get()) > 0:
            self.init_data = ["{0}{1}".format(m, self.add_later.get()) for m in self.init_data]
        if len(self.add_b_l.get()) > 0:
            self.init_data = ["{0}{1}{0}".format(self.add_b_l.get(), m) for m in self.init_data]

        # 删除重复值
        if self.del_repeate.get() == 1:
            self.init_data = list(set(self.init_data))

        # 添加分隔符
        if len(self.delimiter.get()) > 0 and len(self.init_data) > 0:
            # init_data = self.delimiter.get().join(init_data)
            self.init_data = [init_data_detail + self.delimiter.get() for init_data_detail in self.init_data]
            # 最后一个字符去掉分隔符
            self.init_data[-1] = self.init_data[-1][0:len(self.init_data[-1]) - len(self.delimiter.get())]

        # 删除换行符
        if self.del_newline.get() == 0:
            self.init_data = [init_data_detail + "\n" for init_data_detail in self.init_data]

        # 剔除字符
        if len(self.del_char.get()) > 0:
            self.init_data = [init_data_detail.replace(self.del_char.get(), "") for init_data_detail in self.init_data]

        with open(r"out_data.txt", "w") as f:
            f.writelines(self.init_data)

        with open(r'out_data.txt', 'r') as f:
            self.out_text = f.read()

        self.out_data_text.delete(1.0, END)
        self.out_data_text.insert(1.0, self.out_text)


if __name__ == '__main__':
    root = Tk()
    root.geometry('1200x800+20+20')
    app = Application(master=root)
    root.title("格式化工具V1.0.1")
    root.mainloop()
