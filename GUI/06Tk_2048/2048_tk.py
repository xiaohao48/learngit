import tkinter as tk
import random
import sys
from tkinter import messagebox

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
rows = 3
columns = 5
squ_size = [rows, columns]
gridCell_label = []
gridCell_num = [[0] * columns for n in range(rows)]
score = 0
max_num = 2048
can_merge = False


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
    if random_cells != []:
        random_cell = random.choice(random_cells)
        random_text = random.choice([2, 4])
        gridCell_num[random_cell[0]][random_cell[1]] = random_text
        # print('row=' + str(random_cell[0]),
        #       'columu=' + str(random_cell[1]),
        #       'random_text=' + str(random_text),
        #       'lineno=' + str(sys._getframe().f_lineno))
    else:
        messagebox.showinfo(title='提示', message='Game over!')


def show_num():
    """展示数字颜色"""
    for row in range(rows):
        for column in range(columns):
            if gridCell_num[row][column] != 0:
                gridCell_label[row][column].config(bg=bg_color[str(gridCell_num[row][column])],
                                                   fg=fg_color[str(gridCell_num[row][column])],
                                                   text=gridCell_num[row][column])
            else:
                gridCell_label[row][column].config(bg='azure4', text='')


def move(event):
    derictions = {
        'Up': "print('up')",
        'Down': "print('down')",
        'Left': "left",
        'Right': "print('right')",
    }
    # sys._getframe().f_lineno
    pressed_key = event.keysym
    # print(pressed_key, sys._getframe().f_lineno)
    if pressed_key == 'Left':
        compressGridLevel()
        mergeGridLevel()
    if pressed_key == 'Right':
        leftToRight()
        compressGridLevel()
        mergeGridLevel()
        leftToRight()
    if pressed_key == 'Up':
        transposeToVertical()
        compressGridVertical()
        mergeGridVertical()
        transposeToLevel()
    if pressed_key == 'Down':
        transposeToVertical()
        leftToRight()
        compressGridVertical()
        mergeGridVertical()
        leftToRight()
        transposeToLevel()

    random_num()
    show_num()

    endGame()

    print(f'分数={score}')


def compressGridLevel():
    """水平方向移动压缩"""
    global gridCell_num
    compressedCell = [[0] * columns for i in range(rows)]
    for row in range(rows):
        compressed_column = 0
        for column in range(columns):
            if gridCell_num[row][column] != 0:
                compressedCell[row][compressed_column] = gridCell_num[row][column]
                compressed_column += 1
    gridCell_num = compressedCell
    # print(gridCell_num)


def compressGridVertical():
    """竖直方向转置后移动压缩"""
    global gridCell_num
    compressedCell = [[0] * rows for i in range(columns)]
    for row in range(columns):
        compressed_column = 0
        for column in range(rows):
            if gridCell_num[row][column] != 0:
                compressedCell[row][compressed_column] = gridCell_num[row][column]
                compressed_column += 1
    gridCell_num = compressedCell


def transposeToVertical():
    """水平转竖直"""
    global gridCell_num
    transposeCell = [[0] * rows for i in range(columns)]
    # print(transposeCell)
    for row in range(rows):
        for column in range(columns):
            transposeCell[column][row] = gridCell_num[row][column]
    gridCell_num = transposeCell


def transposeToLevel():
    """竖直转水平"""
    global gridCell_num
    transposeCell = [[0] * columns for i in range(rows)]
    for row in range(columns):
        for column in range(rows):
            transposeCell[column][row] = gridCell_num[row][column]
    gridCell_num = transposeCell


def leftToRight():
    """左右倒置"""
    global gridCell_num
    left_to_right_num = []
    for rows_num in gridCell_num:
        rows_num_new = rows_num[::-1]
        left_to_right_num.append(rows_num_new)
    gridCell_num = left_to_right_num


def mergeGridLevel():
    global score, can_merge
    # can_merge = False
    for row in range(rows):
        for column in range(columns - 1):
            if gridCell_num[row][column] == gridCell_num[row][column + 1]:
                gridCell_num[row][column] *= 2
                gridCell_num[row][column + 1] = 0
                score += gridCell_num[row][column]
                can_merge = True


def mergeGridVertical():
    global score, can_merge
    # can_merge = False
    for row in range(columns):
        for column in range(rows - 1):
            if gridCell_num[row][column] == gridCell_num[row][column + 1]:
                gridCell_num[row][column] *= 2
                gridCell_num[row][column + 1] = 0
                score += gridCell_num[row][column]
                can_merge = True


def endGame():
    for row in range(rows):
        for column in range(columns):
            if can_merge == False or gridCell_num[row][column] == max_num:
                messagebox.showinfo(title='提示', message=f'游戏结束，最高分{score}')
                break


if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry('500x300+100+100')
    root.title('Game_2048 V1.0.1')
    create_widget()
    root.mainloop()
