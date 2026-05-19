#fills screen with typable box, with char wrapping and auto resizing. Outputs what you wrote after (but that gets cleared by the screen)
import asc
import asc_screen
import matplotlib
import pandas as pd

pro = {}
def math():
    lst[1] = "z"

lst = ["x", "y", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

df = pd.DataFrame({"x": lst[0::2], "y": lst[1::2]})

scn = asc_screen.screen()
win = asc.window(scn, "demo")
win.add_inputbox(3, 3, 0, 0, bg_color="blue")
win.add_text_box("Hello! This is a text box! As you can see, I do absolutely nothing except be read! I even do charecter wrapping!", 1, 1, 1, 1, bg_color="red")
win.add_button("This is a button! Pressing me will update the var Y to Z in the table!", math, 5, 5, 0, 0, bg_color="green")
win.add_table(lst, 4, 4, 0, 0, bg_color="magenta")
text_in = win.ui_draw_static()
print(f"You wrote: {text_in}")
print(df)
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