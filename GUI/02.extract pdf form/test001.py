from tkinter import *
from tkinter.filedialog import *

root = Tk();
root.geometry("400x100")


def test1():
    f = askopenfilename(title="上传文件")  # print(f)
    show["text"]=f
Button(root,text="选择编辑的视频文件",command=test1).pack()
show = Label(root,width=40,height=3,bg="green")
show.pack()
root.mainloop()
