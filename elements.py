class Chess():
    def __init__(self, x, y, red=True, selected=False):
        self.x = x
        self.y = y
        self.red = red

    def position(self):#获取位置
        return (self.x,self.y)
    
    def set_position(self, pos):
        self.x, self.y = pos
        
    def d_position(self, start_position, end_position):#位移差
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        return dx, dy

    def is_myplace(self, y):#判断兵,象是否过河
        if self.red and y > 4:
            return True
        elif not self.red and y < 5:
            return True
        return False

    def is_out(self, pos):#检查是否越界
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True

    def move(self, start_position, end_position, chessboard):#棋子移动
        if self.can_move(start_position, end_position, chessboard):
            self.x = end_position[0]
            self.y = end_position[1]
            return True
        return False
   
    def position_has_chess(self, position, chessboard):#判断某个位置是否有棋子
        x, y = position
        if chessboard[x][y] == 0:
            return False
        return True
    
    def chess_is_my(self, red, chess):#判断是否为己方棋子
        if red == chess.red:
            return True
        return False

    def count_chess(self, start_position, end_position ,chessboard):# 计算起点和终点直线之间的棋子
        x, y = start_position
        z, w = end_position
        dx, dy = self.d_position(start_position, end_position)
        sx = dx/abs(dx) if dx != 0 else 0
        sy = dy/abs(dy) if dy != 0 else 0
        num = 0
        while x != z or y != w:
            x = int(x+sx)
            y = int(y+sy)
            if chessboard[x][y]:
                num += 1
        return num

class Bing(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Bing, self).__init__(x, y, red=True, selected=False)
        self.name = '兵'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_pawn.gif'
        else:
            return 'black_pawn.gif'

    def rule(self, dx, dy):
        if abs(dx) + abs(dy) != 1:
            return False
        if self.is_myplace(self.y):#兵没有过河
            if self.red and dy == -1:
                return True
            if not self.red and dy == 1:
                return True
            return False
        else:#兵已过河
            if self.red and dy == 1:
                return False
            if not self.red and dy == -1:
                return False
            return True
         
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        if self.rule(dx, dy):#走棋合法
            if not self.position_has_chess(end_position, chessboard):#移动到的位置没棋子
                return True
            else:
                if self.chess_is_my(self.red, chessboard[x][y]):#本方棋子，不能吃
                    return False
                else:# 对方棋子，可以吃
                    return True
        else:
            return False
    
    def try_move(self, position, chessboard):# 返回棋子能够移动的所有位置
        x, y = position
        a = [(x+1, y),(x-1, y),(x, y+1),(x, y-1)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b

class Che(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Che, self).__init__(x, y, red=True, selected=False)
        self.name = '车'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_rook.gif'
        else:
            return 'black_rook.gif'

    def rule(self, dx, dy):
        if not (dx == 0 and dy == 0):
            if dx == 0 or dy == 0:
                return True
        return False
         
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        if self.rule(dx, dy):
            num = self.count_chess(start_position, end_position, chessboard)#路线上是否有子阻挡
            if not num:#没有子
                return True
            if num == 1 and self.position_has_chess(end_position, chessboard):#终点位置有子
                if not self.chess_is_my(self.red, chessboard[x][y]):#不是本方子
                    return True
            return False
        else:
            return False

    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x+5,y),(x+6,y),(x+7,y),(x+8,y),
                (x-1,y),(x-2,y),(x-3,y),(x-4,y),(x-5,y),(x-6,y),(x-7,y),(x-8,y),
                (x,y+1),(x,y+2),(x,y+3),(x,y+4),(x,y+5),(x,y+6),(x,y+7),(x,y+8),(x,y+9),
                (x,y-1),(x,y-2),(x,y-3),(x,y-4),(x,y-5),(x,y-6),(x,y-7),(x,y-8),(x,y-9)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b


class Ma(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Ma, self).__init__(x, y, red=True, selected=False)
        self.name = '马'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_knight.gif'
        else:
            return 'black_knight.gif'

    def rule(self, dx, dy):
        if dx == 0 or dy == 0:
            return False
        if abs(dx) + abs(dy) == 3:#马走日
            return True
         
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        if self.rule(dx, dy) and not self.block(start_position, dx, dy, chessboard):
            if not self.position_has_chess(end_position, chessboard):#不吃子
                return True
            else:# 吃子
                if not self.chess_is_my(self.red, chessboard[x][y]):#不是本方棋子
                    return True
        return False
    
    def block(self, start_position, dx, dy, chessboard):#别马腿
        x, y = start_position
        if abs(dx) == 1:
            y = int(y + dy/2)
            if chessboard[x][y] == 0:
                return False
        else:
            x = int(x + dx/2)
            if chessboard[x][y] == 0:
                return False
        return True
   
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y+2),(x+2,y+1),(x-1,y+2),(x-2,y+1),(x-1,y-2),(x-2,y-1),(x+1,y-2),(x+2,y-1)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b

