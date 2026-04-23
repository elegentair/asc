#KNOWN ISSUE
#When running this file, the tests run, but the results are cleared by asc.
#SOLUTION
#Use the pytest-html plugin to generate an html report for the results

import asc_screen
import asc
scn = asc_screen.screen()
win = asc.window(scn, "unit-tests", bg_color="base_bg")

def test_init():
    assert win.winlist[0][0] == " "
    assert scn.slist[0][0] == " "

def test_color():
    assert scn.color_text("H", "red") == "\033[31mH\033[0m"

def test_write():
    win.write("H")
    win.draw_win()
    assert win.winlist[0][0] == "\x1b[49mH\x1b[0m"
    win.write("V", startline=2, startcol=5)
    assert win.winlist[1][4] == "\x1b[49mV\x1b[0m"

def test_scn_buff():
    win.write("O")
    win.draw_win()
    assert scn.slist_old[0][0] == "\x1b[49mO\x1b[0m"

def test_widget_creation():
    curr_id = win.curr_id_num
    win.add_inputbox(3, 3)
    assert win.ui_dict[curr_id]["type"] == "input_box"
    curr_id = win.curr_id_num
    win.add_button(3, 3)
    assert win.ui_dict[curr_id]["type"] == "button"