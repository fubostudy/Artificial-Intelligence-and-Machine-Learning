import random
searchtimes = 0
total_solution = 0

class Nqueen(object):

    # 用于外部调用
    def NQueen_back(self, n):
        self.check_state_back([-1] * n, 0, n)

    # 检查是否达到目标状态，是则输出，否则继续搜索
    def check_state_back(self, columnlist, row, n):
        if row == n:
            global total_solution
            total_solution += 1
            self.output(columnlist, n)
            return

        for column in range(n):
            columnlist[row] = column
            global searchtimes
            searchtimes += 1
            if self.check_legal_back(columnlist, row):
                # 如果合法，则进入下一行的搜索
                self.check_state_back(columnlist, row + 1, n)

    # 因为按照行进行排列，因此只需考虑同一列或同一斜线的情况
    def check_legal_back(self, columnlist, row):
        if len(set(columnlist[0:row + 1])) != len(columnlist[0:row + 1]):
            # 是否在同一列上，若是，set之后的len会比list状态的小
            return False

        for i in range(row):
            if abs(columnlist[i] - columnlist[row]) == int(row - i):
                # 是否在同一斜线上
                return False
        return True

    # 评价函数，用于判断当前状态存在的冲突数
    def conflict_judge(self,columnlist):
        conflict_num = 0
        for i in range(len(columnlist)):
            for j in range(i + 1, len(columnlist)):
                # 是否为同一列
                if columnlist[i] == columnlist[j]:
                    conflict_num += 1
                diagonal_judge = j - i
                if abs(columnlist[i] - columnlist[j]) == diagonal_judge:
                # 是否为对角线
                    conflict_num += 1
        return conflict_num

    # 选择冲突数最少的状态xxf
    def climb(self,columnlist):
        convert = {}
        length = len(columnlist)
        for row in range(length):
            for col in range(length):
                if (columnlist[row] == col):
                    continue
                columnlist_copy = list(columnlist)
                columnlist_copy[row] = col
                convert[(row, col)] = self.conflict_judge(columnlist_copy) # 记录每个后继状态的冲突数

        answers = []  # 最佳后继集合
        conflict_now = self.conflict_judge(columnlist)  # 当前冲突数

        # 遍历所有后继，找出冲突数最少的后继
        for key, value in convert.items():
            if value < conflict_now:
                conflict_now = value
        for key, value in convert.items():
            if value == conflict_now:
                answers.append(key)

        # 如果最佳后继多于一个则随机选择
        if len(answers) > 0:
            x = random.randint(0, len(answers) - 1)
            col = answers[x][1]
            row = answers[x][0]
            columnlist[row] = col

        return columnlist

    # 生成初始状态，并且当冲突数大于0时不断进行爬山xxf
    def Nqueen_climb(self,n):
        columnlist = [-1]*n
        for index in range(n):
            # 初始状态随机生成
            random_ini = random.randint(0, n-1)
            columnlist[index] = random_ini
        self.output(columnlist,n)

        while self.conflict_judge(columnlist) > 0:
            global searchtimes
            searchtimes += 1
            columnlist = self.climb(columnlist)
            #print(columnlist)
            #print(self.conflict_judge(columnlist))
        self.output(columnlist, n)

    def output(self, columnlist, n):
        for row in range(n):
            line = ""
            for column in range(n):
                if columnlist[row] == column:
                    line += "1 "
                else:
                    line += "0 "
            print(line, "\n")
        # 将解的状态和搜索的次数输出
        print('searchtimes:', searchtimes ,'\n')

if __name__ == '__main__': #xxf
    n = int(input('请输入皇后数量\n'))
    type=input('请选择解决算法:\na.回溯法\tb.爬山法\n')
    if(type == 'a'):
        Nqueen().NQueen_back(n)
        print('total_solution:', total_solution, '\n')
    if (type == 'b'):
        Nqueen().Nqueen_climb(n)


