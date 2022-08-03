import tkinter as tk
import random
import sys

bg_color = {
    # '': 'azure4',
    '2': '#eee4da',
    '4': '#ede0c8',
    '8': '#edc850',
    '16': '#edc53f',
    '32': '#f67c5f',
    '64': '#f65e3b',
    '128': '#edcf72',
    '256': '#edcc61',
    '512': '#f2b179',
    '1024': '#f59563',
    '2048': '#edc22e',
}
fg_color = {
    '2': '#776e65',
    '4': '#f9f6f2',
    '8': '#f9f6f2',
    '16': '#f9f6f2',
    '32': '#f9f6f2',
    '64': '#f9f6f2',
    '128': '#f9f6f2',
    '256': '#f9f6f2',
    '512': '#776e65',
    '1024': '#f9f6f2',
    '2048': '#f9f6f2',
}
rows = 2
columns = 4
squ_size = [rows, columns]
gridCell_label = []
gridCell_num = [[0] * columns for n in range(rows)]


def create_widget():
    create_squ()  # 创建游戏区域
    random_num()  # 初始化随机生成1个数字
    random_num()  # 初始化随机生成1个数字
    show_num()  # 展示数字
    root.bind('<Key>', move)  # 移动操作


def create_squ():
    """使用label创建游戏区域"""
    for row in range(rows):
        row_cells = []
        for column in range(columns):
            label = tk.Label(root, text='', bg='azure4', font=('arial', 22), width=4, height=2)
            label.grid(row=row, column=column, padx=5, pady=5)
            row_cells.append(label)
        gridCell_label.append(row_cells)


def random_num():
    random_cells = []
    for row in range(rows):
        for column in range(columns):
            if gridCell_num[row][column] == 0:
                random_cells.append((row, column))
    random_cell = random.choice(random_cells)
    random_text = random.choice([2, 4])
    gridCell_num[random_cell[0]][random_cell[1]] = random_text
    print('row=' + str(random_cell[0]),
          'columu=' + str(random_cell[1]),
          'random_text=' + str(random_text),
          'lineno=' + str(sys._getframe().f_lineno))


def show_num():
    """展示数字颜色"""
    for row in range(rows):
        for column in range(columns):
            if gridCell_num[row][column] != 0:
                gridCell_label[row][column].config(bg=bg_color[str(gridCell_num[row][column])],
                                                   fg=fg_color[str(gridCell_num[row][column])],
                                                   text=gridCell_num[row][column])
            else:
                gridCell_label[row][column].config(bg='azure4')


def move(event):
    derictions = {
        'Up': "print('up')",
        'Down': "print('down')",
        'Left': left,
        'Right': "print('right')",
    }
    # sys._getframe().f_lineno
    pressed_key = event.keysym
    print(pressed_key, event.keysym, sys._getframe().f_lineno)
    if event.keysym in derictions.keys():
        print(derictions[event.keysym])
        derictions[event.keysym]



def left():
    for row in range(0, rows):
        # for column in range(0, columns - 1):
        column = 0
        while column < columns - 1:
            print(str(gridCell_num[row][column]), sys._getframe().f_lineno)
            if str(gridCell_num[row][column]) == '':
                gridCell_num[row][column], gridCell_num[row][column + 1] = gridCell_num[row][column + 1], \
                                                                           gridCell_num[row][column]
                show_num()
                print(gridCell_num[row][column], sys._getframe().f_lineno)
                column += 1
            else:
                break
    # print(num_list)
    # show_num()


def fix_geometry():
    width = ''


def create_font():
    ...


if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry('500x300+100+100')
    root.title('Game_2048 V1.0.1')
    create_widget()
    root.mainloop()
