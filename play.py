from center import Chessboard
import pygame
import os

data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'source')

class background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('boardchess.gif')

class add_chess(pygame.sprite.Sprite):
    def __init__(self, name, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name)
        x, y = position
        self.rect.center = (x * 80 + 40, y * 80 + 40)#使得棋子位于棋盘图像中合适位置（小格内居中）
        self.position = position

    def move(self, position):
        x, y = position
        self.rect.center = (x * 80 + 40, y * 80 + 40)#使得棋子位于棋盘图像中合适位置（小格内居中）
        self.position = position

def mouse_to_side(position):#将鼠标点击位置转化为棋盘编号位置（0，0）-（9，10）
    a, b = position 
    return a//80, b//80

def load_image(name):
    filename = os.path.join(data_dir, name)
    surface = pygame.image.load(filename)
    return surface.convert(), surface.get_rect()

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(data_dir, 'easymode.wav'))
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((720,800))#设置屏幕大小为（720，800），方便对应棋子位置
    board = pygame.sprite.Group()#显示的图像
    board.add((background()))#加入背景图
    all_chess = pygame.sprite.Group()#所有棋子
    chess_board = Chessboard()#整个地图的元素
    for a in chess_board.chessboard:#a为每列所有元素
        for b in a:#b为a中每个位置的元素
            if b != 0:#该位置有棋子
                all_chess.add((add_chess(b.picture(), b.position())))#将该棋子加入所有棋子的集合中
    flag = 1 #是否继续进行游戏的标记
    from_side = (-1,-1) #棋子出发位置
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:#点击某处
                to_side = mouse_to_side(pygame.mouse.get_pos())#将点击位置转化为棋盘上坐标
                if chess_board.can_move(from_side, to_side):#棋子从出发位置到鼠标点击位置移动合法
                    for side in all_chess:#寻找移动的棋子位置
                        if side.position == to_side:#棋子被吃
                            side.kill()
                        if side.position == from_side:#棋子从出发位置移动
                            side.move(to_side)
                    from_side =  (-1,-1) #出发位置赋值为空
                else: #出发位置未赋值或者结束位置不合法
                    from_side = to_side #将出发位置设置为鼠标点击位置
            elif event.type == pygame.QUIT:#退出游戏
                flag = 0
        board.draw(screen)#显示棋盘背景
        all_chess.draw(screen)#显示所有棋子
        pygame.display.flip()