"""
Application class skeleton for the app

In the application class all the

"""

import tkinter as tk
from panes.control_pane import ControlPane
from panes.image_pane import ImagePane
from panes.list_pane import ListPane


class Application:

    def __init__(self):

        # set up the main tkinter interface for the application
        self.root = tk.Tk()

        # set up the sub panes
        self.image_pane = ImagePane(self.root)
        self.control_pane = ControlPane(self.root)
        self.list_pane = ListPane(self.root)

        # set up the layout of the widgets in the application in the grid
        self.image_pane.grid(row=0, column=0)
        self.control_pane.grid(row=1, column=0)
        self.list_pane.grid(row=0, column=1)

    def run(self):
        # start the application
        self.root.mainloop()