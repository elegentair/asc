#fills screen with typable box, with char wrapping and auto resizing. Outputs what you wrote after
import asc
import asc_screen
scn = asc_screen.screen()
win = asc.window(scn, "demo")
win.add_inputbox(3, 3, color="magenta")
text_in, expe = win.ui_draw()
print(f"You wrote: {text_in}")
#FOR DEBUGGING
#print(win.ui_dict)
print(expe)