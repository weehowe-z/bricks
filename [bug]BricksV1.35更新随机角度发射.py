# -*- coding: cp936 -*-
import pygame
import sys
import os
from random import *
from math import *
#设定屏幕大小
screenSize = 600,600
#设定砖块大小
brickWidth = 60
brickHeight = 15
#设定挡板大小
baffleWidth = 80
baffleHeight = 12
#设定小球大小
radius = 8
diameter = 2*radius
#设定挡板移动速度
baffleVelocity = 5
#设定小球移动速度
ballVelocity = [5,5]
#设定最大移动范围
minXpos = 0
minBallXpos = 0
minBallYpos = 0
maxXpos = screenSize[0] - baffleWidth
maxBallXpos = screenSize[0] - diameter
maxBallYpos = screenSize[1] - diameter - 10
#设定挡板位置(均以左上角计）
baffleXpos = (screenSize[0] - baffleWidth)/2
baffleYpos = screenSize[1] - baffleHeight -10
#设定小球位置
ballXpos = screenSize[0]/2 - radius
ballYpos = baffleYpos -diameter 
#定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
brickColor = (184,134,11)

#定义状态常量
State_restarting = 0
State_playing = 1
State_win = 2
State_gameover = 3
State_highscore=4
State_stopping=5

#程序的封装
class Brick:
    def __init__(self):
        #初始化pygame模块
        pygame.init()

        #初始化混音器
        pygame.mixer.init()
        pygame.time.delay(1000)

        #创建游戏窗口
        self.screen = pygame.display.set_mode(screenSize,0)
