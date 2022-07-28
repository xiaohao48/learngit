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
num_list = [['' for m in range(columns)] for n in range(rows)]


def create_widget():
    create_squ()  # 创建游戏区域
    init_random()  # 初始化随机生成2个数字

    root.bind('<Key>', move)  # 移动操作


def create_squ():
    """使用label创建游戏区域"""
    for row in range(rows):
        for column in range(columns):
            num_list[row][column] = tk.Label(root, text='', bg='azure4', font=('arial', 22), width=4, height=2)
            num_list[row][column].grid(row=row, column=column, padx=5, pady=5)


def random_num():
    random_row = random.randint(1, rows)
    random_column = random.randint(1, columns)
    random_text = random.choice([2, 4])
    # num_list[random_row - 1][random_column - 1]['text'] = random_text
    return [random_row, random_column, random_text, num_list[random_row - 1][random_column - 1]]


def init_random():
    """初始化随机两个2"""
    random_list = []
    while True:
        random_1 = random_num()
        random_2 = random_num()
        print(random_1, random_2, sys._getframe().f_lineno)
        if random_1[0] != random_2[0] or random_1[1] != random_2[1]:
            random_list.append(random_1)
            random_list.append(random_2)
            # show_num()  # 展示数字
            # print(random_list)
        if len(random_list) == 2:
            break
        # print(random_list)
    num_list[random_list[0][0] - 1][random_list[0][1] - 1]['text'] = random_list[0][2]
    num_list[random_list[1][0] - 1][random_list[1][1] - 1]['text'] = random_list[1][2]
    show_num()
    print(random_list, sys._getframe().f_lineno)


def show_num():
    """展示数字颜色"""
    for row in range(rows):
        for column in range(columns):
            if str(num_list[row][column]['text']) in bg_color.keys():
                num_list[row][column].config(bg=bg_color[str(num_list[row][column]['text'])],
                                             fg=fg_color[str(num_list[row][column]['text'])])
            else:
                num_list[row][column].config(bg='azure4')


def create_new_grid():
    null_num = []
    for row in range(rows):
        for column in range(columns):
            if num_list[row][column]['text'] == '':
                null_num.append((row, column))
    if len(null_num) > 0:
        random_null = random.choice(null_num)
        random_text = random.choice([2, 4])
        num_list[random_null[0]][random_null[1]]['text'] = random_text
        null_num.remove(random_null)
        print(random_null)
        show_num()  # 展示数字
    print(null_num)


def create_new_grid2():
    ...


def move(event):
    derictions = {
        'Up': "print('up')",
        'Down': "print('down')",
        'Left': left(),
        'Right': "print('right')",
    }
    # sys._getframe().f_lineno
    print(event.keysym, sys._getframe().f_lineno)
    if event.keysym in derictions.keys():
        # print(derictions[event.keysym])
        derictions[event.keysym]


def left():
    for row in range(0, rows):
        # for column in range(0, columns - 1):
        column = 0
        while column < columns - 1:
            print(str(num_list[row][column]['text']))
            if str(num_list[row][column]['text']) == '':
                num_list[row][column]['text'], num_list[row][column + 1]['text'] = num_list[row][column + 1]['text'], \
                                                                                   num_list[row][column]['text']
                show_num()
                print(num_list[row][column]['text'])
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
