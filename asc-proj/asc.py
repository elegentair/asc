class window:
    def __init__(self, screen_obj, title="Window", bg=" ", bg_color = "base_bg", grid_mult = 1, borders=False, uidict={}, strtxt = ""):
        import math
        self.firstdraw = True
        self.screen = screen_obj
        lines = self.screen.line_num
        cols = self.screen.col_num
        self.title = title
        self.resize = 0
        self.endmsg = ""
        #BORDERS ARE DEPRICATED FOR NOW
        self.borders = False
        self.bgchoice = bg
        self.arc_lines = lines
        self.arc_cols = cols
        #This is a dictionary that will hold all data about each ui widget in the window
        self.ui_dict = uidict
        #if "leftmost_avail_col" not in self.ui_dict:
        #    #This is the left-most empty column availible
        #    self.ui_dict["leftmost_avil_col"] = 0
        #    #This is the same for the right
        #    self.ui_dict["rightmost_avail_col"] = self.arc_cols
        #if "highest_avail_line" not in self.ui_dict:
        #    #This is the highest empty line availible
        #    self.ui_dict["highest_avail_line"] = self.arc_lines
        #    #This is the same from the bottom
        #    self.ui_dict["avail_bot_lines"] = self.arc_lines`
        #Makes a grid of widget positions
        #This does not check if it is already been done because it NEEDS to be recalculated on resize
        if "ui_grid" not in self.ui_dict:
            self.ui_dict["ui_grid"] = {}

        self.grid_mult = grid_mult

        for i in range(1, ((grid_mult * 5) + 1)):
            self.ui_dict["ui_grid"][i] = {}
            for c in range(1, ((grid_mult * 5) + 1)):
                self.ui_dict["ui_grid"][i][c] = 0

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
        if self.sizelines > self.screen.line_num:
            self.need_shrink_lines = True
        else:
            self.need_shrink_lines = False

        if self.sizecols > self.screen.col_num:
            self.need_shrink_cols = True
        else:
            self.need_shrink_cols = False

        #The background of the window is really space chars, and this colors them to the chosen bg color.
        self.bg_char = self.screen.color_background(self.bgchoice, bg_color)
        
        #This makes the nested dictionaries for the lines and cols of the window.
        for i in range(1, self.arc_lines + 1):
            self.window_chars[i] = {}
        for i in self.window_chars:
            for c in range(1, self.arc_cols + 1):
                self.window_chars[i][c] = self.bg_char
        #This is a class text var, used in the input write method.
        self.str_text = strtxt
        #This is a state used to determine if the currently focused ui element needs to be unfocused bc esc has been pressed
        self.need_unfocus_current = False
    
    def resize_win(self):
        # This re-initializes the ui every time the user resizes the app. This is needed so that the app doesnt break when resized
        self.screen.clear()
        self.resize += 1
        self.screen.__init__()
        self.__init__(self.screen, self.title, self.bgchoice, self.bgcolor, self.grid_mult, self.borders, self.ui_dict, self.str_text)

    def draw_win(self):
        self.screen.update_res()
        if self.screen.check_resize(self.arc_lines, self.arc_cols):
            self.resize_win()
        #This is another counter var to keep track of what lines have been drawn on
        window_lines_index = 1
        if self.borders:
            lines_start = 2
            cols_start = 2
            lines_end = self.arc_lines - 1
            cols_end = self.arc_cols - 1
        else:
            lines_start = 1
            cols_start = 1
            lines_end = self.sizelines
            cols_end = self.sizecols
        #This is the main for loop that transposes the window onto the screen
        for i in range(lines_start, lines_end + 1):
            window_cols_index = 1
            for c in range(cols_start, cols_end):
                #print(f"I: {i} C: {c}")
                #print(f"lstart: {lines_start} lend: {lines_end}, cstart {cols_start}, cend {cols_end} i: {i}, c: {c}")
                self.screen.lines[i][c] = self.window_chars[window_lines_index][window_cols_index]
                window_cols_index += 1
            window_lines_index += 1
        #Drawing Window Borders:
        if self.borders:
            #First loop draws borders on top and bottom, second loop does sides and corners
            for i in range(cols_start - 1, cols_end + 1):
                self.screen.lines[(lines_start)][i] = self.screen.bordercol
                self.screen.lines[(lines_end + 1)][i] = self.screen.bordercol
                
            for i in range(lines_start - 1, lines_end + 1):
                self.screen.lines[i][(cols_start)] = self.screen.bordercol
                self.screen.lines[i][(cols_end + 1)] = self.screen.bordercol
        #This updates the screen
        self.screen.newdraw()
        if self.firstdraw:
            self.firstdraw = False
    #This method allows text to be placed freely on the screen. It is NOT meant to be used independenty (NOT a ui widget). It is used by other methods.
    #Line is the line the text will be put on, col is the column it will start on.
    #text is the actual text to be written.
    #Color is the text color, the wrapping setting controls if the text is wrapping or not.
    #The bg var is the background color of the text
    def write(self, text, startline=1, startcol=1, endline="max", endcol="max", color="base_text", bg_color="base_win_bg", wrapping=True):
        #If endline and endcol are "max", the text will use all lines (besides starting) and all cols (besides starting)
        if endline == "max":
            endline = self.sizelines
        if endcol == "max":
            endcol = self.sizecols
            
        #If the bg is left default, it will inherit the background color of the window.
        if bg_color == "base_win_bg":
            bg_color = self.bgcolor
        #This is a counter var to keep track of columns
        c = startcol
        #This loop iterates through the text and writes each letter to the column before it.
        for i in text:
            charec = self.screen.color_bf(i, color, bg_color)
            self.window_chars[startline][c] = charec
            if wrapping == False:
                if c >= endcol:
                    #FOR LATER: implement text scrolling if it doesnt wrap
                    self.need_unfocus_current = True
                else:
                    c += 1
            #This auto pushes the text to the next line if it overtakes the first line & wrapping is on
            elif wrapping == True:
                if startline >= self.sizelines and c >= endcol:
                    self.need_unfocus_current = True
                elif c >= self.sizecols or c >= endcol:
                    startline += 1
                    c = startcol
                else:
                    c += 1
    def widget_place(self, align_vert, align_hor, colsize, linsize):
        if align_vert == "center" and align_hor == "center":
            #get middle column of widget:
            #Size must be odd to be in perfect middle
            middle_col = int(align_hor - ((align_hor - 1) / 2))
            
            

    #This method does the same as the write method, but writes with user input
    #It captures user input until a app dev set keybinding activates
    def add_inputbox(self, align_hor="center", align_vert="center"):
        colsize = (hor_perc / 100) * self.arc_cols
        line_size = (vert_perc / 100) * self.arc_lines
        total_hor_pad = self.arc_cols - colsize
        total_vert_pad = self.arc_lines - line_size
        if align_hor == "center":
            hor_pad = total_hor_pad / 2
            vert_pad = total_vert_pad / 2
            #startcol = self.ui_dict["
            startcol = self.ui_dict[""]
        elif align_hor == "left":
            startcol = 1
        #If endline and endcol are "max", the text will use all lines (besides starting) and all cols (besides starting)
        if endline == "max":
            endline = self.sizelines
        if endcol == "max":
            endcol = self.sizecols
    def input_write(self, startline=1, startcol=1, endline="max", endcol="max", align_hor="center", align_vert="center", color="base_text", bg_color="base_win_bg", wrapping=True):
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
        if "txt" in self.ui_dict[self.curr_id_num]:
            self.str_text = self.ui_dict[self.curr_id_num]
        for i in range(0, char_amount):
            bufftxt += " "
            self.write(bufftxt, startline, startcol, endline, endcol, color, bg_color, wrapping)
        self.draw_win()

        self.need_unfocus_current = False
        
        while self.need_unfocus_current == False:
            res = self.screen.get_input()
            if res == "^BACKSPACE":
                self.str_text = self.str_text[:-1]
                self.str_text += " "
                self.write(self.str_text, startline, startcol, endline, endcol, color, bg_color, wrapping)
                self.str_text = self.str_text[:-1]
                self.draw_win()
            elif res == "^ESCAPE":
                self.need_unfocus_current = True
            else:
                self.str_text = self.str_text[:-1]
                self.str_text += res
                self.str_text += "_"
                self.write(self.str_text, startline, startcol, endline, endcol, color, bg_color, wrapping)
                self.draw_win()
            self.ui_dict[self.curr_id_num]["txt"] = self.str_text
        ent_str = self.str_text[:-1]
        self.str_text = ""
        self.curr_id_num += 1
        return ent_str
    def add_uispace(self, vert_perc, hor_perc):
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "ui_space"
        self.ui_dict[self.curr_id_num]["vert_size"] = vert_perc
        self.ui_dict[self.curr_id_num]["hor_size"] = hor_perc
        self.curr_id_num += 1
