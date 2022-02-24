from tkinter import *
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

    def createWidget(self):
        """创建组件"""
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

    def confirm(self):
        """数据格式化"""
        print(self.init_data_text.get(1.0, END))
        self.init_data = self.init_data_text.get(1.0, END).split("\n")
        self.init_data.pop()

        # 删除空值
        if self.del_em_value.get() == 1:
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
            self.init_data = [init_data_detail + self.delimiter.get() for init_data_detail in self.init_data]
            # 最后一个字符去掉分隔符
            self.init_data[-1] = self.init_data[-1][0:len(self.init_data[-1]) - len(self.delimiter.get())]

        # 删除换行符
        if self.del_newline.get() == 0:
            self.init_data = [init_data_detail + "\n" for init_data_detail in self.init_data]

        # 剔除字符
        if len(self.del_char.get()) > 0:
            self.init_data = [init_data_detail.replace(self.del_char.get(), "") for init_data_detail in self.init_data]

        self.out_data_text.delete(1.0, END)
        self.out_data_text.insert(1.0, self.init_data)

    def copy(self):
        return pyperclip.copy(''.join(self.init_data))


if __name__ == '__main__':
    root = Tk()
    root.geometry('1200x800+20+20')
    app = Application(master=root)
    root.title("格式化工具V1.0.1")
    root.mainloop()
