#fills screen with typable box, with char wrapping and auto resizing. Outputs what you wrote after (but that gets cleared by the screen)
import asc
import asc_screen
scn = asc_screen.screen()
win = asc.window(scn, "demo", bg_color="blue")
win.add_inputbox(3, 4, color="magenta")
win.add_inputbox(1, 2)
text_in = win.ui_draw()
print(f"You wrote: {text_in}")

wid = int(win.arc_cols/win.grid_mult)
wrem = win.arc_cols%win.grid_mult
lin = int(win.arc_lines/win.grid_mult)
lrem = win.arc_lines%win.grid_mult



#FOR DEBUGGING
print(win.ui_dict["ui_grid"])
#print(expe)