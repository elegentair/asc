import time
class window:
    def __init__(self, screen_obj, title="Window", bg=" ", bg_color = "base_bg", grid_mult = 1, borders=False, uidict={}, strtxt = "", diff_draw=True, dyn_size = False):
        self.firstdraw = True
        self.screen = screen_obj
        lines = self.screen.line_num
        cols = self.screen.col_num
        self.title = title
        self.dyn_size = dyn_size
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
            for i in range(1, ((grid_mult * 5) + 1)):
                self.ui_dict["ui_grid"][i] = {}
                for c in range(1, ((grid_mult * 5) + 1)):
                    self.ui_dict["ui_grid"][i][c] = 0

        if "ui_pos" not in self.ui_dict:
            self.ui_dict["ui_pos"] = {}
            #ADD MORE HERE

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
        self.__init__(self.screen, self.title, self.bgchoice, self.bgcolor, self.grid_mult, self.borders, self.ui_dict, self.str_text, self.diff_draw, self.dyn_size)

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
        #these sizes being zero means the widget engine has not determined their sizes yet
        self.ui_dict[self.curr_id_num]["l_size"] = 0
        self.ui_dict[self.curr_id_num]["c_size"] = 0
        #Lines, THEN Cols
        self.ui_dict["ui_grid"][grid_y][grid_x] = self.curr_id_num
        self.ui_dict[self.curr_id_num]["color"] = color
        self.ui_dict[self.curr_id_num]["bg_color"] = bg_color
        self.ui_dict[self.curr_id_num]["wrapping"] = wrapping
        self.ui_dict[self.curr_id_num]["txt"] = ""
        self.curr_id_num += 1

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
        #self.curr_id_num += 1
        return ent_str
    
    def get_dyn_pos(self, id):
        #This function determines by how many grid steps a widget size can be extended.
        #NOTE: For it to do this, it must be called in a loop until calling it with all widgets returns 1
        gridx = self.ui_dict[id]["grid_x"]
        gridy = self.ui_dict[id]["grid_y"]
        if id not in self.ui_dict["ui_pos"]:
            self.ui_dict["ui_pos"][id] = {}
            #Diagonals are not yet added here.
            # "*_size" Vals are out of 5 (or grid_mult), will be turned into fractions later, and are not addable.
            # They represent how many grid units can be added to each side, but do not account for the 1x1 size of the original grid position.
            e_left = True
            l_size = 0

            r_size = 0
            e_right = True

            u_size = 0
            e_up = True

            d_size = 0
            e_down = True

            #top left
            tl_size = 0
            e_tl = True

            #top right
            tr_size = 0
            e_tr = True

            #bottom left
            bl_size = 0
            e_bl = True

            #bottom right
            br_size = 0
            e_br = True 

            curr_left_extent = gridx
            curr_right_extent = gridx
            curr_up_extent = gridy
            curr_down_extent = gridy
            curr_tl_left_extent = gridx
            curr_tl_up_extent = gridy
            curr_tr_right_extent = gridx
            curr_tr_up_extent = gridy
            curr_bl_left_extent = gridx
            curr_bl_down_extent = gridy
            curr_br_right_extent = gridx
            curr_br_down_extent = gridy
        else:
            e_up = self.ui_dict["ui_pos"][id]["e_up"]
            e_down = self.ui_dict["ui_pos"][id]["e_down"]
            e_left = self.ui_dict["ui_pos"][id]["e_left"]
            e_right = self.ui_dict["ui_pos"][id]["e_right"]
            e_tl = self.ui_dict["ui_pos"][id]["e_tl"]
            e_tr = self.ui_dict["ui_pos"][id]["e_tr"]
            e_bl = self.ui_dict["ui_pos"][id]["e_bl"]
            e_br = self.ui_dict["ui_pos"][id]["e_br"]

            u_size = self.ui_dict["ui_pos"][id]["u_size"]
            d_size = self.ui_dict["ui_pos"][id]["d_size"]
            l_size = self.ui_dict["ui_pos"][id]["l_size"]
            r_size = self.ui_dict["ui_pos"][id]["r_size"]
            tl_size = self.ui_dict["ui_pos"][id]["tl_size"]
            tr_size = self.ui_dict["ui_pos"][id]["tr_size"]
            bl_size = self.ui_dict["ui_pos"][id]["bl_size"]
            br_size = self.ui_dict["ui_pos"][id]["br_size"]

            curr_left_extent = self.ui_dict["ui_pos"][id]["curr_left_extent"]
            curr_right_extent = self.ui_dict["ui_pos"][id]["curr_right_extent"]
            curr_up_extent = self.ui_dict["ui_pos"][id]["curr_up_extent"]
            curr_down_extent = self.ui_dict["ui_pos"][id]["curr_down_extent"]
            curr_tl_up_extent = self.ui_dict["ui_pos"][id]["curr_tl_up_extent"]
            curr_tl_left_extent = self.ui_dict["ui_pos"][id]["curr_tl_left_extent"]
            curr_tr_right_extent = self.ui_dict["ui_pos"][id]["curr_tr_right_extent"]
            curr_tr_up_extent = self.ui_dict["ui_pos"][id]["curr_tr_up_extent"]
            curr_bl_left_extent = self.ui_dict["ui_pos"][id]["curr_bl_left_extent"]
            curr_bl_down_extent = self.ui_dict["ui_pos"][id]["curr_bl_down_extent"]
            curr_br_right_extent = self.ui_dict["ui_pos"][id]["curr_br_right_extent"]
            curr_br_down_extent = self.ui_dict["ui_pos"][id]["curr_br_down_extent"]

        if e_left == True:
            if curr_left_extent == 1:
                e_left = False
            elif self.ui_dict["ui_grid"][gridy][curr_left_extent - 1] == 0:
                self.ui_dict["ui_grid"][gridy][curr_left_extent - 1] = id
                curr_left_extent -= 1
                l_size += 1
            else:
                e_left = False
        
        if e_right == True:
            if curr_right_extent == 5:
                e_right = False
            elif self.ui_dict["ui_grid"][gridy][curr_right_extent + 1] == 0:
                self.ui_dict["ui_grid"][gridy][curr_right_extent + 1] = id
                curr_right_extent += 1
                r_size += 1
            else:
                e_right = False

        if e_up == True:
            if curr_up_extent == 5:
                e_up = False
            elif self.ui_dict["ui_grid"][curr_up_extent + 1][gridx] == 0:
                self.ui_dict["ui_grid"][curr_up_extent + 1][gridx] = id
                curr_up_extent += 1
                u_size += 1
            else:
                e_up = False
        
        if e_down == True:
            if curr_down_extent == 1:
                e_down = False
            elif self.ui_dict["ui_grid"][curr_down_extent - 1][gridx] == 0:
                self.ui_dict["ui_grid"][curr_down_extent - 1][gridx] = id
                curr_down_extent -= 1
                d_size += 1
            else:
                e_down = False

        if e_tl == True:
            if curr_tl_up_extent == 5 or curr_tl_left_extent == 1:
                e_tl = False
            elif self.ui_dict["ui_grid"][curr_tl_up_extent + 1][curr_tl_left_extent - 1] == 0 and self.ui_dict["ui_grid"][curr_tl_up_extent + 1][gridx] == 0 and self.ui_dict["ui_grid"][gridy][curr_tl_left_extent - 1] == 0:
                self.ui_dict["ui_grid"][curr_tl_up_extent + 1][curr_tl_left_extent - 1] = id
                curr_tl_up_extent += 1
                curr_tl_left_extent -= 1
                tl_size += 1
            else:
                e_tl = False

        if e_tr == True:
            if curr_tr_up_extent == 5 or curr_tr_right_extent == 5:
                e_tr = False
            elif self.ui_dict["ui_grid"][curr_tr_up_extent + 1][curr_tr_right_extent + 1] == 0 and self.ui_dict["ui_grid"][curr_tr_up_extent + 1][gridx] == 0 and self.ui_dict["ui_grid"][gridy][curr_tr_right_extent + 1] == 0:
                self.ui_dict["ui_grid"][curr_tr_up_extent + 1][curr_tr_right_extent + 1] = id
                curr_tr_up_extent += 1
                curr_tr_right_extent += 1
                tr_size += 1
            else:
                e_tr = False

        if e_bl == True:
            if curr_bl_down_extent == 1 or curr_bl_left_extent == 1:
                e_bl = False
            elif self.ui_dict["ui_grid"][curr_bl_down_extent - 1][curr_bl_left_extent - 1] == 0 and self.ui_dict["ui_grid"][curr_bl_down_extent - 1][gridx] == 0 and self.ui_dict["ui_grid"][gridy][curr_bl_left_extent - 1] == 0:
                self.ui_dict["ui_grid"][curr_bl_down_extent - 1][curr_bl_left_extent - 1] = id
                curr_bl_down_extent -= 1
                curr_bl_left_extent -= 1
                bl_size += 1
            else:
                e_bl = False

        if e_br == True:
            if curr_br_down_extent == 1 or curr_br_right_extent == 5:
                e_br = False
            elif self.ui_dict["ui_grid"][curr_br_down_extent - 1][curr_br_right_extent + 1] == 0 and self.ui_dict["ui_grid"][curr_br_down_extent - 1][gridx] == 0 and self.ui_dict["ui_grid"][gridy][curr_br_right_extent + 1] == 0:
                self.ui_dict["ui_grid"][curr_br_down_extent - 1][curr_br_right_extent + 1] = id
                curr_br_down_extent -= 1
                curr_br_right_extent += 1
                br_size += 1
            else:
                e_br = False

        self.ui_dict["ui_pos"][id]["e_up"] = e_up
        self.ui_dict["ui_pos"][id]["e_down"] = e_down
        self.ui_dict["ui_pos"][id]["e_left"] = e_left
        self.ui_dict["ui_pos"][id]["e_right"] = e_right
        self.ui_dict["ui_pos"][id]["e_tl"] = e_tl
        self.ui_dict["ui_pos"][id]["e_tr"] = e_tr
        self.ui_dict["ui_pos"][id]["e_bl"] = e_bl
        self.ui_dict["ui_pos"][id]["e_br"] = e_br

        self.ui_dict["ui_pos"][id]["u_size"] = u_size
        self.ui_dict["ui_pos"][id]["d_size"] = d_size
        self.ui_dict["ui_pos"][id]["l_size"] = l_size
        self.ui_dict["ui_pos"][id]["r_size"] = r_size
        self.ui_dict["ui_pos"][id]["tl_size"] = tl_size
        self.ui_dict["ui_pos"][id]["tr_size"] = tr_size
        self.ui_dict["ui_pos"][id]["bl_size"] = bl_size
        self.ui_dict["ui_pos"][id]["br_size"] = br_size

        self.ui_dict["ui_pos"][id]["curr_left_extent"] = curr_left_extent
        self.ui_dict["ui_pos"][id]["curr_right_extent"] = curr_right_extent
        self.ui_dict["ui_pos"][id]["curr_up_extent"] = curr_up_extent
        self.ui_dict["ui_pos"][id]["curr_down_extent"] = curr_down_extent
        self.ui_dict["ui_pos"][id]["curr_tl_up_extent"] = curr_tl_up_extent
        self.ui_dict["ui_pos"][id]["curr_tl_left_extent"] = curr_tl_left_extent
        self.ui_dict["ui_pos"][id]["curr_tr_right_extent"] = curr_tr_right_extent
        self.ui_dict["ui_pos"][id]["curr_tr_up_extent"] = curr_tr_up_extent
        self.ui_dict["ui_pos"][id]["curr_bl_left_extent"] = curr_bl_left_extent
        self.ui_dict["ui_pos"][id]["curr_bl_down_extent"] = curr_bl_down_extent
        self.ui_dict["ui_pos"][id]["curr_br_right_extent"] = curr_br_right_extent
        self.ui_dict["ui_pos"][id]["curr_br_down_extent"] = curr_br_down_extent
        
        if e_left == False and e_right == False and e_up == False and e_down == False and e_tl == False and e_tr == False and e_bl == False and e_br == False:
            return 1
        else:
            return 0
        #return (f"UP: {u_size} DOWN: {d_size} LEFT: {l_size} RIGHT: {r_size}, TL: {tl_size}, TR: {tr_size}, BL: {bl_size}, BR: {br_size}")

    def get_pos(self, id):
        print("TEST")
    
    def ui_draw(self):
        txt_to_return = ""
        #If this is true, all widgets have had their positions calculated
        all_wid_pos = False
        num_widgets = 0
        num_wid_done = 0
        for i in self.ui_dict:
            if i == "ui_grid" or i == "draw_id" or i == "ui_pos":
                continue
            num_widgets += 1
        if self.dyn_size:
            #This is code for dynamic resizing (WIP)
            while all_wid_pos == False:
                for i in range(1, num_widgets + 1):
                    val = self.get_pos(i)
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

            for i in self.ui_dict:
                if i == "ui_grid" or i == "draw_id" or i == "ui_pos":
                    continue
                self.ui_dict[i]["l_size"] = lin * (self.ui_dict["ui_pos"][i]["u_size"])
                self.ui_dict[i]["c_size"] = wid
                if lrem > 0:
                    self.ui_dict[i]["l_size"] += 1
                    lrem -= 1
                if wrem > 0:
                    self.ui_dict[i]["c_size"] += 1
                    wrem -= 1
        else:
            #NON DYNAMIC RESIZING:
            print("HI")


        for i in self.ui_dict:
            #Not skipping through this will cause an error
            if i == "ui_grid":
                continue
            if i == "draw_id":
                continue
            if i == "ui_pos":
                continue

            self.drawing_id = i

            #INPUT BOX
            if self.ui_dict[i]["type"] == "input_box":
                txt_to_return = self.input_write(color=self.ui_dict[i]["color"], bg_color=self.ui_dict[i]["bg_color"], wrapping=self.ui_dict[i]["wrapping"])
        return txt_to_return