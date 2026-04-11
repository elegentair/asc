import asc
import asc_screen
scn = asc_screen.screen()
win = asc.window(scn, "demo", bg_color="magenta")
text_in = win.input_write()
text_int = win.input_write()
print(f"You wrote: {text_in}, {text_int}")
print(win.ui_dict)