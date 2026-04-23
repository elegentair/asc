import time
class window:
    def __init__(self, screen_obj, title="Window", bg=" ", bg_color = "base_bg", grid_mult = 1, borders=False, uidict={}, strtxt = "", diff_draw=True):
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
        self.diff_draw = diff_draw
        #This represents the current widget id being drawn
        self.drawing_id = 0
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
        
        #THIS IS FOR THE SWITCH TO LISTS FROM DICTIONARIES:
        self.winlist = [[self.bg_char] * self.arc_cols for _ in range(self.arc_lines)]
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
        
        for i in range(lines_start - 1, lines_end):
            window_cols_index = 1
            for c in range(cols_start - 1, cols_end):
                self.screen.slist[i][c] = self.winlist[window_lines_index - 1][window_cols_index - 1]
                window_cols_index += 1
            window_lines_index += 1
        #This updates the screen
        if self.diff_draw:
            if self.firstdraw:
                self.screen.fulldraw()
                self.firstdraw = False
            else:
                self.screen.newdraw()
        else:
            if self.firstdraw:
                self.screen.fulldraw()
                self.firstdraw = False
            else:
                self.screen.fulldraw()
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
            #self.window_chars[startline][c] = charec
            self.winlist[startline - 1][c - 1] = charec
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

    #This method does the same as the write method, but writes with user input
    #It captures user input until a app dev set keybinding activates
    def add_inputbox(self, grid_x, grid_y, color="base_text", bg_color="base_win_bg", wrapping=True):
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "input_box"
        self.ui_dict[self.curr_id_num]["grid_x"] = grid_x
        self.ui_dict[self.curr_id_num]["grid_y"] = grid_y
        #Lines, THEN Cols
        self.ui_dict["ui_grid"][grid_y][grid_x] = 1
        self.ui_dict[self.curr_id_num]["color"] = color
        self.ui_dict[self.curr_id_num]["bg_color"] = bg_color
        self.ui_dict[self.curr_id_num]["wrapping"] = wrapping
        self.ui_dict[self.curr_id_num]["txt"] = ""

    def input_write(self, startline=1, startcol=1, endline="max", endcol="max", color="base_text", bg_color="base_win_bg", wrapping=True):
        #If endline and endcol are "max", the text will use all lines (besides starting) and all cols (besides starting)
        if endline == "max":
            endline = self.sizelines
        if endcol == "max":
            endcol = self.sizecols
        self.need_unfocus_current = False
        
        while self.need_unfocus_current == False:
            res = self.screen.get_input()
            if res == "^BACKSPACE":
                self.ui_dict[self.drawing_id]["txt"] = self.ui_dict[self.drawing_id]["txt"][:-1]
                self.ui_dict[self.drawing_id]["txt"] += " "
                self.write(self.ui_dict[self.drawing_id]["txt"], startline, startcol, endline, endcol, color, bg_color, wrapping)
                self.ui_dict[self.drawing_id]["txt"] = self.ui_dict[self.drawing_id]["txt"][:-1]
                self.draw_win()
            elif res == "^ESCAPE":
                self.need_unfocus_current = True
            else:
                self.ui_dict[self.drawing_id]["txt"] = self.ui_dict[self.drawing_id]["txt"][:-1]
                self.ui_dict[self.drawing_id]["txt"] += res
                self.ui_dict[self.drawing_id]["txt"] += "_"
                self.write(self.ui_dict[self.drawing_id]["txt"], startline, startcol, endline, endcol, color, bg_color, wrapping)
                self.draw_win()
        ent_str = self.ui_dict[self.drawing_id]["txt"][:-1]
        self.curr_id_num += 1
        return ent_str
    
    def ui_draw(self):
        txt_to_return = ""
        for i in self.ui_dict:
            #Not skipping through this will cause an error
            if i == "ui_grid":
                continue
            self.drawing_id = i

            #INPUT BOX
            if self.ui_dict[i]["type"] == "input_box":
                txt_to_return = self.input_write()
        return txt_to_return