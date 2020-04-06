from elements import Che
from elements import Ma
from elements import Xiang
from elements import Shi
from elements import Shuai
from elements import Bing
from elements import Pao

class Chessboard():
    def __init__(self):
        self.red_move = True
        board = [0] * 9
        for i in range(9):
            board[i] = [0] * 10
        self.chessboard = board
        self.chessboard[0][6] = Bing(0, 6) 
        self.chessboard[2][6] = Bing(2, 6) 
        self.chessboard[4][6] = Bing(4, 6) 
        self.chessboard[6][6] = Bing(6, 6) 
        self.chessboard[8][6] = Bing(8, 6) 
        self.chessboard[1][7] = Pao(1, 7) 
        self.chessboard[7][7] = Pao(7, 7) 
        self.chessboard[0][9] = Che(0, 9)
        self.chessboard[8][9] = Che(8, 9) 
        self.chessboard[1][9] = Ma(1, 9) 
        self.chessboard[7][9] = Ma(7, 9) 
        self.chessboard[2][9] = Xiang(2, 9) 
        self.chessboard[6][9] = Xiang(6, 9) 
        self.chessboard[3][9] = Shi(3, 9) 
        self.chessboard[5][9] = Shi(5, 9) 
        self.chessboard[4][9] = Shuai(4, 9) 
        self.chessboard[0][3] = Bing(0, 3, red = False) 
        self.chessboard[2][3] = Bing(2, 3, red = False) 
        self.chessboard[4][3] = Bing(4, 3, red = False) 
        self.chessboard[6][3] = Bing(6, 3, red = False) 
        self.chessboard[8][3] = Bing(8, 3, red = False) 
        self.chessboard[1][2] = Pao(1, 2, red = False) 
        self.chessboard[7][2] = Pao(7, 2, red = False) 
        self.chessboard[0][0] = Che(0, 0, red = False) 
        self.chessboard[8][0] = Che(8, 0, red = False) 
        self.chessboard[1][0] = Ma(1, 0, red = False) 
        self.chessboard[7][0] = Ma(7, 0, red = False) 
        self.chessboard[2][0] = Xiang(2, 0, red = False) 
        self.chessboard[6][0] = Xiang(6, 0, red = False) 
        self.chessboard[3][0] = Shi(3, 0, red = False) 
        self.chessboard[5][0] = Shi(5, 0, red = False) 
        self.chessboard[4][0] = Shuai(4, 0, red = False) 

    def check(self, position):# 判断坐标是否在棋盘内
        x, y = position
        if x < 0 or y < 0:
            return False
        if x > 8 or y > 9:
            return False
        return True

    def can_move(self, start_position, end_position):
        x, y = start_position
        if not self.check(start_position) or not self.check(end_position):#位置越界
            return False
        if self.chessboard[x][y] == 0:# 出发的位置不存在棋子
            return False
        if self.red_move:#走棋颜色错误
            if not self.chessboard[x][y].red:
                return False 
        else:
            if self.chessboard[x][y].red:
                return False 
        if not self.chessboard[x][y].move(start_position, end_position, self.chessboard):#该棋子不能动
            return False
        self.red_move = not self.red_move
        z, w = end_position
        self.chessboard[z][w] = self.chessboard[x][y]
        self.chessboard[x][y] = 0
        return True