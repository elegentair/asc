# This python file contains the screen class for the "asc" TUI lib. This screen class is for writing to standard terminals

# Used to get term len and width
import shutil
# Used for Windows support to enable escape chars for colors.
#import os
# Used to cleanup terminal (turn on cursor) at exit
import atexit
import signal
# Used for input and other functions:
import sys
# Used for input:
import termios

import time

import copy
# Get original terminal settings:
og_term = termios.tcgetattr(sys.stdin.fileno())

#This function will run on quit of program
def term_cleanup():
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, og_term)
    sys.stdout.write("\033[?25h\033[0m\033[0J")
    #sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()

#These commands set the function above to run at exit
atexit.register(term_cleanup)

def exit_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

# Class for terminal canvas
class screen:
    def __init__(self, initchar=" "):
        # Get the terminal size and assign it to column and line number vars
        term_size = shutil.get_terminal_size()
        self.og_line_num = term_size.lines
        self.og_cols_num = term_size.columns
        self.bordercol = "\033[107m" + " "+ "\033[0m"
        self.line_num = term_size.lines
        self.col_num = term_size.columns

        # Enter cbreak + disable input mode:
        ter = sys.stdin.fileno()
        term_to_modify = termios.tcgetattr(ter)
        term_to_modify[3] &= ~termios.ECHO
        term_to_modify[3] &= ~termios.ICANON
        term_to_modify[3] &= ~termios.ISIG
        term_to_modify[0] &= ~termios.IXON
        term_to_modify[6][termios.VMIN] = 0
        term_to_modify[6][termios.VTIME] = 0
        termios.tcsetattr(ter, termios.TCSADRAIN, term_to_modify)
        
        self.slist_old = []
        self.slist = []
        for i in range(0, self.line_num):
            self.slist.append([])
        for i in range(0, self.line_num):
            for c in range(0, self.col_num):
                self.slist[i].append(initchar)

    def clear(self):
        #print("\033[H\033[2J")
        print("\033[H")

    def newdraw(self):
        #moves cursor to home position and hides it
        sys.stdout.write("\033[H\033[?25l")

        for i in range(0, self.line_num):
            if self.slist_old[i] != self.slist[i]:
                for r in range(0, self.col_num):
                    if self.slist_old[i][r] != self.slist[i][r]:
                        #Moves cursor to place where text is different
                        sys.stdout.write(f"\x1b[{i + 1};{r + 1}H")
                        sys.stdout.write(self.slist[i][r])
        sys.stdout.write("\x1b[H")
        sys.stdout.flush()
        #stores the old frame
        self.slist_old = copy.deepcopy(self.slist)

    def fulldraw(self):
        charl = []
        charl.append("\033[H\033[?25l")
        #char_str = "\033[H\033[?25l"
        for i in range(0, self.line_num):
            for r in range(0, self.col_num):
                charl.append(self.slist[i][r])
            if (i + 1) < self.line_num:
                charl.append("\n")
        outp = "".join(charl)
        #sys.stdout.write(char_str)
        sys.stdout.write(outp)
        sys.stdout.flush()
        self.slist_old = copy.deepcopy(self.slist)

    # Takes the line and col num to be edited, and the charecter to replace it with, with color.
    # Color is taken manually in asc instead of with escape codes.
    # This is so color works on all systems, regardless of old (and janky) escape code usage
    # When using colors in asc, please use this instead of escape chars.
    def edit(self, line, col, charec, color="base_text", bgcolor="base_bg"):
        # Color Support. 1st esc. code is color code, last is the color reset code, so that the color code doesnt effect text after the colored text
        if bgcolor == "red":
            bgc = "\033[41m"
        elif bgcolor == "green":
            bgc = "\033[42m"
        elif bgcolor == "yellow":
            bgc = "\033[43m"
        elif bgcolor == "blue":
            bgc = "\033[44m"
        elif bgcolor == "magenta":
            bgc = "\033[45m"
        elif bgcolor == "cyan":
            bgc = "\033[46m"
        elif bgcolor == "base_bg":
            bgc = "\033[49m"
        
        if color == "red":
            color_char = "\033[31m" + bgc + str(charec) + "\033[0m"
        elif color == "green":
            color_char = "\033[32m" + bgc + str(charec) + "\033[0m"
        elif color == "yellow":
            color_char = "\033[33m" + bgc + str(charec) + "\033[0m"
        elif color == "blue":
            color_char = "\033[34m" + bgc + str(charec) + "\033[0m"
        elif color == "magenta":
            color_char = "\033[35m" + bgc + str(charec) + "\033[0m"
        elif color == "cyan":
            color_char = "\033[36m" + bgc + str(charec) + "\033[0m"
        elif color == "base_text":
            color_char = bgc + str(charec) + "\033[0m"
        #This serves as a good example of how to manually edit the screen as well
        self.lines[line][col] = color_char

    def check_resize(self, li, co):
        term_size = shutil.get_terminal_size()
        if li == term_size.lines and co == term_size.columns:
            return False
        else:
            return True

    def update_res(self):
        # Get the terminal size and assign it to column and line number vars
        term_size = shutil.get_terminal_size()
        self.col_num = term_size.columns
        self.line_num = term_size.lines