class Pao(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Pao, self).__init__(x, y, red=True, selected=False)
        self.name = '炮'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_cannon.gif'
        else:
            return 'black_cannon.gif'

    def rule(self, dx, dy):
        if not (dx == 0 and dy == 0):
            if dx == 0 or dy == 0:
                return True
        return False
         
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        if self.rule(dx, dy):
            num = self.count_chess(start_position, end_position, chessboard)
            if not num:#移动的路线上没子
                return True
            if num == 2 and self.position_has_chess(end_position, chessboard):#有两个子且一个在终点处
                if not self.chess_is_my(self.red, chessboard[x][y]):
                    return True
        return False

    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x+5,y),(x+6,y),(x+7,y),(x+8,y),
                (x-1,y),(x-2,y),(x-3,y),(x-4,y),(x-5,y),(x-6,y),(x-7,y),(x-8,y),
                (x,y+1),(x,y+2),(x,y+3),(x,y+4),(x,y+5),(x,y+6),(x,y+7),(x,y+8),(x,y+9),
                (x,y-1),(x,y-2),(x,y-3),(x,y-4),(x,y-5),(x,y-6),(x,y-7),(x,y-8),(x,y-9)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b

class Shi(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Shi, self).__init__(x, y, red=True, selected=False)
        self.name = '士'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_mandarin.gif'
        else:
            return 'black_mandarin.gif'

    def rule(self, dx, dy, end_position):
        x, y = end_position
        if abs(dx) == 1 and abs(dy) == 1:
            if self.red and 2 < x < 6 and 6 < y < 10:# 判断是否出九宫格
                return True
            if not self.red and 2 < x < 6 and -1 < y < 3:
                return True
        return False
 
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        if self.rule(dx, dy, end_position):
            if not self.position_has_chess(end_position, chessboard):#终点处无棋子
                return True
            elif not self.chess_is_my(self.red, chessboard[x][y]):#终点处是对方棋子
                return True
        return False
   
    def try_move(self, position, chessboard):
        x, y = position
        a = [(x+1,y+1),(x-1,y+1),(x-1,y-1),(x+1,y-1)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b

class Shuai(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Shuai, self).__init__(x, y, red=True, selected=False)
        self.name = '帅'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_king.gif'
        else:
            return 'black_king.gif'

    def rule(self, dx, dy, end_position):
        x, y = end_position
        if abs(dx) + abs(dy) == 1:
            if self.red and 2 < x < 6 and 6 < y < 10:
                return True
            if not self.red and 2 < x < 6 and -1 < y < 3:
                return True
        return False
 
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        for i in chessboard:#判断是否有白脸将
            for p in i:
                if p == 0: 
                    continue
                if p.name == '帅':
                    if p.red != self.red:
                        a = p
        x1, y1 = a.position()
        if x1 == x:
            if y1 > y:
                c = y1
                y1 = y
                y = c
            flag = 0
            for i in range(y1+1, y):
                if chessboard[x1][i]:
                    flag = 1
            if flag == 0:
                return False
        if self.rule(dx, dy, end_position):
            if not self.position_has_chess(end_position, chessboard):#终点处无棋子
                return True
            elif not self.chess_is_my(self.red, chessboard[x][y]):#终点处是对方棋子
                return True
        return False
    
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b

class Xiang(Chess):
    def __init__(self, x, y, red=True, selected=False):
        super(Xiang, self).__init__(x, y, red=True, selected=False)
        self.name = '象'
        self.red = red

    def picture(self):
        if self.red:
            return 'red_elephant.gif'
        else:
            return 'black_elephant.gif'

    def rule(self, dx, dy):
        if abs(dx) == 2 and abs(dy) == 2:
            return True
        return False
 
    def xiangti(self, start_position, end_position, dx, dy, chessboard):# 是否别象眼或象过河
        x, y = start_position
        z, w = end_position
        x = int(x+dx/2)
        y = int(y+dy/2)
        if chessboard[x][y] == 0:
            return False
        if self.red and w < 5:#象是否过河
            return False
        if not self.red and w > 4:
            return False
        return True

    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx, dy = self.d_position(start_position, end_position)
        if self.rule(dx, dy) and not self.xiangti(start_position, end_position, dx, dy, chessboard):
            if not self.position_has_chess(end_position, chessboard):#终点处无棋子
                return True
            elif not self.chess_is_my(self.red, chessboard[x][y]):#终点处是对方棋子
                return True
        return False

    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+2,y+2),(x-2,y+2),(x-2,y-2),(x+2,y-2)]
        b = []
        for i in a:
            if not self.is_out(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b