import time
class window:
    def __init__(self, screen_obj, title="Window", bg=" ", bg_color = "base_bg", grid_mult = 5, borders=False, uidict={}, strtxt = "", diff_draw=True, dyn_size = False, initn=True):
        self.firstdraw = True
        self.screen = screen_obj
        self.ui_needs_init = True
        self.need_recalc = False
        lines = self.screen.line_num
        cols = self.screen.col_num
        self.title = title
        self.dyn_size = False
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
        if "draw_id" not in self.ui_dict:
            self.drawing_id = 0
            #NOTE: This version of the drawing ID is not up to date with the current one EXCEPT when window is resized.
            #It is updated in the resize function.
            self.ui_dict["draw_id"] = 0
        else:
            self.drawing_id = self.ui_dict["draw_id"]
        #Makes a grid of widget positions
        #This does not check if it is already been done because it NEEDS to be recalculated on resize
        self.grid_mult = grid_mult
        if "ui_grid" not in self.ui_dict:
            self.ui_dict["ui_grid"] = {}
            for i in range(1, ((grid_mult) + 1)):
                self.ui_dict["ui_grid"][i] = {}
                for c in range(1, ((grid_mult) + 1)):
                    self.ui_dict["ui_grid"][i][c] = 0

        if "ui_pos" not in self.ui_dict:
            self.ui_dict["ui_pos"] = {}
            #ADD MORE HERE
        if "ui_grid_sizes" not in self.ui_dict:
            self.ui_dict["ui_grid_sizes"] = {}
            for i in range(1, ((grid_mult) + 1)):
                self.ui_dict["ui_grid_sizes"][i] = {}
                for c in range(1, ((grid_mult) + 1)):
                    self.ui_dict["ui_grid_sizes"][i][c] = {}

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
        self.ui_dict["draw_id"] = self.drawing_id
        self.screen.clear()
        self.resize += 1
        self.screen.__init__()
        self.__init__(self.screen, self.title, self.bgchoice, self.bgcolor, self.grid_mult, self.borders, self.ui_dict, self.str_text, self.diff_draw, self.dyn_size, initn=True)
        self.get_pos()
        self.need_recalc = True
        self.ui_needs_init = True

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
    def write(self, text, startline=1, startcol=1, endline="max", endcol="max", color="base_text", bg_color="base_win_bg", wrapping=True, focus_force=False):
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
                    if not focus_force:
                        self.need_unfocus_current = True
                if c >= self.sizecols or c >= endcol:
                    startline += 1
                    c = startcol
                else:
                    c += 1     

    #This method does the same as the write method, but writes with user input
    #It captures user input until a app dev set keybinding activates
    def add_inputbox(self, grid_x, grid_y, l_size = 0, c_size = 0, color="base_text", bg_color="base_win_bg", wrapping=True):
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "input_box"
        #if not using dyn sizing, this is the top left corner of grid widget
        self.ui_dict[self.curr_id_num]["grid_x"] = grid_x
        self.ui_dict[self.curr_id_num]["grid_y"] = grid_y
        #if not using dynamic resizing, these are the grid unit sizes of widgets:
        self.ui_dict[self.curr_id_num]["c_ext"] = c_size + 1
        self.ui_dict[self.curr_id_num]["l_ext"] = l_size + 1
        #these sizes being zero means the widget engine has not determined their sizes yet
        self.ui_dict[self.curr_id_num]["l_size"] = 0
        self.ui_dict[self.curr_id_num]["c_size"] = 0
        self.ui_dict[self.curr_id_num]["c_tl"] = 0
        self.ui_dict[self.curr_id_num]["l_tl"] = 0
        #Lines, THEN Cols
        self.ui_dict["ui_grid"][grid_y][grid_x] = self.curr_id_num
        self.ui_dict[self.curr_id_num]["color"] = color
        self.ui_dict[self.curr_id_num]["bg_color"] = bg_color
        self.ui_dict[self.curr_id_num]["wrapping"] = wrapping
        self.ui_dict[self.curr_id_num]["txt"] = ""
        #WIDGET SIZING
        for i in range(grid_y, (l_size + grid_y + 1)):
            for c in range(grid_x, (c_size + grid_x + 1)):
                self.ui_dict["ui_grid"][i][c] = self.curr_id_num

        self.curr_id_num += 1

    def input_write(self, startline=1, startcol=1, endline="max", endcol="max", color="base_text", bg_color="base_win_bg", init=False, firstinit=False, wrapping=True):
        #If endline and endcol are "max", the text will use all lines (besides starting) and all cols (besides starting)
        if endline == "max":
            endline = self.sizelines
        if endcol == "max":
            endcol = self.sizecols
        self.need_unfocus_current = False
        if init:
            space_txt = ""
            for i in range(startline, endline + 1):
                for c in range(startcol, endcol + 1):
                    space_txt += " "
                    self.write(space_txt, startline, startcol, endline, endcol, color, bg_color, wrapping, focus_force=True)
        if firstinit:
            self.ui_dict[self.drawing_id]["txt"] += "_"
            self.write(self.ui_dict[self.drawing_id]["txt"], startline, startcol, endline, endcol, color, bg_color, wrapping)
        if firstinit or init:
            self.draw_win()
        if not init:
            while self.need_unfocus_current == False and self.need_recalc == False:
                res = self.screen.get_input()
                #if res == "":
                #    continue
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
            #self.curr_id_num += 1
            return ent_str
        
    
    def add_text_box(self, text, grid_x, grid_y, l_size = 0, c_size = 0, color="base_text", bg_color="base_win_bg", wrapping=True):
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "text_box"
        #if not using dyn sizing, this is the top left corner of grid widget
        self.ui_dict[self.curr_id_num]["grid_x"] = grid_x
        self.ui_dict[self.curr_id_num]["grid_y"] = grid_y
        #if not using dynamic resizing, these are the grid unit sizes of widgets:
        self.ui_dict[self.curr_id_num]["c_ext"] = c_size + 1
        self.ui_dict[self.curr_id_num]["l_ext"] = l_size + 1
        #these sizes being zero means the widget engine has not determined their sizes yet
        self.ui_dict[self.curr_id_num]["l_size"] = 0
        self.ui_dict[self.curr_id_num]["c_size"] = 0
        self.ui_dict[self.curr_id_num]["c_tl"] = 0
        self.ui_dict[self.curr_id_num]["l_tl"] = 0
        #Lines, THEN Cols
        self.ui_dict["ui_grid"][grid_y][grid_x] = self.curr_id_num
        self.ui_dict[self.curr_id_num]["color"] = color
        self.ui_dict[self.curr_id_num]["bg_color"] = bg_color
        self.ui_dict[self.curr_id_num]["wrapping"] = wrapping
        self.ui_dict[self.curr_id_num]["text"] = text
        #WIDGET SIZING
        for i in range(grid_y, (l_size + grid_y + 1)):
            for c in range(grid_x, (c_size + grid_x + 1)):
                self.ui_dict["ui_grid"][i][c] = self.curr_id_num

        self.curr_id_num += 1


    def text_box(self, id, startline=1, startcol=1, endline="max", endcol="max"):
        color = self.ui_dict[id]["color"]
        bg_color = self.ui_dict[id]["bg_color"]
        wrapping = self.ui_dict[id]["wrapping"]
        text = self.ui_dict[id]["text"]
        self.write(text, startline, startcol, endline, endcol, color, bg_color, wrapping)
        self.draw_win()

    def add_button(self, text, func, grid_x, grid_y, l_size=0, c_size=0, color="base_text", bg_color="base_win_bg"):
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "button"
        #if not using dyn sizing, this is the top left corner of grid widget
        self.ui_dict[self.curr_id_num]["grid_x"] = grid_x
        self.ui_dict[self.curr_id_num]["grid_y"] = grid_y
        #if not using dynamic resizing, these are the grid unit sizes of widgets:
        self.ui_dict[self.curr_id_num]["c_ext"] = c_size + 1
        self.ui_dict[self.curr_id_num]["l_ext"] = l_size + 1
        #these sizes being zero means the widget engine has not determined their sizes yet
        self.ui_dict[self.curr_id_num]["l_size"] = 0
        self.ui_dict[self.curr_id_num]["c_size"] = 0
        self.ui_dict[self.curr_id_num]["c_tl"] = 0
        self.ui_dict[self.curr_id_num]["l_tl"] = 0
        #Lines, THEN Cols
        self.ui_dict["ui_grid"][grid_y][grid_x] = self.curr_id_num
        self.ui_dict[self.curr_id_num]["color"] = color
        self.ui_dict[self.curr_id_num]["bg_color"] = bg_color
        self.ui_dict[self.curr_id_num]["function"] = func
        self.ui_dict[self.curr_id_num]["text"] = text
        #WIDGET SIZING
        for i in range(grid_y, (l_size + grid_y + 1)):
            for c in range(grid_x, (c_size + grid_x + 1)):
                self.ui_dict["ui_grid"][i][c] = self.curr_id_num

        self.curr_id_num += 1

    def button(self, id, startline=1, startcol=1, endline="max", endcol="max", init=False):
        color = self.ui_dict[id]["color"]
        bg_color = self.ui_dict[id]["bg_color"]
        text = self.ui_dict[id]["text"]
        func = self.ui_dict[id]["function"]
        if init:
            self.write(text, startline, startcol, endline, endcol, color, bg_color, True)
            self.draw_win()
        else:
            func()
    
    def add_table(self, dicti, grid_x, grid_y, l_size=0, c_size=0, color="base_text", bg_color="base_win_bg"):
        self.ui_dict[self.curr_id_num] = {}
        self.ui_dict[self.curr_id_num]["type"] = "table"
        #if not using dyn sizing, this is the top left corner of grid widget
        self.ui_dict[self.curr_id_num]["grid_x"] = grid_x
        self.ui_dict[self.curr_id_num]["grid_y"] = grid_y
        #if not using dynamic resizing, these are the grid unit sizes of widgets:
        self.ui_dict[self.curr_id_num]["c_ext"] = c_size + 1
        self.ui_dict[self.curr_id_num]["l_ext"] = l_size + 1
        #these sizes being zero means the widget engine has not determined their sizes yet
        self.ui_dict[self.curr_id_num]["l_size"] = 0
        self.ui_dict[self.curr_id_num]["c_size"] = 0
        self.ui_dict[self.curr_id_num]["c_tl"] = 0
        self.ui_dict[self.curr_id_num]["l_tl"] = 0
        #Lines, THEN Cols
        self.ui_dict["ui_grid"][grid_y][grid_x] = self.curr_id_num
        self.ui_dict[self.curr_id_num]["color"] = color
        self.ui_dict[self.curr_id_num]["bg_color"] = bg_color
        self.ui_dict[self.curr_id_num]["dict"] = dicti
        #WIDGET SIZING
        for i in range(grid_y, (l_size + grid_y + 1)):
            for c in range(grid_x, (c_size + grid_x + 1)):
                self.ui_dict["ui_grid"][i][c] = self.curr_id_num

        self.curr_id_num += 1
    
    def table(self, id, startline=1, startcol=1, endline="max", endcol="max", init=False):
        color = self.ui_dict[id]["color"]
        bg_color = self.ui_dict[id]["bg_color"]
        dicti = self.ui_dict[id]["dict"]
        if init:
            c = 0
            i = 0
            while c < len(dicti):
                strw = "| " + str(dicti[c]) + " | " + str(dicti[c + 1]) + " |"
                stlen = len(strw)
                self.write(strw, startline + i, startcol, endline, endcol, color, bg_color, False)
                self.draw_win()
                if c == 0:
                    i += 1
                    strw = ""
                    for d in range(0, stlen):
                        strw += "_"
                    self.write(strw, startline + i, startcol, endline, endcol, color, bg_color, False)
                    self.draw_win()
                strw = ""
                c += 2
                i += 1
    
    def get_pos(self):
        all_wid_pos = False
        num_widgets = 0
        num_wid_done = 0
        for i in self.ui_dict:
            if i == "ui_grid" or i == "draw_id" or i == "ui_pos" or i == "ui_grid_sizes":
                continue
            num_widgets += 1
        if self.dyn_size:
            #This is code for dynamic resizing (WIP)
            while all_wid_pos == False:
                for i in range(1, num_widgets + 1):
                    val = self.get_dyn_pos(i)
                    if val == 1:
                        num_wid_done += 1
                    if num_wid_done == num_widgets:
                        all_wid_pos = True
            #After the loop, we are calculating the coordinates of the widgets based on the grid extensions calculated prior
            #Here, we calculate the cols and lines of each grid box
            #NOTE: Put exact coords in ui dict for each widget, so that final loop doesnt have to be rewritten
            wid = int(self.arc_cols/self.grid_mult)
            wrem = self.arc_cols%self.grid_mult
            lin = int(self.arc_lines/self.grid_mult)
            lrem = self.arc_lines%self.grid_mult
        else:
            #calculate the width and height of each grid space:
            for i in self.ui_dict["ui_grid_sizes"]:
                for c in self.ui_dict["ui_grid_sizes"][i]:
                    endc = round(c * (self.arc_cols / self.grid_mult))
                    stc = round((c - 1) * (self.arc_cols / self.grid_mult))
                    endl = round(i * (self.arc_lines / self.grid_mult))
                    stl = round((i - 1) * (self.arc_lines / self.grid_mult))
                    self.ui_dict["ui_grid_sizes"][i][c]["lines"] = endl - stl
                    self.ui_dict["ui_grid_sizes"][i][c]["cols"] = endc - stc
            st = ""
            for i in self.ui_dict["ui_grid_sizes"]:
                for c in self.ui_dict["ui_grid_sizes"][i]:
                    st += str(self.ui_dict["ui_grid_sizes"][i][c])
                    st += " "
                print(st)
                st = ""
            print(self.arc_cols)
            print(self.arc_lines)
            for d in self.ui_dict:
                if d == "ui_grid" or d == "draw_id" or d == "ui_pos" or d == "ui_grid_sizes":
                    continue
                tl_lines = 0
                tl_cols = 0
                wid_line_size = 0
                wid_cols_size = 0
                tl_gridx = self.ui_dict[d]["grid_x"]
                tl_gridy = self.ui_dict[d]["grid_y"]
                for i in range(1, tl_gridy + 1):
                    if i == self.ui_dict[d]["grid_y"]:
                        break
                    tl_lines += self.ui_dict["ui_grid_sizes"][i][tl_gridx]["lines"]
                for i in range(1, tl_gridx + 1):
                    if i == self.ui_dict[d]["grid_x"]:
                        break
                    tl_cols += self.ui_dict["ui_grid_sizes"][tl_gridy][i]["cols"]
                #now, calculating the length and width of the widget
                for i in range(tl_gridy, tl_gridy + self.ui_dict[d]["l_ext"]):
                    print(tl_gridy)
                    wid_line_size += self.ui_dict["ui_grid_sizes"][i][tl_gridy]["lines"]
                for i in range(tl_gridx, tl_gridx + self.ui_dict[d]["c_ext"]):
                    wid_cols_size += self.ui_dict["ui_grid_sizes"][tl_gridx][i]["cols"]
                self.ui_dict[d]["c_tl"] = tl_cols
                self.ui_dict[d]["l_tl"] = tl_lines
                self.ui_dict[d]["c_size"] = wid_cols_size
                self.ui_dict[d]["l_size"] = wid_line_size

    def ui_draw(self):
        firstinit = True
        self.get_pos()
        recalc = True
        while recalc:
            did_size = False
            recalc = False
            self.need_recalc = False
            if self.ui_needs_init:
                for i in self.ui_dict:
                    #Not skipping through this will cause an error
                    if i == "ui_grid":
                        continue
                    if i == "draw_id":
                        continue
                    if i == "ui_pos":
                        continue
                    if i == "ui_grid_sizes":
                        continue

                    self.drawing_id = i

                    #need start line, start col, end line, and end col
                    start_line = self.ui_dict[i]["l_tl"]
                    start_col = self.ui_dict[i]["c_tl"]
                    end_line = (self.ui_dict[i]["l_tl"] + self.ui_dict[i]["l_size"]) - 1
                    end_col = (self.ui_dict[i]["c_tl"] + self.ui_dict[i]["c_size"]) - 1
                    print("dim")
                    print(start_line)
                    print(end_line)
                    print(start_col)
                    print(end_col)

                    if self.ui_dict[i]["type"] == "input_box":
                        self.input_write(startcol=start_col, startline=start_line, endcol=end_col, endline=end_line, color=self.ui_dict[i]["color"], bg_color=self.ui_dict[i]["bg_color"], init=True, firstinit=firstinit, wrapping=self.ui_dict[i]["wrapping"])
                        did_size = True
                    self.ui_needs_init = False
                firstinit = False
            for i in self.ui_dict:
                #Not skipping through this will cause an error
                if i == "ui_grid":
                    continue
                if i == "draw_id":
                    continue
                if i == "ui_pos":
                    continue
                if i == "ui_grid_sizes":
                    continue

                self.drawing_id = i

                #need start line, start col, end line, and end col
                start_line = self.ui_dict[i]["l_tl"]
                start_col = self.ui_dict[i]["c_tl"]
                end_line = (self.ui_dict[i]["l_tl"] + self.ui_dict[i]["l_size"]) - 1
                end_col = (self.ui_dict[i]["c_tl"] + self.ui_dict[i]["c_size"]) - 1

                #INPUT BOX
                if self.ui_dict[i]["type"] == "input_box":
                    txt_to_return = self.input_write(startcol=start_col, startline=start_line, endcol=end_col, endline=end_line, color=self.ui_dict[i]["color"], bg_color=self.ui_dict[i]["bg_color"], wrapping=self.ui_dict[i]["wrapping"])
                if self.need_recalc:
                    recalc = True

        return did_size, txt_to_return
    
    def ui_draw_static(self):
        for i in self.ui_dict:
            if i == "ui_grid":
                continue
            if i == "draw_id":
                continue
            if i == "ui_pos":
                continue
            if i == "ui_grid_sizes":
                continue
            self.drawing_id = i
            if i == 1:
                start_line = 1
                start_col = 1
                end_line = 24
                end_col = 40
            if i == 2:
                start_line = 1
                start_col = 41
                end_line = 3
                end_col = 80
            if i == 3:
                start_line = 4
                start_col = 41
                end_line = 6
                end_col = 80
            if i == 4:
                start_line = 7
                start_col = 41
                end_line = 24
                end_col = 80

            if self.ui_dict[i]["type"] == "input_box":
                self.input_write(startcol=start_col, startline=start_line, endcol=end_col, endline=end_line, color=self.ui_dict[i]["color"], bg_color=self.ui_dict[i]["bg_color"], init=True, firstinit=True, wrapping=self.ui_dict[i]["wrapping"])
            elif self.ui_dict[i]["type"] == "text_box":
                self.text_box(i, start_line, start_col, end_line, end_col)
            elif self.ui_dict[i]["type"] == "button":
                self.button(i, start_line, start_col, end_line, end_col, True)
            elif self.ui_dict[i]["type"] == "table":
                self.table(i, start_line, start_col, end_line, end_col, True)
        
        for i in self.ui_dict:
            alpha_dict = {
                "a": 1,
                "b": 2,
                "c": 3,
                "d": 4,
                "e": 5,
                "f": 6,
                "g": 7,
                "h": 8,
                "i": 9,
                "j": 10,
                "k": 11,
                "l": 12,
                "m": 13,
                "n": 14,
                "o": 15,
                "p": 16,
                "q": 17,
                "r": 18,
                "s": 19,
                "t": 20,
                "u": 21,
                "v": 22,
                "w": 23,
                "x": 24,
                "y": 25,
                "z": 26
            }
        
        while self.need_unfocus_current == False:
            chc = ""
            while chc != "^ENTER":
                chc = self.screen.get_input()
                if chc == "^ENTER":
                    break
                elif chc in alpha_dict:
                    wid_in = alpha_dict[chc]
                else: 
                    continue
            
            for i in self.ui_dict:
                if i == "ui_grid":
                    continue
                if i == "draw_id":
                    continue
                if i == "ui_pos":
                    continue
                if i == "ui_grid_sizes":
                    continue
                self.drawing_id = i
                if i == 1:
                    start_line = 1
                    start_col = 1
                    end_line = 24
                    end_col = 40
                if i == 2:
                    start_line = 1
                    start_col = 41
                    end_line = 3
                    end_col = 80
                if i == 3:
                    start_line = 4
                    start_col = 41
                    end_line = 6
                    end_col = 80
                if i == 4:
                    start_line = 7
                    start_col = 41
                    end_line = 24
                    end_col = 80
                if i == wid_in:
                    if self.ui_dict[i]["type"] == "input_box":
                        txt_to_return = self.input_write(startcol=start_col, startline=start_line, endcol=end_col, endline=end_line, color=self.ui_dict[i]["color"], bg_color=self.ui_dict[i]["bg_color"], wrapping=self.ui_dict[i]["wrapping"])
                    elif self.ui_dict[i]["type"] == "button":
                        self.button(i, start_line, start_col, end_line, end_col, False)
                    elif self.ui_dict[i]["type"] == "table":
                        self.table(i, start_line, start_col, end_line, end_col, True)

        return txt_to_return
            
