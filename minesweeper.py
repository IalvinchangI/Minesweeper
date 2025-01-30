import tkinter as tk
import random, time


window = tk.Tk()
window.title("minesweeper")

###############
xd = 10  #地圖寬度
yd = 10  #地圖高度
top_y = 7
x_size = 2  #一格寬度
y_size = 1  #一格高度
difficulty = tk.IntVar()
difficulty.set(7)  #難度(越小越難)
###############


def dig_check(list_xy, x, y, data, xd, yd, top_y):
    def check(continue_TF = True):
        if continue_TF:
            for list_pos, pos in get_position(list_xy, x, y):
                dig_check(list_xy, pos[0], pos[1], data, xd, yd, top_y)
        else:
            for list_pos, pos in get_position(list_xy, x, y, 2):
                if list_pos == 0:
                    dig_check(list_xy, pos[0], pos[1], data, xd, yd, top_y)
        if data[0] == data[1]:
            data.append(gameover(list_xy, xd, yd, top_y))
    if list_xy[y][x][0] == 0:
        dig(list_xy, x, y)
        data[1] -= 1
        check()
    elif list_xy[y][x][0] == 9:
        dig(list_xy, x, y)
        data[1] -= 1
        data.append(gameover(list_xy, xd, yd, top_y, word="Loss"))
    elif list_xy[y][x][0] > 0:
        dig(list_xy, x, y)
        data[1] -= 1
        check(continue_TF = False)

def dig(list_xy, x, y):
    blank = list_xy[y][x]
    translate = {0:("", "gray"), 1:("１", "darkorange"), 2:("２", "green"), 3:("３", "blue"), 4:("４", "indigo"),
             5:("５", "midnightblue"), 6:("６", "black"), 7:("７", "black"), 8:("８", "black"), 9:("Ｘ", "red")}
    try:
        blank[1]["text"] = translate[blank[0]][0]
        blank[1]["fg"] = translate[blank[0]][1]
        blank[2].destroy()
        del blank[3]
        blank[1]["relief"] = "sunken"
        if blank[1]["bg"] == "dimgray":
            blank[1]["bg"] = "lightgray"
        else:
            blank[1]["bg"] = "whitesmoke"
        blank[0] = -1
    except KeyError: pass

def get_position(list_xy, x, y, step = 1):
    pos_dict = {
        1:(list_xy[y + 1][x - 1][0], (x - 1, y + 1)), 2:(list_xy[y + 1][x][0], (x, y + 1)), 3:(list_xy[y + 1][x + 1][0], (x + 1, y + 1)),
        4:(list_xy[y][x - 1][0], (x - 1, y)), 10:(list_xy[y][x][0], (x, y)), 6:(list_xy[y][x + 1][0], (x + 1, y)),
        7:(list_xy[y - 1][x - 1][0], (x - 1, y - 1)), 8:(list_xy[y - 1][x][0], (x, y - 1)), 9:(list_xy[y - 1][x + 1][0], (x + 1, y - 1))
    }  #(數字鍵)
    return tuple([i[1] for i in pos_dict.items() if not i[0] % step])

def gameover(list_xy, xd, yd, top_y, word = "Congratulation"):
    def btn_gameover():
        nonlocal gameover_button
        gameover_button.destroy()
        del gameover_button
        for y in range(yd):
            for x in range(xd):
                if len(list_xy[y][x]) == 4:
                    dig(list_xy, x, y)
    gameover_button = tk.Button(window, text=word, font="Helvetica 17 bold",
                      width=x_size * xd, height=y_size * (yd - 1), relief="flat",
                      fg="slategray", command=btn_gameover)
    gameover_button.grid(row=top_y + 1, column=1, rowspan=yd, columnspan=xd)
    return gameover_button

def create(xd, yd, difficulty, top_y = 3, x_size = 2, y_size = 1):
    def btn_dig(list_xy, x, y, data, xd, yd, top_y):
        return lambda: dig_check(list_xy, x, y, data, xd, yd, top_y)
    ground = list([[0, None, None, None][:] for i in range(xd + 1)[:]] for i in range(yd + 1))
    data = [0, xd * yd]
    for y in range(yd):
        for x in range(xd):
            blank = ground[y][x]
            if random.randint(0, difficulty.get()) == 0:
                blank[0] = 9  #mine
                data[0] += 1
                for list_pos, pos in get_position(ground, x, y):
                    if list_pos != 9:
                        ground[pos[1]][pos[0]][0] += 1
            blank[1] = tk.Label(window, font="Helvetica 14 bold",
                                width=x_size, height=y_size, relief="flat")
            blank[3] = btn_dig(ground, x, y, data, xd, yd, top_y)
            blank[2] = tk.Button(window, font="Helvetica 10",
                                 width=x_size, height=y_size, relief="flat",
                                 command=blank[3])
            if (x + y) % 2:
                blank[1]["bg"] = blank[2]["bg"] = "dimgray"
            else:
                blank[1]["bg"] = blank[2]["bg"] = "gray"
            blank[1].grid(row=y + top_y + 1, column=x + 1)
            blank[2].grid(row=y + top_y + 1, column=x + 1)
    for y in range(yd): ground[y][xd][0] = -1
    for x in range(xd + 1): ground[yd][x][0] = -1
    return ground, data

