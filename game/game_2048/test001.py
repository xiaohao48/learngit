import copy
import random

class Matrix2048():
    def __init__(self, column: int = 4):
        self.column = column
        self.matrix = [[0 for i in range(column)] for li in range(column)]
        self.history = []
        self.score = 0
        self.init()

    # 生成新的数字
    def generate_number(self):
        matrix = self.matrix
        column = self.column
        # 找出所有为0的位置
        zero = [(x, y) for x in range(column)
                for y in range(column) if matrix[x][y] == 0]
        # 随机选择一个为0的位置并填充为随机数字
        if zero != []:
            x, y = random.choice(zero)
            matrix[x][y] = random.choice([2, 2])

    # 判断游戏是否结束 结束则返回True， 否则返回False
    def gameover(self) -> bool:
        matrix = self.matrix
        column = self.column
        # 1. 矩阵(self.matrix)中有0则未结束
        if 0 in [i for li in matrix for i in li]:
            return False

        # 2. 水平方向上有相同的数字则未结束
        for row in range(column):
            for col in range(column-1):
                if matrix[row][col] == matrix[row][col+1]:
                    return False

        # 3. 垂直方向上有相同的数字则未结束
        for row in range(column-1):
            for col in range(column):
                if matrix[row][col] == matrix[row+1][col]:
                    return False
        return True

    # 游戏初始化 用于新建游戏或重置游戏
    def init(self):
        self.matrix = [[0 for x in range(self.column)]
                       for y in range(self.column)]
        self.generate_number()
        self.generate_number()

        self.history = []
        self.score = 0

    # 移动合并 并记录历史数据
    def matrix_move(self, direction):
        if direction in ['L', 'R', 'D', 'U']:

            # 记录历史
            prev_step = {
                'score': copy.deepcopy(self.score),
                'matrix': copy.deepcopy(self.matrix)
            }
            self.history.append(prev_step)
            # 只记录最近10次
            if len(self.history) > 10:
                self.history = self.history[-10:]
            if direction == 'U':
                self.move_up()
            if direction == 'D':
                self.move_down()
            if direction == 'L':
                self.move_left()
            if direction == 'R':
                self.move_right()

    # 向左移动合并
    def move_left(self):
        column = self.column
        matrix = self.matrix

        # 数字左移
        def move_left_(matrix):
            for row in range(column):
                while 0 in matrix[row]:
                    matrix[row].remove(0)
                while len(matrix[row]) != column:
                    matrix[row].append(0)
            return matrix

        # 数字向左合并
        def merge_left(matrix):
            for row in range(column):
                for col in range(column-1):
                    if matrix[row][col] == matrix[row][col+1] and matrix[row][col] != 0:
                        matrix[row][col] = 2 * matrix[row][col]
                        matrix[row][col+1] = 0
                        self.score = self.score + matrix[row][col]
            return matrix

        matrix = move_left_(matrix)
        matrix = merge_left(matrix)
        self.matrix = move_left_(matrix)

    # 向右移动合并
    def move_right(self):
        self.matrix = [li[::-1] for li in self.matrix]
        self.move_left()
        self.matrix = [li[::-1] for li in self.matrix]

    # 向上移动合并
    def move_up(self):
        column = self.column

        self.matrix = [[self.matrix[x][y]
                        for x in range(column)] for y in range(column)]
        self.move_left()
        self.matrix = [[self.matrix[x][y]
                        for x in range(column)] for y in range(column)]

    # 向下移动合并
    def move_down(self):
        self.matrix = self.matrix[::-1]
        self.move_up()
        self.matrix = self.matrix[::-1]

    # 返回上一步
    def prev_step(self):
        if self.history:
            prev_data = self.history[-1]
            self.score = prev_data['score']
            self.matrix = prev_data['matrix']
            self.history = self.history[0:-1]

    # 命令行显示
    def show(self):
        r = '+-----' * self.column + '+\n'
        for li in self.matrix:
            for i in li:
                s = '|' + ' '*5 if i == 0 else '|' + str(i).center(5, ' ')
                r = r + s
            r = r + '|\n' + '+-----' * self.column + '+\n'
        print(r)