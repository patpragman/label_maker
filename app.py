"""
Application class skeleton for the app

In the application class we tie everything together, the data model, the controllers, and the functions
that tie controllers (like buttons etc) to the data model

"""

import atexit
import tkinter as tk

from json import load, dump

from os import getcwd, path

# controller panels come from here
from panes.control_pane import ControlPane
from panes.image_pane import ImagePane
from panes.list_pane import ListPane
from data_model.imagescores import Folder, ScoredImage


class Application:

    def __init__(self):

        self.save_state_file = path.join(getcwd(), "savestates/save.json")
        if path.exists(self.save_state_file):
            with open(self.save_state_file, "r") as save_state_file:
                last_directory_worked_on = load(save_state_file)
            self.current_folder = Folder(last_directory_worked_on)
        else:
            self.current_folder = Folder(getcwd())
            with open(self.save_state_file, "w") as save_state_file:
                dump(str(self.current_folder), save_state_file)

        # set up the main tkinter interface for the application
        self.root = tk.Tk()

        # let's configure the root window
        self.root.title("Image Labeler Tool")
        self.root.resizable(False, False)

        # set up the sub panes
        self.image_pane = ImagePane(self.root)
        self.control_pane = ControlPane(self.root)
        self.list_pane = ListPane(self.root)

        # set up the layout of the widgets in the application in the grid
        self.image_pane.grid(row=0, column=0)
        self.control_pane.grid(row=1, column=0)
        self.list_pane.grid(row=0, column=1)

        atexit.register(self.save)
        atexit.register(self.current_folder.save)

    def save(self):
        with open(self.save_state_file, "w") as save_state_file:
            dump(str(self.current_folder), save_state_file)


    def run(self):
        # start the application
        self.root.mainloop()