import tkinter as tk
import random, time


window = tk.Tk()
window.title("minesweeper")

class GUImines():
    width = 2  #一格寬度
    height = 1  #一格高度
    label_font = "Helvetica 14 bold"
    button_font = "Helvetica 10"
    translate = {0:("", "gray"), 1:("１", "darkorange"), 2:("２", "green"), 3:("３", "blue"), 4:("４", "indigo"),
                5:("５", "midnightblue"), 6:("６", "black"), 7:("７", "black"), 8:("８", "black"), 9:("Ｘ", "red")}
    @classmethod
    def setting(cls, list_xy, xd, yd, data, top_y, window):
        cls.list_xy = list_xy
        cls.xd = xd  #地圖寬度
        cls.yd = yd  #地圖高度
        cls.data = data
        cls.top_y = top_y
        cls.window = window
    
    def get_position(self, step = 1):
        pos_dict = {
            1:(self.list_xy[self.y + 1][self.x - 1][0], (self.x - 1, self.y + 1)), 2:(self.list_xy[self.y + 1][self.x][0], (self.x, self.y + 1)), 3:(self.list_xy[self.y + 1][self.x + 1][0], (self.x + 1, self.y + 1)),
            4:(self.list_xy[self.y][self.x - 1][0], (self.x - 1, self.y)), 10:(self.list_xy[self.y][self.x][0], (self.x, self.y)), 6:(self.list_xy[self.y][self.x + 1][0], (self.x + 1, self.y)),
            7:(self.list_xy[self.y - 1][self.x - 1][0], (self.x - 1, self.y - 1)), 8:(self.list_xy[self.y - 1][self.x][0], (self.x, self.y - 1)), 9:(self.list_xy[self.y - 1][self.x + 1][0], (self.x + 1, self.y - 1))
        }  #(數字鍵)
        return tuple([i[1] for i in pos_dict.items() if not i[0] % step])
    
    def __init__(self, x, y, bg="dimgray"):
        self.x = x
        self.y = y
        self.bg = bg
        self.label = tk.Label(self.window, font=self.label_font,
                              width=self.width, height=self.height, relief="flat", bg=self.bg)
        self.button = tk.Button(self.window, font=self.button_font,
                                width=self.width, height=self.height, relief="flat",
                                bg=self.bg, command=self.__btn_dig)
        self.label.grid(row=self.y + self.top_y + 1, column=self.x + 1)
        self.button.grid(row=self.y + self.top_y + 1, column=self.x + 1)

    def __btn_dig(self):
        self.blank = self.list_xy[self.y][self.x][0]
        if self.blank == 0:
            self.__dig()
            self.__check()
        elif self.blank == 9:
            self.__dig()
            self.gameover(word="Loss")
        elif self.blank > 0:
            self.__dig()
            self.__check(continue_TF = False)
    
    def __check(self, continue_TF = True):
        if continue_TF:
            for list_pos, pos in self.get_position():
                if list_pos != -1:
                    self.list_xy[pos[1]][pos[0]][1].__btn_dig()
        else:
            for list_pos, pos in self.get_position(2):
                if list_pos == 0:
                    self.list_xy[pos[1]][pos[0]][1].__btn_dig()
        if self.data[0] == self.data[1]:
            self.gameover()
    
    def __dig(self):
        try:
            self.label["text"], self.label["fg"] = self.translate[self.list_xy[self.y][self.x][0]]
            self.button.destroy()
            del self.button
            self.label["relief"] = "sunken"
            if self.label["bg"] == "dimgray":
                self.label["bg"] = "lightgray"
            else:
                self.label["bg"] = "whitesmoke"
            self.list_xy[self.y][self.x][0] = -1
            self.data[1] -= 1
        except: pass  #AttributeError
    
    def gameover(self, word = "Congratulation"):
        self.data.append(tk.Button(window, text=word, font="Helvetica 17 bold",
                        width=self.width * self.xd, height=self.height * (self.yd - 1), relief="flat",
                        fg="slategray", command=self.__btn_gameover))
        self.data[2].grid(row=self.top_y + 1, column=1, rowspan=self.yd, columnspan=self.xd)
    
    def __btn_gameover(self):
        self.data[2].destroy()
        del self.data[2]
        for y in range(self.yd):
            for x in range(self.xd):
                if self.list_xy[y][x][0] != -1:
                    self.list_xy[y][x][1].__dig()


