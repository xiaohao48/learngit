import requests
import re
import tkinter as tk
import os


class Applications(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.lb_url = tk.Label(self, text="PPT url:", width=10, bg='green')
        self.lb_url.grid(row=1, column=1, sticky='ew')

        self.lb_ppt_name = tk.Label(self, text="PPT name:", width=10, bg='green')
        self.lb_ppt_name.grid(row=2, column=1, sticky='ew')

        self.lb_ppt_page = tk.Label(self, text="PPT page:", width=10, bg='green')
        self.lb_ppt_page.grid(row=3, column=1, sticky='ew')

        self.lb_show = tk.Label(self, text="", width=10, height=6, bg='green')
        self.lb_show.grid(row=4, column=1, columnspan=3, sticky='ew')

        self.entry_url_var = tk.StringVar(value='http://ppt.doczj.com/ppt/0b871761-')
        self.entry_url = tk.Entry(self, text=self.entry_url_var, width=30)
        self.entry_url.grid(row=1, column=2, sticky='ew')

        self.entry_name_var = tk.StringVar(value='《护理文书书写》PPT课件')
        self.entry_name = tk.Entry(self, text=self.entry_name_var, width=30)
        self.entry_name.grid(row=2, column=2, sticky='ew')

        self.entry_page_var = tk.StringVar(value=5)
        self.entry_page = tk.Entry(self, text=self.entry_page_var, width=30)
        self.entry_page.grid(row=3, column=2, sticky='ew')

        self.bt_clrear = tk.Button(self, text="清空", command=self.data_clear, width=7)
        self.bt_clrear.grid(row=1, column=3, sticky='ew')

        self.bt_down = tk.Button(self, text="下载", command=self.down_img, width=7)
        self.bt_down.grid(row=2, column=3, sticky='ew')

        self.bt_check = tk.Button(self, text="查看", command=self.check_file, width=7)
        self.bt_check.grid(row=3, column=3, sticky='ew')

    def data_clear(self):
        self.entry_url_var.set(value='')
        self.entry_name_var.set(value='')
        self.entry_page_var.set(value='')
        self.lb_show['text'] = '已清空'

    def down_img(self):
        if self.entry_url_var.get() != '' and self.entry_name_var.get() != '' and self.entry_page_var.get() != '':
            for page in range(1, int(self.entry_page_var.get()) + 1):
                url = f'{self.entry_url_var.get()}-{page}.html'
                result = requests.get(url)
                result.encoding = 'utf-8'
                html = result.text
                reg = f'<p class="img"><img src="(.*?)" alt="{self.entry_name_var.get()}" /></p>'
                img_path = re.findall(reg, html)
                # print(img_path[0])
                head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
                response = requests.get(img_path[0], headers=head).content

                with open(f'img_ppt_{page}.jpg', 'wb') as f:
                    f.write(response)
                f.close()
            self.lb_show["text"] = "下载完成"
        else:
            self.lb_show['text'] = '请输入相关信息'

    def check_file(self):
        folder = os.getcwd()
        self.lb_show['text'] = folder
        os.startfile(folder)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("400x200+200+300")
    root.title('在线PPT下载')
    app = Applications(master=root)
    root.mainloop()
