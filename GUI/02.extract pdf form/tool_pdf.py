import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.createLabel("请选择文件", row=0, column=0, rowspan=1, columnspan=1)

    def createLabel(self, text, row, column, rowspan, columnspan):
        self.create_label = tk.Label(self, text=text)
        self.create_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1200x800+50+50')
    root.title("pdf tools")
    app = Application(master=root)
    root.mainloop()