class Ground():
    window = window
    width = 2  #一格寬度
    height = 1  #一格高度
    x_original = 0
    y_original = 0
    difficulty_dict = {12:("Easy", "limegreen"), 7:("Normal", "darkorange"), 4:("Hard", "crimson")}
    fill = lambda self, list_, lable: list_.append(lable)
    @classmethod
    def setting(cls, top_y=7):
        cls.difficulty = tk.IntVar()  #難度(越小越難)
        cls.difficulty.set(7)
        cls.top_y = top_y
        cls.top_lable = []
        cls.frame_top_lable, cls.frame_right_lable, cls.frame_bottom_lable, cls.frame_left_lable = [], [], [], []

    def __init__(self, xd, yd):
        self.xd = xd  #地圖寬度
        self.yd = yd  #地圖高度
        self.ground = list([[0, None][:] for i in range(xd + 1)[:]] for i in range(yd + 1))
        self.data = []

        self.x_add = self.xd + 2 - self.x_original
        self.y_add = self.yd - self.y_original
        
        self.data = [0, self.xd * self.yd]
        GUImines.setting(self.ground, self.xd, self.yd, self.data, self.top_y, self.window)
        for y in range(self.yd):
            for x in range(self.xd):
                if (x + y) % 2:
                    self.ground[y][x][1] = GUImines(x, y)
                else:
                    self.ground[y][x][1] = GUImines(x, y, "gray")
                
                if random.randint(0, self.difficulty.get()) == 0:
                    self.ground[y][x][0] = 9  #mine
                    self.data[0] += 1
                    for list_pos, pos in self.ground[y][x][1].get_position():
                        if list_pos != 9:
                            self.ground[pos[1]][pos[0]][0] += 1
        for y in range(self.yd): self.ground[y][self.xd][0] = -1
        for x in range(self.xd + 1): self.ground[self.yd][x][0] = -1
        self.top_Label()
        self.frame_Label()
        self.frame_Button()
    
    def delete(self):
        '''清空GUImines'''
        if len(self.data) == 3:
            self.data[2].destroy()
            del self.data[2]
        for y in range(self.yd):
            for x in range(self.xd):
                self.ground[y][x][1].label.destroy()
                if self.ground[y][x][0] != -1:
                    self.ground[y][x][1].button.destroy()
                del self.ground[y][x][:]
        
        self.exit_button.destroy()
        del self.exit_button

    
    def top_Label(self):
        '''選項區的背景'''
        original = self.x_original
        if self.x_add > 0:
            for i in range(self.x_add):
                x = original + i
                self.fill(self.top_lable, tk.Label(self.window, font="Helvetica 14 bold",
                                width=self.width, height=self.height * (self.top_y - 1), relief="flat",
                                bg="slategray"))
                self.top_lable[x].grid(row=0, column=x, rowspan=self.top_y - 1)
            while len(self.top_lable) <= 10:
                x += 1
                self.fill(self.top_lable, tk.Label(self.window, font="Helvetica 14 bold",
                                width=self.width, height=self.height * (self.top_y - 1), relief="flat",
                                bg="slategray"))
                self.top_lable[x].grid(row=0, column=x, rowspan=self.top_y - 1)
        elif self.x_add < 0:
            for i in range(self.x_add, 0):
                if len(self.top_lable) > 11:
                    self.top_lable[-1].destroy()
                    del self.top_lable[-1]
                else:
                    break
        
    def top_Button(self):  #不變
        '''選項：xd、yd、difficulty'''
        #xd、yd input
        self.xd_label = tk.Label(self.window, text="width :", font="elephant 14",
                                width=self.width * 3, height=self.height, relief="flat",
                                bg="slategray")
        self.yd_label = tk.Label(self.window, text="height :", font="elephant 14",
                                width=self.width * 3, height=self.height, relief="flat",
                                bg="slategray")
        self.xd_entry = tk.Entry(self.window, font="Helvetica 12 bold", width=self.width * 3)
        self.yd_entry = tk.Entry(self.window, font="Helvetica 12 bold", width=self.width * 3)
        self.xd_label.grid(row=1, column=1, columnspan=3)
        self.yd_label.grid(row=1, column=4, columnspan=3)
        self.xd_entry.grid(row=2, column=1, columnspan=3)
        self.yd_entry.grid(row=2, column=4, columnspan=3)
        #difficulty choice
        self.difficulty_label = tk.Label(self.window, text="difficulty :", font="elephant 14",
                                width=self.width * 4, height=self.height, relief="flat",
                                bg="slategray")
        self.difficulty_label.grid(row=4, column=1, columnspan=4)
        for i, (val, (word, color)) in enumerate(self.difficulty_dict.items()):
            tk.Radiobutton(self.window, text=word, font="Helvetica 10 bold",
                        width=self.width * 3, relief="raised", indicatoron=0,
                        bg=color, fg="black", value=val, variable=self.difficulty,
                        command=self.__btn_difficulty).grid(row=5, column=i * 3 + 1, columnspan=3)
    
    def __btn_difficulty(self):
        '''新的一盤( + 換難度)'''
        self.delete()
        xd = self.xd_entry.get()
        yd = self.yd_entry.get()
        if xd and yd: self.__init__(int(xd), int(yd))
        else: self.__init__(self.xd, self.yd)
    
    def frame_Label(self):
        '''邊框的背景'''
        x_original = self.x_original
        y_original = self.y_original
        if self.x_add > 0:  #right、top
            for i in range(self.x_add):
                x = x_original + i
                self.fill(self.frame_top_lable, tk.Label(self.window, font="Helvetica 14 bold",
                            width=self.width, height=self.height, relief="flat",
                            bg="lightslategray"))
                self.fill(self.frame_bottom_lable, tk.Label(self.window, font="Helvetica 14 bold",
                            width=self.width, height=self.height, relief="flat",
                            bg="lightslategray"))
                self.frame_top_lable[x].grid(row=self.top_y, column=x)
            while len(self.frame_top_lable) <= 10:
                x += 1
                self.fill(self.frame_top_lable, tk.Label(self.window, font="Helvetica 14 bold",
                        width=self.width, height=self.height, relief="flat",
                        bg="lightslategray"))
                self.fill(self.frame_bottom_lable, tk.Label(self.window, font="Helvetica 14 bold",
                        width=self.width, height=self.height, relief="flat",
                        bg="lightslategray"))
                self.frame_top_lable[x].grid(row=self.top_y, column=x)
        elif self.x_add < 0:
            for i in range(self.x_add, 0):
                if len(self.frame_top_lable) > 11:
                    self.frame_top_lable[-1].destroy()
                    del self.frame_top_lable[-1]
                    self.frame_bottom_lable[-1].destroy()
                    del self.frame_bottom_lable[-1]
                else:
                    break
        #""""""""""""""""""""""""""""""""""""""""""""""""""""""""#
        if self.y_add > 0:  #right、left
            for i in range(self.y_add):
                y = y_original + i
                self.fill(self.frame_right_lable, tk.Label(self.window, font="Helvetica 14 bold",
                            width=self.width, height=self.height, relief="flat",
                            bg="lightslategray"))
                self.fill(self.frame_left_lable, tk.Label(self.window, font="Helvetica 14 bold",
                            width=self.width, height=self.height, relief="flat",
                            bg="lightslategray"))
                self.frame_left_lable[y].grid(row=self.top_y + 1 + y, column=0)
        elif self.y_add < 0:
            for i in range(self.y_add, 0):
                self.frame_right_lable[-1].destroy()
                del self.frame_right_lable[-1]
                self.frame_left_lable[-1].destroy()
                del self.frame_left_lable[-1]
        #bottom、right定位
        for x, i in enumerate(self.frame_bottom_lable):
            i.grid(row=self.top_y + 1 + len(self.frame_left_lable), column=x)
        for y, i in enumerate(self.frame_right_lable, self.top_y + 1):
            i.grid(row=y, column=len(self.frame_top_lable) - 1)
        #return original
        self.x_original = len(self.frame_top_lable)
        self.y_original = len(self.frame_left_lable)
    
    def frame_Button(self):
        '''邊框的按鈕'''
        #self.print_button = tk.Button(self.window, text="Print", font="Helvetica 9", width=self.width * 2, height=self.height, relief="ridge", bg="lightslategray", command=self.__btn_print)
        self.exit_button = tk.Button(self.window, text="Exit", font="Helvetica 9 bold",
                        width=self.width * 2, height=self.height, relief="raised",
                        bg="darkred", fg="white", command=self.window.destroy)
        #self.print_button.grid(row=self.yd + self.top_y + 1, column=len(self.frame_top_lable) - 4, columnspan=2)
        self.exit_button.grid(row=self.yd + self.top_y + 1, column=len(self.frame_top_lable) - 2, columnspan=2)
    
    def __btn_print(self):
        '''debug'''
        for i in range(self.yd): print(self.ground[i])
        for i in range(self.yd + 1): print(", ".join([str(j[0]) for j in self.ground[i]]))

Ground.setting()
a = Ground(10, 10)
a.top_Button()
#a._Ground__btn_print()

window.mainloop()