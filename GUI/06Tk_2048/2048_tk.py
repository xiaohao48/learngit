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
score = 0
max_num = 2048
can_merge = True
row_var = 0
column_var = 0
max_num_var = 0
is_over = False


def create_widget():
    init_page()
    # start_game()
    # create_squ(game_frame)  # 创建游戏区域


def init_page():
    global row_var, column_var, max_num_var, max_score_show_lb
    # root.geometry('300x300+100+100')
    max_num_lb = tk.Label(start_frame, text='合成最大值：')
    max_num_lb.pack()
    max_num_var = tk.StringVar(value=2048)
    max_num_entry = tk.Entry(start_frame, text=max_num_var)
    max_num_entry.pack()
    row_lb = tk.Label(start_frame, text='游戏区域行数：')
    row_lb.pack()
    row_var = tk.StringVar(value=4)
    row_entry = tk.Entry(start_frame, text=row_var)
    row_entry.pack()
    column_lb = tk.Label(start_frame, text='游戏区域列数：')
    column_lb.pack()
    column_var = tk.StringVar(value=4)
    column_entry = tk.Entry(start_frame, text=column_var)
    column_entry.pack()
    max_score_lb = tk.Label(start_frame, text='游戏最高分:')
    max_score_lb.pack()
    max_score_show_lb = tk.Label(start_frame, text=score, bg='yellow')
    max_score_show_lb.pack()
    confirm_bt = tk.Button(start_frame, text='确定', command=confirm_game)
    confirm_bt.pack()


def start_game():
    create_squ(game_frame)  # 创建游戏区域
    random_num()  # 初始化随机生成1个数字
    random_num()  # 初始化随机生成1个数字
    show_num()  # 展示数字
    root.bind('<Key>', move)  # 移动操作


def confirm_game():
    global rows, columns, max_num, gridCell_num, score, gridCell_label
    score = 0
    rows = int(row_var.get())
    columns = int(column_var.get())
    max_num = int(max_num_var.get())
    gridCell_num = [[0] * columns for n in range(rows)]
    gridCell_label = []
    start_frame.pack_forget()
    game_frame.pack()
    start_game()


def create_squ(master):
    """使用label创建游戏区域"""
    for row in range(rows):
        row_cells = []
        for column in range(columns):
            label = tk.Label(master, text='', bg='azure4', font=('arial', 22), width=4, height=2)
            label.grid(row=row, column=column, padx=5, pady=5)
            row_cells.append(label)
        gridCell_label.append(row_cells)


def random_num():
    global is_over
    random_cells = []
    for row in range(rows):
        for column in range(columns):
            if gridCell_num[row][column] == 0:
                random_cells.append((row, column))
    if len(random_cells) > 0:
        random_cell = random.choice(random_cells)
        random_text = random.choice([2, 4])
        gridCell_num[random_cell[0]][random_cell[1]] = random_text
        # print('row=' + str(random_cell[0]),
        #       'columu=' + str(random_cell[1]),
        #       'random_text=' + str(random_text),
        #       'lineno=' + str(sys._getframe().f_lineno))
    # elif random_cells == []:
    else:
        # messagebox.showinfo(title='提示', message='Game over!')
        is_over = True


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
    pressed_key = event.keysym
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
    # if is_over == True:
    #     endGame()

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
            if gridCell_num[row][column] == max_num or is_over is True:
                messagebox.showinfo(title='提示', message=f'游戏结束，最高分{score}')
                game_frame.pack_forget()
                start_frame.pack()
                max_score_show_lb['text'] = score
                break


if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry('500x300+100+100')
    root.title('Game_2048 V1.0.1')
    start_frame = tk.Frame(root)
    start_frame.pack()
    game_frame = tk.Frame(root)
    create_widget()
    root.mainloop()
