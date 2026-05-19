#fills screen with typable box, with char wrapping and auto resizing. Outputs what you wrote after (but that gets cleared by the screen)
import asc
import asc_screen
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("dataset.csv")

lst = []

xlst = df['x'].tolist()
ylst = df['y'].tolist()

xlen = len(xlst)

ylen = len(ylst)

mlen = xlen + ylen

x = 0
y = 0
for i in range(0, mlen):
    if i % 2 == 0:
        lst.append(xlst[x]) 
        x += 1
    else:
        lst.append(ylst[y]) 
        y += 1

dfc = df.drop(0)

dfc["x"] = dfc["x"].astype(float)
dfc["y"] = dfc["y"].astype(float)
#plt.figure(figsize=(6, 4))
def math():
    plt.scatter(dfc["x"], dfc["y"], color="blue", marker="o")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("ASC Test Scatterplot")
    plt.savefig("asc_scatter_plot.png")

scn = asc_screen.screen()
win = asc.window(scn, "demo")
win.add_inputbox(3, 3, 0, 0, bg_color="blue")
win.add_text_box("Hello! This is a text box! As you can see, I do absolutely nothing except be read! I even do charecter wrapping!", 1, 1, 1, 1, bg_color="red")
win.add_button("This is a button! Pressing me will generate a plot from the data in the table!", math, 5, 5, 0, 0, bg_color="green")
win.add_table(lst, 4, 4, 0, 0, bg_color="magenta")
text_in = win.ui_draw_static()
print(f"You wrote: {text_in}")
debug = False

#FOR DEBUGGING
if debug:
    st = ""
    for i in win.ui_dict["ui_grid"]:
        for c in win.ui_dict["ui_grid"][i]:
            st += str(win.ui_dict["ui_grid"][i][c])
            st += " "
        print(st)
        st = ""
    i = 1
    start_line = win.ui_dict[i]["l_tl"]
    start_col = win.ui_dict[i]["c_tl"]
    end_line = win.ui_dict[i]["l_tl"] + win.ui_dict[i]["l_size"]
    end_col = win.ui_dict[i]["c_tl"] + win.ui_dict[i]["c_size"]
    l_size = win.ui_dict[i]["l_size"]
    c_size = win.ui_dict[i]["c_size"]
    print(start_line)
    print(end_line)
    print(start_col)
    print(end_col)
    print(l_size)
    print(c_size)
#print(recalc)