#This method colors any text needed. It is called by asc.
#It is in this file bc escape chars may not exist on other platforms
    def color_text(self, charec, color):
        color_char = ""
        if color == "red":
            color_char = "\033[31m" + str(charec) + "\033[0m"
        elif color == "green":
            color_char = "\033[32m" + str(charec) + "\033[0m"
        elif color == "yellow":
            color_char = "\033[33m" + str(charec) + "\033[0m"
        elif color == "blue":
            color_char = "\033[34m" + str(charec) + "\033[0m"
        elif color == "magenta":
            color_char = "\033[35m" + str(charec) + "\033[0m"
        elif color == "cyan":
            color_char = "\033[36m" + str(charec) + "\033[0m"
        elif color == "base_text":
            color_char = charec
        return color_char
    def color_background(self, charec, color):
        if color == "red":
            color_char = "\033[41m" + str(charec) + "\033[0m"
        elif color == "green":
            color_char = "\033[42m" + str(charec) + "\033[0m"
        elif color == "yellow":
            color_char = "\033[43m" + str(charec) + "\033[0m"
        elif color == "blue":
            color_char = "\033[44m" + str(charec) + "\033[0m"
        elif color == "magenta":
            color_char = "\033[45m" + str(charec) + "\033[0m"
        elif color == "cyan":
            color_char = "\033[46m" + str(charec) + "\033[0m"
        elif color == "base_bg":
            color_char = charec
        return color_char
    def color_bf(self, charec, color="base_text", bgcolor="base_bg"):
        if bgcolor == "red":
            bgc = "\033[41m"
        elif bgcolor == "green":
            bgc = "\033[42m"
        elif bgcolor == "yellow":
            bgc = "\033[43m"
        elif bgcolor == "blue":
            bgc = "\033[44m"
        elif bgcolor == "magenta":
            bgc = "\033[45m"
        elif bgcolor == "cyan":
            bgc = "\033[46m"
        elif bgcolor == "base_bg":
            bgc = "\033[49m"
        
        if color == "red":
            color_char = "\033[31m" + bgc + str(charec) + "\033[0m"
        elif color == "green":
            color_char = "\033[32m" + bgc + str(charec) + "\033[0m"
        elif color == "yellow":
            color_char = "\033[33m" + bgc + str(charec) + "\033[0m"
        elif color == "blue":
            color_char = "\033[34m" + bgc + str(charec) + "\033[0m"
        elif color == "magenta":
            color_char = "\033[35m" + bgc + str(charec) + "\033[0m"
        elif color == "cyan":
            color_char = "\033[36m" + bgc + str(charec) + "\033[0m"
        elif color == "base_text":
            color_char = bgc + str(charec) + "\033[0m"
        return color_char
    
    def get_input(self):
        inp = sys.stdin.read(1)
        #if inp == "\x1b":
        #time.sleep(0.02)
        if not inp:
            return ""
        
        if inp == "\x1b":
            time.sleep(0.02)
            while True:
                rem = sys.stdin.read(1)
                if rem:
                    inp += rem
                else:
                    break
        if inp == "\x1b":
            return "^ESCAPE"
        elif inp == "\x7f":
            char = "^BACKSPACE"
        #elif inp == "\x1b":
            #char = "^ESCAPE"
        elif inp == "\x1b[A":
            char = "^UP_ARROW"
        elif inp == "\x1b[B":
            char = "^DOWN_ARROW"
        elif inp == "\x1b[C":
            char = "^RIGHT_ARROW"
        elif inp == "\x1b[D":
            char = "^LEFT_ARROW"
        elif inp == "\n":
            char = "^ENTER"
        else:
            char = inp
        return char