from tkinter import *
from tkinter import messagebox
import random
class Board:
    bg_colors = {'2':'#d878f5','4':'#c86fe3','8':'#b665cf','16':'#a45bba','32':'#9251a6', '64':'#804791',
             '128':'#673975','256':'#a039bf','512':'#8a30a6','1024':'#68247d','2048':'#64107d'}
    
    colors = {'2':'#262326','4':'#262326','8':'#262326','16':'#262326','32':'#262326','64':'#262326',
             '128':'#262326','256':'#262326','512':'#262326','1024':'#262326','2048':'#262326'}
    
    def __init__(self):
        self.n = 4
        self. main_win = Tk()
        self.main_win.title('2048 Game')
        self.gridTiles = [[0]*4 for i in range(4)]
        self.board = []
        self.score = 0
        self.compress = False
        self.merge = False
        self.moved = False
        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.main_win,
                          bg='black',
                          text='',
                          font=('arial',26,'bold'),
                          width = 4,
                          height = 2)
                l.grid(row=i,column=j,padx=2,pady=2)
                rows.append(l)
            self.board.append(rows)
        s = Label(self.main_win,text="score",font=('arial',26),width=6,height=2,fg='#8a30a6',bg='white')
        num = Label(self.main_win,text=str(self.score),font=('arial',26),width=6,height=2,fg='#8a30a6',bg='white')
        s.grid(row=0,column=4)
        num.grid(row=1,column=4)
        


    def paint_grid(self):
        for i in range(4):
            for j in range(4):
                if self.gridTiles[i][j] == 0:
                    self.board[i][j].config(text='',bg='black')
                else:
                    self.board[i][j].config(text=str(self.gridTiles[i][j]),
                                            bg=self.bg_colors.get(str(self.gridTiles[i][j])),
                                            fg=self.colors.get(str(self.gridTiles[i][j])))
        num = Label(self.main_win,text=str(self.score),font=('arial',26),width=6,height=2,bg='white',fg='#8a30a6')
        num.grid(row=1,column=4)
   
    def random_tile(self):
        tiles = []
        for i in range(4):
            for j in range(4):
                if self.gridTiles[i][j] == 0:
                    tiles.append((i,j))
        curr = random.choice(tiles)
        i = curr[0]
        j = curr[1]
        self.gridTiles[i][j] = 2
        values = [2,4]
        self.gridTiles[i][j]=random.choice(values)

    def reverse(self):
        for ind in range(4):
            i=0
            j=3
            while(i<j):
                self.gridTiles[ind][i], self.gridTiles[ind][j]= self.gridTiles[ind][j], self.gridTiles[ind][i]
                i+=1
                j-=1

    def compress_grid(self):
        self.compress=False
        temp=[[0] *4 for i in range(4)]
        for i in range(4):
            count=0
            for j in range(4):
                if self.gridTiles[i][j]!=0:
                    temp[i][count]=self.gridTiles[i][j]
                    if count!=j:
                        self.compress=True
                    count+=1
        self.gridTiles=temp

    def can_merge(self):
        for i in range(3):
            for j in range(4):
                return self.gridTiles[i+1][j] == self.gridTiles[i][j]
        for i in range(4):
            for j in range(3):
                return self.gridTiles[i+1][j] == self.gridTiles[i][j]

    def merge_grid(self):
        self.merge = False
        for i in range(4):
            for j in range(3):
                if self.gridTiles[i][j] == self.gridTiles[i][j+1] and self.gridTiles[i][j] != 0:
                    self.gridTiles[i][j] *= 2
                    self.gridTiles[i][j+1] = 0
                    self.score += self.gridTiles[i][j]
                    self.merge = True

    def transpose(self):
        self.gridTiles = [list(t) for t in zip(*self.gridTiles)]
        


class Game:
    def __init__(self,gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False

    def start(self):
        self.gamepanel.random_tile()
        self.gamepanel.random_tile()
        self.gamepanel.paint_grid()
        self.gamepanel.main_win.bind('<Key>',self.link_keys)
        self.gamepanel.main_win.mainloop()

    def link_keys(self,event):
        if self.end or self.won:
            return
        
        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False

        pressed_key = event.keysym

        if pressed_key == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.compress_grid()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_grid()
            self.gamepanel.transpose()

        elif pressed_key == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compress_grid()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_grid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
        elif presed_key=='Left':
            self.gamepanel.compress_grid()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_grid()
        elif presed_key=='Right':
            self.gamepanel.reverse()
            self.gamepanel.compress_grid()
            self.gamepanel.merge_grid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compress_grid()
            self.gamepanel.reverse()
        else:
            pass

        self.gamepanel.paint_grid()
        print(self.gamepanel.score)

        flag=0

        for i in range(4):
            for j in range(4):
                if(self.gamepanel.gridTiles[i][j] == 2048):
                    flag = 1
                    break
        if(flag==1):
            self.won = True
            messagebox.showinfo('2048',message='You Wonn!!')
            print('won')
            return

        for i in range(4):
            for j in range(4):
                if self.gamepanel.gridTiles[i][j]==0:
                    flag=1
                    break

        if not (flag or self.gamepanel.can_merge()):
            self.end = True
            messagebox.showinfo('2048','Game Over!!!')
            print('Over')

        if self.gamepanel.moved:
            self.gamepanel.random_tile()

        self.gamepanel.paint_grid()

        


gamepanel = Board()
game = Game(gamepanel)
game.start()




