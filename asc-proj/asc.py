import time
import math
#Imports the screen class. The screen class is the only part that will vary across platforms
import asc_screen

#IDEA FOR DYNAMIC RESIZING:
#The curent screen lines number would be divided by the the base window size (usually 80 cols). This num would be called the line multiplier. If the line multiplier is less than 1, the program would tell the user that their terminal is too small. The same thing would be done for columns. Then, on resize/window scaliong, every ui element would be resized by that line & col multiplier. The only concern is that if its a decimal that could cause some things to go wrong and it may not be even. Aspect ratio would need to be presevred, so if the screen is not the windows base aspect ratio, letterboxing would be used (i.e just making the screen bg around the window.)

#Makes the main screen object that apps will interact with
scn = asc_screen.screen()
class window:
    def __init__(self, title="Window", lines=24, cols=80, bg=" ", bg_color = "base_bg", borders=False):
        self.title = title
        self.borders = borders
        #This is a dictionary that will hold all data about each ui widget in the window
        self.ui_dict = {}
        #This is a number that is used to assign id nums to ui elements
        self.curr_id_num = 1
        #Here, lines and cols sizes are subtracted by 2 because borders take up two cols, two lines
        if self.borders:
            self.sizelines = lines - 2
            self.sizecols = cols - 2
        else:
            self.sizelines = lines
            self.sizecols = cols
        #Here, the dictionary that will hold line and col chars is made
        self.window_chars = {}
        #This sets the window bg color
        self.bgcolor = bg_color
        #This serves as a detector var if the window is too big
        if self.sizelines > scn.line_num:
            self.need_shrink_lines = True
        else:
            self.need_shrink_lines = False

        if self.sizecols > scn.col_num:
            self.need_shrink_cols = True
        else:
            self.need_shrink_cols = False

        #The background of the window is really space chars, and this colors them to the chosen bg color.
        self.bg_char = scn.color_background(" ", bg_color)
        
        #This makes the nested dictionaries for the lines and cols of the window.
        for i in range(1, self.sizelines + 1):
            self.window_chars[i] = {}
        for i in self.window_chars:
            for c in range(1, self.sizecols + 1):
                self.window_chars[i][c] = self.bg_char
        #This is a class text var, used in the input write method.
        self.str_text = ""
        #This is a state used to determine if the currently focused ui element needs to be unfocused bc esc has been pressed
        self.need_unfocus_current = False
        if self.borders:
            lns = self.sizelines + 2
            colns = self.sizecols + 2
            aspect_gcd = math.gcd(lns, colns)
            self.aspect_ratio_lines = (lns / aspect_gcd)
            self.aspect_ratio_cols = (colns / aspect_gcd)
        else:
            aspect_gcd = math.gcd(self.sizecols, self.sizelines)
            self.aspect_ratio_lines = (self.sizelines / aspect_gcd)
            self.aspect_ratio_cols = (self.sizecols / aspect_gcd)

            
    def draw_win(self):
        #Here, the middle line and column of the window and the screen is calculated.
        #It is used for alignment of the window with the screen
        scn_lines_mid = ((scn.line_num - 1) / 2) + 1
        scn_cols_mid = ((scn.col_num - 1) / 2) + 1
        win_lines_mid = ((self.sizelines - 1) / 2) + 1
        win_cols_mid = ((self.sizecols - 1) / 2) + 1
        #Here, the starting and ending line of the screen that the window will be drawn on is calculated.
        lines_start = int(scn_lines_mid - ((self.sizelines - 1) / 2))
        lines_end = int(scn_lines_mid + ((self.sizelines - 1) / 2))
        #The same is done for columns:
        cols_start = int(scn_cols_mid - ((self.sizecols - 1) / 2))
        cols_end = int(scn_cols_mid + ((self.sizecols - 1 ) / 2))
        #This is another counter var to keep track of what lines have been drawn on
        window_lines_index = 1
        #This is the main for loop that transposes the window onto the screen
        for i in range(lines_start, lines_end + 1):
            window_cols_index = 1
            for c in range(cols_start, cols_end + 1):
                scn.lines[i][c] = self.window_chars[window_lines_index][window_cols_index]
                window_cols_index += 1
            window_lines_index += 1
        #Drawing Window Borders:
        if self.borders:
            #First loop draws borders on top and bottom, second loop does sides and corners
            for i in range(cols_start - 1, cols_end + 2):
                scn.lines[(lines_start - 1)][i] = scn.bordercol
                scn.lines[(lines_end + 1)][i] = scn.bordercol
                
            for i in range(lines_start, lines_end + 1):
                scn.lines[i][(cols_start - 1)] = scn.bordercol
                scn.lines[i][(cols_end + 1)] = scn.bordercol
        #This updates the screen
        scn.newdraw()
    #This method allows text to be placed freely on the screen.
    #Line is the line the text will be put on, col is the column it will start on.
    #text is the actual text to be written.
    #Color is the text color, the wrapping setting controls if the text is wrapping or not.
    #The bg var is the background color of the text
    def write(self, text, line=1, col=1, endline="max", endcol="max", color="base_text", bg="base_win_bg", wrapping=True):
        #If endline and endcol are "max", the text will use all lines (besides starting) and all cols (besides starting)
        if endline == "max":
            endline = self.sizelines
        if endcol == "max":
            endcol = self.sizecols
            
        #If the bg is left default, it will inherit the background color of the window.
        if bg == "base_win_bg":
            bg = self.bgcolor
        #This is a counter var to keep track of columns
        c = col
        #This loop iterates through the text and writes each letter to the column before it.
        for i in text:
            charec = scn.color_bf(i, color, bg)
            self.window_chars[line][c] = charec
            if wrapping == False:
                if c >= endcol:
                    #FOR LATER: implement text scrolling if it doesnt wrap
                    self.need_unfocus_current = True
                else:
                    c += 1
            #This auto pushes the text to the next line if it overtakes the first line & wrapping is on
            elif wrapping == True:
                if line >= self.sizelines and c >= endcol:
                    self.need_unfocus_current = True
                elif c >= self.sizecols or c >= endcol:
                    line += 1
                    c = col
                else:
                    c += 1
    #This method does the same as the write method, but writes with user input
    #It captures user input until a app dev set keybinding activates
    def input_write(self, startline=1, startcol=1, endline="max", endcol="max", color="base_text", bg="base_win_bg", wrapping=True):
        #If endline and endcol are "max", the text will use all lines (besides starting) and all cols (besides starting)
        if endline == "max":
            endline = self.sizelines
        if endcol == "max":
            endcol = self.sizecols
        char_amount = ((endline - startline) + 1) * ((endcol - startcol) + 1)
        bufftxt = ""
        #Assign the dict entry for this widget
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "input_write"
        self.ui_dict[self.curr_id_num]["hor_size"] = ((endcol - startcol) + 1)
        self.ui_dict[self.curr_id_num]["vert_size"] = ((endline - startline) + 1)
        self.curr_id_num += 1
        for i in range(0, char_amount):
            bufftxt += " "
            self.write(bufftxt, startline, startcol, endline, endcol, color, bg, wrapping)
        self.draw_win()

        self.need_unfocus_current = False
        
        while self.need_unfocus_current == False:
            res = scn.get_input()
            if res == "^BACKSPACE":
                self.str_text = self.str_text[:-1]
                self.str_text += " "
                self.write(self.str_text, startline, startcol, endline, endcol, color, bg, wrapping)
                self.str_text = self.str_text[:-1]
                self.draw_win()
            elif res == "^ESCAPE":
                self.need_unfocus_current = True
            else:
                self.str_text = self.str_text[:-1]
                self.str_text += res
                self.str_text += "_"
                self.write(self.str_text, startline, startcol, endline, endcol, color, bg, wrapping)
                self.draw_win()
# to maintain a similar aspect ratio, add 7 columns for every two rows added, starting at 80x22    
win = window("test", lines=22, cols=80, bg_color="blue", borders=True)
#print(scn.line_num)
#win.write("This is mr sandman!!!! I love my country because it is the best!", line=3, col=40, endcol=50)
win.draw_win()
win.input_write(wrapping=True)
#time.sleep(5)
#print(f"Lines: {win.aspect_ratio_lines} Cols: {win.aspect_ratio_cols}")
