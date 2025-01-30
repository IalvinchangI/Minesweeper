import tkinter as tk
import random


window = tk.Tk()
window.title("minesweeper")

###############
xd = 20  #地圖寬度
yd = 20  #地圖高度
x_size = 2  #一格寬度
y_size = 1  #一格高度
difficulty = 7  #難度(越小越難)
###############

def btn_dig(list_xy, x, y):
    return lambda: dig_check(list_xy, x, y)

def dig_check(list_xy, x, y):
    if list_xy[y][x][0] == 0:
        dig(list_xy, x, y)
    elif list_xy[y][x][0] == 9:
        dig(list_xy, x, y, continue_TF = False)
        global gameover
        gameover = True
    elif list_xy[y][x][0] > 0:
        dig(list_xy, x, y, continue_TF = False)

def dig(list_xy, x, y, continue_TF = True):
    blank = list_xy[y][x]
    try:
        blank[3].destroy()
        blank[2]["text"] = translate[blank[0]][0]
        blank[2]["fg"] = translate[blank[0]][1]
        blank[2]["relief"] = "sunken"
        if blank[2]["bg"] == "dimgray":
            blank[2]["bg"] = "lightgray"
        else:
            blank[2]["bg"] = "whitesmoke"
        blank[0] = -1
    except KeyError: pass
    else:
        if continue_TF:
            for list_pos, pos in get_position(list_xy, x, y):
                dig_check(list_xy, pos[0], pos[1])
        else:
            for list_pos, pos in get_position(list_xy, x, y, 2):
                if list_pos == 0:
                    dig_check(list_xy, pos[0], pos[1])

def create(xd, yd, difficulty, x_size = 2, y_size = 1):
    ground = tuple(tuple([0, None, None, None][:] for i in range(xd + 1))[:] for i in range(yd + 1))
    for y in range(yd):
        for x in range(xd):
            blank = ground[y][x]
            if random.randint(0, difficulty) == 0:
                blank[0] = 9  #mine
                for list_pos, pos in get_position(ground, x, y):
                    if list_pos != 9:
                        ground[pos[1]][pos[0]][0] += 1
            
            blank[1] = btn_dig(ground, x, y)
            blank[2] = tk.Label(window, font="Helvetica 14 bold",
                                width=x_size, height=y_size, relief="flat"
                                )
            blank[3] = tk.Button(window, font="Helvetica 10",
                                 width=x_size, height=y_size, relief="flat",
                                 command=blank[1]
                                )
            if (x + y) % 2:
                blank[2]["bg"] = blank[3]["bg"] = "dimgray"
            else:
                blank[2]["bg"] = blank[3]["bg"] = "gray"
            blank[2].grid(row=y, column=x)
            blank[3].grid(row=y, column=x)
    for y in range(yd): ground[y][xd][0] = -1
    for x in range(xd + 1): ground[yd][x][0] = -1

def get_position(list_xy, x, y, step = 1):
    pos_dict = {
        1:(list_xy[y + 1][x - 1][0], (x - 1, y + 1)), 2:(list_xy[y + 1][x][0], (x, y + 1)), 3:(list_xy[y + 1][x + 1][0], (x + 1, y + 1)),
        4:(list_xy[y][x - 1][0], (x - 1, y)), 10:(list_xy[y][x][0], (x, y)), 6:(list_xy[y][x + 1][0], (x + 1, y)),
        7:(list_xy[y - 1][x - 1][0], (x - 1, y - 1)), 8:(list_xy[y - 1][x][0], (x, y - 1)), 9:(list_xy[y - 1][x + 1][0], (x + 1, y - 1))
    }  #(數字鍵)
    return tuple([i[1] for i in pos_dict.items() if not i[0] % step])


translate = {0:("", "gray"), 1:("１", "darkorange"), 2:("２", "green"), 3:("３", "blue"), 4:("４", "indigo"),
             5:("５", "midnightblue"), 6:("６", "black"), 7:("７", "black"), 8:("８", "black"), 9:("Ｘ", "red")}
gameover = False


create(xd, yd, difficulty, x_size, y_size)

window.mainloop()