#无边框版self.screen = pygame.display.set_mode(screenSize,pygame.NOFRAME)

        #设置窗口标题
        pygame.display.set_caption("Bricks by zwh")

        #将图像数据都转化为Surface对象
        self.background=pygame.image.load("bg.png").convert()

        #载入背景音乐
        self.soundwav=pygame.mixer.Sound("bgmusic.wav")
        #设定时钟
        self.clock = pygame.time.Clock()

        #载入字体 
        self.font = pygame.font.Font("Lancy.ttf",23)
        self.font2 = pygame.font.Font("Kevin.ttf",20)

        self.init_game()

    #读取最高分
    def highScore(self): 
        if os.path.isfile("highscore.dat"):
            highfile=open("highscore.dat","r")
            highscore=highfile.readline() 
            highfile.close() 
        else:
            highscore=0
        return highscore

    #游戏数据初始化（变化的）
    def init_game(self):
        #初始化生命得分和状态
        self.lives = 3
        self.score = 0
        self.level = 1
        #初始化小球速度
        self.ballVelocity = ballVelocity
        #读取最高分
        self.highscore = self.highScore()
        self.state = State_restarting
        #创建挡板和小球的矩形范围
        self.baffle = pygame.Rect(baffleXpos,baffleYpos,baffleWidth,baffleHeight)
        self.ball   = pygame.Rect(ballXpos,ballYpos,diameter,diameter)
        #执行创建砖块矩形函数
        self.create_bricks()

    #升级时数据更新
    def next_game(self):
        self.level+=1
        self.lives += 1
        self.state = State_restarting
        self.baffle = pygame.Rect(baffleXpos,baffleYpos,baffleWidth,baffleHeight)
        self.ball   = pygame.Rect(ballXpos,ballYpos,diameter,diameter)
        self.create_bricks()
        
    
    #创建砖块矩形范围
    def create_bricks(self):
        ypos= 30
        self.bricks = []
        for i in range(7):
            xpos = 25
            for j in range(8):
                self.bricks.append(pygame.Rect(xpos,ypos,brickWidth,brickHeight))
                xpos += brickWidth+ 10
            ypos += brickHeight + 5

    #画出砖块
    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brickColor, brick)
            #pygame.draw.ellipse(self.screen, brickColor, brick) 椭圆版 

    #侦测键盘输入控制平台位置    
    def keyInput(self):
        keys = pygame.key.get_pressed()

        #左键左移
        if keys[pygame.K_LEFT] and  self.state != State_stopping:
            self.baffle.left -= baffleVelocity
            if self.baffle.left <= minXpos:
                self.baffle.left = minXpos

        #右键右移
        if keys[pygame.K_RIGHT] and  self.state != State_stopping:
            self.baffle.left += baffleVelocity
            if self.baffle.left >= maxXpos:
                self.baffle.left = maxXpos
                
        #           太空版(测试Win使用）
        ##上键上移
        if keys[pygame.K_UP]:
            self.baffle.top -= baffleVelocity
        ##下键下移
        if keys[pygame.K_DOWN]:
            self.baffle.top += baffleVelocity
        
        #Space重置
        elif keys[pygame.K_SPACE] and self.state == State_restarting:
            self.ballVelocity= [4 + self.level,4 + self.level]
        #           随机角度发射（+-30°之间）
        #    base= (4+self.level)*2**0.5
        #    angle=randrange(-30,30)/180.0*pi
        #    self.ballVelocity= [base*sin(angle),-base*cos(angle)]
            self.state = State_playing

        #失败时回车重新启动
        elif keys[pygame.K_RETURN] and (self.state == State_gameover \
            or self.state == State_highscore):
            self.init_game()
        elif keys[pygame.K_RETURN] and self.state == State_win:
            self.next_game()
        #游戏时按回车暂停
        elif keys[pygame.K_RETURN] and self.state == State_playing:
            self.state = State_stopping
        elif keys[pygame.K_SPACE] and self.state == State_stopping:
            self.state = State_playing

    def move_ball(self):

        #移动距离 速度V*Δt(与帧数相关） 以左上角为标准
        self.ball.left += self.ballVelocity[0]
        self.ball.top  += self.ballVelocity[1]

        #碰壁反向
        if self.ball.left <= minBallXpos:
            self.ball.left = minBallXpos
            self.ballVelocity[0] *= -1
        elif self.ball.left >= maxBallXpos:
            self.ball.left = maxBallXpos
            self.ballVelocity[0] *= -1
        elif self.ball.top <= minBallYpos:
            self.ball.top = minBallYpos 
            self.ballVelocity[1] *= -1
        #触底静止
        elif self.ball.top >= maxBallYpos:            
            self.ball.top = maxBallYpos

    #碰撞处理
    def collision(self):

        #对于每一块砖块进行判断 加分 反弹 砖块消除
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 10*self.level
                self.ballVelocity[1] *= -1
                self.bricks.remove(brick)
                break
        #碰撞挡板反弹
        if self.ball.colliderect(self.baffle):
            self.ball.top = self.baffle.top - diameter
            self.ballVelocity[1] *= -1

        #状态判断模块
        if self.bricks == []:
            self.state = State_win
            
        elif self.ball.top == maxBallYpos:
            self.lives -= 1
            if self.lives > 0:
                self.state = State_restarting
            #死亡操作
            elif self.lives == 0 and self.score > int(self.highscore):
                self.state = State_highscore
            else:
                self.state = State_gameover
                
    def writeHighScore(self): #写入最高分
        highfile=open("highscore.dat","w")  
        highfile.writelines(str(self.score))  
        highfile.close()  
    
    #显示基本状态
    def show_stats(self):
        myRecord = self.font2.render("RECORD: " + str(self.highscore), True, WHITE)
        myScore = self.font2.render(" SCORE: " + str(self.score), True, WHITE)
        myLife = self.font2.render(" LIVES: " + str(self.lives), True, WHITE)
        myLevel = self.font.render(" LEVLE " + str(self.level), True, WHITE)
        self.screen.blit(myRecord, (450,5))
        self.screen.blit(myScore, (300,5))
        self.screen.blit(myLife, (200,5))
        self.screen.blit(myLevel, (0,0))
        #获取程序Fps
     #   self.fps=int(self.clock.get_fps())  #为了去掉末尾的小数
     #   myfps=self.font2.render("FPS: " + str(self.fps) , True, WHITE)
     #   self.screen.blit(myfps, (5,580))

    #显示关键信息模块
    def show_message(self,message):
            #获取字体大小使文字显示在中央
            size = self.font.size(message)
            font_surface = self.font.render(message,True, WHITE)
            x = (screenSize[0] - size[0]) / 2
            y = (screenSize[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
            
        
    #运行过程      
    def run(self):
        #播放背景音乐（-1表示循环)
        self.soundwav.play(-1)

        while True:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #控制帧数
            self.clock.tick(100)
            #生成背景
            self.screen.blit(self.background, (0,0))
             #self.screen.fill((0,0,0))#黑屏版
             #self.screen.fill((255,255,255))#白屏版

            #执行按键侦测
            self.keyInput()
            #判断游戏所处在的状态并给出相应反馈
            if self.state == State_playing:   #只有在该状态下才会触发移动和碰撞
                self.move_ball()
                self.collision()
            elif self.state == State_restarting:
                self.ball.left = self.baffle.left + self.baffle.width / 2 - radius
                self.ball.top  = self.baffle.top - self.ball.height
                self.show_message("Press SPACE to Launch the Ball")
            elif self.state == State_gameover:
                self.show_message("~Game over!~Press ENTER to retry")
            elif self.state == State_highscore:
                self.show_message("~New Record!!!~Press ENTER to play again")
                self.writeHighScore()
            elif self.state == State_win:
                self.show_message("~Congratulations!~Press ENTER to go")
            elif self.state == State_stopping:
                self.show_message("~Pause~")

            #画出砖块
            self.draw_bricks()
            #执行显示状态
            self.show_stats()
            #画出挡板
            pygame.draw.rect(self.screen, BLUE, self.baffle)
            #画出小球
            pygame.draw.circle(self.screen, WHITE, \
            (self.ball.left + radius, self.ball.top + radius), radius)

            #更新显示到屏幕表面
            pygame.display.flip()

myMasterpiece=Brick()
myMasterpiece.run()
