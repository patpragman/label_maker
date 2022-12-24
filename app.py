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

from tkinter import filedialog


class Application:

    def __init__(self):

        # save state (last file worked on) code lives here
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
        self.list_pane = ListPane(self.root,
                                  choose_folder_callback=self._choose_folder)

        # set up the layout of the widgets in the application in the grid
        self.image_pane.grid(row=0, column=0)
        self.control_pane.grid(row=1, column=0)
        self.list_pane.grid(row=0, column=1)

        # we need to register these states so they save when you close out of the program
        self._register_save_states()

    def _register_save_states(self):
        # unregister previous state
        atexit.unregister(self.save)
        atexit.register(self.current_folder.save)

        # register new states
        atexit.register(self.save)
        atexit.register(self.current_folder.save)

    def _choose_folder(self):
        # first save the folder you're currently in
        self.current_folder.save()

        # now choose a new folder
        self.current_folder = Folder(filedialog.askdirectory(title="choose the directory you want to explore"))

        # re-register the save states
        self._register_save_states()


    def save(self):
        # open up the save state file, and save the current state
        with open(self.save_state_file, "w") as save_state_file:
            dump(str(self.current_folder), save_state_file)

    def run(self):
        # start the application
        self.root.mainloop()