def top(xd, yd, data, top_y = 3, x_size = 2, y_size = 1):
    def btn_difficulty():
        global ground, data
        for y in range(yd):
            for x in range(xd):
                ground[y][x][1].destroy()
                if len(ground[y][x]) == 4:
                    ground[y][x][2].destroy()
                del ground[y][x][:]
            del ground[y][xd]
        for x in range(xd):
            del ground[yd][x][:]
        del ground[yd][:]
        del ground[:]
        if len(data) == 3:
            data[2].destroy()
        del data[:]
        ground, data = create(xd, yd, difficulty, top_y, x_size, y_size)
    top_lable = []
    fill = lambda list_, lable: list_.append(lable)
    for x in range(xd + 2):
        fill(top_lable, tk.Label(window, font="Helvetica 14 bold",
                        width=x_size, height=y_size * (top_y - 1), relief="flat",
                        bg="slategray"))
        top_lable[x].grid(row=0, column=x, rowspan=top_y - 1)
    """
    xd_entry = tk.Entry(window, font="Helvetica 12 bold", width=x_size * 3)
    yd_entry = tk.Entry(window, font="Helvetica 12 bold", width=x_size * 3)
    xd_entry.grid(row=1, column=1, columnspan=3)
    yd_entry.grid(row=1, column=4, columnspan=3)
    """
    difficulty_dict = {12:("Easy", "limegreen"), 7:("Normal", "darkorange"), 4:("Hard", "crimson")}
    for i, (val, (word, color)) in enumerate(difficulty_dict.items()):
        tk.Radiobutton(window, text=word, font="Helvetica 10 bold",
                    width=x_size * 3, relief="raised", indicatoron=0,
                    bg=color, fg="black", value=val, variable=difficulty,
                    command=btn_difficulty).grid(row=5, column=i * 3 + 1, columnspan=3)

def frame(xd, yd, top_y = 3, x_size = 2, y_size = 1):
    def btn_print():
        for i in range(yd): print(ground[i])
        for i in range(yd + 1): print(", ".join([str(j[0]) for j in ground[i]]))
    fill = lambda list_, lable: list_.append(lable)
    frame_top_lable, frame_right_lable, frame_bottom_lable, frame_left_lable = [], [], [], []
    for x in range(xd + 2):
        fill(frame_top_lable, tk.Label(window, font="Helvetica 14 bold",
                      width=x_size, height=y_size, relief="flat",
                      bg="lightslategray"))
        fill(frame_bottom_lable, tk.Label(window, font="Helvetica 14 bold",
                      width=x_size, height=y_size + 1, relief="flat",
                      bg="lightslategray"))
        frame_top_lable[x].grid(row=top_y, column=x)
        frame_bottom_lable[x].grid(row=top_y + 1 + yd, column=x)
    for y in range(yd):
        fill(frame_right_lable, tk.Label(window, font="Helvetica 14 bold",
                      width=x_size, height=y_size, relief="flat",
                      bg="lightslategray"))
        fill(frame_left_lable, tk.Label(window, font="Helvetica 14 bold",
                      width=x_size, height=y_size, relief="flat",
                      bg="lightslategray"))
        frame_right_lable[y].grid(row=top_y + 1 + y, column=1 + xd)
        frame_left_lable[y].grid(row=top_y + 1 + y, column=0)
    print_button = tk.Button(window, text="Print", font="Helvetica 10",
                    width=x_size * 2, height=y_size, relief="ridge",
                    bg="lightslategray", command=btn_print)
    exit_button = tk.Button(window, text="Exit", font="Helvetica 10 bold",
                    width=x_size * 2, height=y_size, relief="raised",
                    bg="darkred", fg="white", command=window.destroy)
    print_button.grid(row=yd + top_y + 1, column=xd - 3, columnspan=2)
    exit_button.grid(row=yd + top_y + 1, column=xd - 1, columnspan=2)


ground, data = create(xd, yd, difficulty, top_y, x_size, y_size)
top(xd, yd, data, top_y, x_size, y_size)
frame(xd, yd, top_y, x_size, y_size)





window.mainloop()