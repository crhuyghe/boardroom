import tkinter as tk
from tkinter import ttk
from typing import Iterable

from Frontend.Classes.Components.DarkModeInterface import DarkMode


# Credit to user OysterShucker on StackOverflow
# https://stackoverflow.com/questions/63926996/tkinter-frame-inside-of-canvas-not-expanding-to-fill-area

class ScrollFrame(tk.Frame, DarkMode):
    def __init__(self, master, dark_mode=False, alt_color=False, scrollspeed=5, r=0, c=0, rspan=1, cspan=1, grid={}, **kwargs):
        self.dark_mode = dark_mode
        self.alt_color = alt_color
        if dark_mode:
            if alt_color:
                bg = "#1f2226"
            else:
                bg = "#24272b"
        else:
            if alt_color:
                bg = "#DDDDDD"
            else:
                bg = "#EEEEEE"
        kwargs["background"] = bg
        tk.Frame.__init__(self, master, **{'width': 400, 'height': 300, **kwargs})


        # __GRID
        self.grid(**{'row': r, 'column': c, 'rowspan': rspan, 'columnspan': cspan, 'sticky': 'nswe', **grid})

        # allow user to set width and/or height
        if {'width', 'height'} & {*kwargs}:
            self.grid_propagate(0)

        # give this widget weight on the master grid
        self.master.grid_rowconfigure(r, weight=1)
        self.master.grid_columnconfigure(c, weight=1)

        # give self.frame weight on this grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # _WIDGETS
        self.canvas = tk.Canvas(self, bd=0, bg=self['bg'], highlightthickness=0, yscrollincrement=scrollspeed)
        self.canvas.grid(row=0, column=0, sticky='nswe')

        self.frame = tk.Frame(self.canvas, **kwargs)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        vsb = tk.Scrollbar(self, orient="vertical", jump=True)
        vsb.grid(row=0, column=1, sticky='ns')
        vsb.configure(command=self.canvas.yview)

        # attach scrollbar to canvas
        self.canvas.configure(yscrollcommand=vsb.set)

        # _BINDS
        # canvas resize
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        # frame resize
        self.frame.bind("<Configure>", self.on_frame_configure)
        # scroll wheel
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)

    # makes frame width match canvas width
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)

    # when frame dimensions change pass the area to the canvas scroll region
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # add scrollwheel feature
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / abs(event.delta)), 'units')

    # configure self.frame row(s)
    def rowcfg(self, index, **options):
        index = index if isinstance(index, Iterable) else [index]
        for i in index:
            self.frame.grid_rowconfigure(i, **options)
        # so this can be used inline
        return self

    # configure self.frame column(s)
    def colcfg(self, index, **options):
        index = index if isinstance(index, Iterable) else [index]
        for i in index:
            self.frame.grid_columnconfigure(i, **options)
        # so this can be used inline
        return self

    # Dark mode
    def swap_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            if self.alt_color:
                bg = "#1f2226"
            else:
                bg = "#24272b"
        else:
            if self.alt_color:
                bg = "#DDDDDD"
            else:
                bg = "#EEEEEE"
        self.canvas.configure(bg=bg)
        self.frame.configure(bg=bg)
        self.configure(bg=bg)
