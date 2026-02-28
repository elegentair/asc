# asc
A (future) TUI tookit to run anywhere!  

This is an in-progress TUI (text user interface) toolkit project! Currently, it is at a very elementry stage, only being able to run a window with text input inside it.   

The goal for this project is to have apps written in the toolkit run on any platform (including platforms other than desktop terminals). As such, its defining feature is the seperation between software specific tools (i.e, escape charecters, setting cbreak mode, stdin) and the main toolkit code. This allows (in the future) cross platform compatibility. To add a platform, all one has to do is rewrite the screen class (asc_screen.py) to use inpout & output commands for that specifc platform.  

This project was borne out of the idea to create an entire userland of apps and menus on a microcontroller running circutpython. Because circutpython does not have "cbreak mode" and the other abstractions that Linux provides, other apps would not run without these abstractions being taken away. The microcontroller idea has since been replaced by a pi zero running a custom buildroot Linux os (just in the ideation phase), but this toolkit still serves as a way to develop cross platform applications.  

Currently, this project is in its infancy. As described above, its only main function is to write a window to the screen and input text to it. Below, I have listed all planned features for the toolkit:  

*Planned Features:*  
Window resizing (automatic) to terminal size, with dynamic resizing of all widgets inside the window  
A robust input system inspired by qutebrowser, where each "clickable" ui element is given a activator key  
Button widgets that the user can activate  
List and table widgets  
Make text input windows application readable  
Menubar widgets  
Wrapper abstractions to read and write from files easily  
Vertical scrollbars
