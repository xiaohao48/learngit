import tkinter as tk


def create_widget():
    lb01 = tk.Label(text='helllo')
    lb01.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x300')
    root.title('joke')
    create_widget()
    root.mainloop()
