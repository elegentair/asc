#fills screen with typable box, with char wrapping and auto resizing. Outputs what you wrote after (but that gets cleared by the screen)
import asc
import asc_screen
scn = asc_screen.screen()
win = asc.window(scn, "demo")
win.add_inputbox(3, 3, 2, 2, bg_color="blue")
#win.add_inputbox(1, 2)
text_in = win.ui_draw()
print(f"You wrote: {text_in}")

#FOR DEBUGGING
#st = ""
#for i in win.ui_dict["ui_grid_sizes"]:
#    for c in win.ui_dict["ui_grid_sizes"][i]:
#        st += str(win.ui_dict["ui_grid_sizes"][i][c])
#        st += " "
#    print(st)
#    st = ""
#i = 1
#start_line = win.ui_dict[i]["l_tl"]
#start_col = win.ui_dict[i]["c_tl"]
#end_line = win.ui_dict[i]["l_tl"] + win.ui_dict[i]["l_size"]
#end_col = win.ui_dict[i]["c_tl"] + win.ui_dict[i]["c_size"]
#l_size = win.ui_dict[i]["l_size"]
#c_size = win.ui_dict[i]["c_size"]
#print(start_line)
#print(end_line)
#print(start_col)
#print(end_col)
#print(l_size)
#print(c_size)