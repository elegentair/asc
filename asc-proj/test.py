import asc
import asc_screen
scn = asc_screen.screen()
win = asc.window(scn, "demo")
win.add_inputbox(3, 3)
text_in = win.ui_draw()
print(f"You wrote: {text_in}")
#print(win.ui_dict)