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
    #These two things are depricated, HAVE to be false
    assert win.borders == False
    assert win.dyn_size == False

    assert win.screen == scn
    assert win.ui_needs_init == True
    assert win.drawing_id == 0

def test_color():
    assert scn.color_text("H", "red") == "\033[31mH\033[0m"
    assert scn.color_background(" ", "red") == "\033[41m" + " " + "\033[0m"
    assert scn.color_bf(" ", "red", "blue") == "\033[31m" + "\033[44m" + " " + "\033[0m"

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
    win.add_inputbox(3, 3, 1, 1)
    assert win.ui_dict[curr_id]["type"] == "input_box"
    assert win.ui_dict[curr_id]["grid_x"] == 3
    assert win.ui_dict[curr_id]["grid_y"] == 3
    assert win.ui_dict[curr_id]["l_ext"] == 2
    assert win.ui_dict[curr_id]["c_ext"] == 2
    curr_id = win.curr_id_num
    win.add_text_box("hello", 5, 5, 0, 0)
    assert win.ui_dict[curr_id]["type"] == "text_box"
    assert win.ui_dict[curr_id]["text"] == "hello"

