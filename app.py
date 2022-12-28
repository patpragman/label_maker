"""
Application class skeleton for the app

In the application class we tie everything together, the data model, the controllers, and the functions
that tie controllers (like buttons etc) to the data model

"""

import atexit
import tkinter as tk

from operator import add, sub

from json import load, dump

from os import getcwd, path

# controller panels come from here
from panes.control_pane import ControlPane
from panes.image_pane import ImagePane
from panes.list_pane import ListPane
from data_model.imagescores import Folder, ScoredImage

from tkinter import filedialog
from tkinter import messagebox


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

        # image sub-pane
        self.image_pane = ImagePane(self.root)

        self.control_pane = ControlPane(self.root,
                                        zero_button_callback=lambda: self._set_current_image_score(0),
                                        one_button_callback=lambda: self._set_current_image_score(1),
                                        two_button_callback=lambda: self._set_current_image_score(2),
                                        three_button_callback=lambda: self._set_current_image_score(3),
                                        mark_uncertain_button_callback=lambda: self._set_current_image_score(-1),
                                        )

        self.list_pane = ListPane(self.root,
                                  score_paths=[(image.score, image.path) for image in self.current_folder],
                                  choose_folder_callback=self._choose_folder,
                                  click_select_callback=self._click_select_image)
        self._selected_index = 0

        """
        Now let's set up the required keyboard commands, this could be abstracted, but it's less clear
        if I do that.       
        """

        # bind the numpad
        self.root.bind('<KP_0>', lambda _: self._set_current_image_score(0))
        self.root.bind('<KP_1>', lambda _: self._set_current_image_score(1))
        self.root.bind('<KP_2>', lambda _: self._set_current_image_score(2))
        self.root.bind("<KP_3>", lambda _: self._set_current_image_score(3))

        # numbers
        self.root.bind('0', lambda _: self._set_current_image_score(0))
        self.root.bind('1', lambda _: self._set_current_image_score(1))
        self.root.bind('2', lambda _: self._set_current_image_score(2))
        self.root.bind("3", lambda _: self._set_current_image_score(3))

        # left right arrow keys
        self.root.bind('<Left>', lambda _: self._move(sub))
        self.root.bind('<Right>', lambda _: self._move(add))


        # set up the layout of the widgets in the application in the grid
        self.image_pane.grid(row=0, column=0)
        self.control_pane.grid(row=1, column=0)
        self.list_pane.grid(row=0, column=1)

        # we need to register these states, so they save when you close out of the program
        self._register_save_states()

        self._refresh_all()

    def _move(self, f):
        self._selected_index = f(self._selected_index, 1)

        if self.list_pane.list_box.size() == 0:
            return None

        if self._selected_index >= self.list_pane.list_box.size():
            self._selected_index = 0
        elif self._selected_index < 0:
            self._selected_index = self.list_pane.list_box.size() - 1


        self._refresh_all()

    def _set_current_image_score(self, score):
        self.current_folder.current_image.score = score
        self._move(add)
        self._refresh_all()

    def _register_save_states(self):
        # unregister previous state
        atexit.unregister(self.save)
        atexit.register(self.current_folder.save)

        # register new states
        atexit.register(self.save)
        atexit.register(self.current_folder.save)

    def _refresh_all(self):
        # now, handle the list pane
        self.list_pane.score_paths = [(image.score, image.path) for image in self.current_folder]

        # raise a warning when all images checked
        if all(image.score != -1 for image in self.current_folder):
            messagebox.showinfo("showwarning", "all files checked")

        self.list_pane.refresh_list_box()
        self.list_pane.list_box.select_set(self._selected_index)
        self._refresh_image()

    def _choose_folder(self):
        # first save the folder you're currently in
        self.current_folder.save()

        # now choose a new folder
        self.current_folder = Folder(filedialog.askdirectory(title="choose the directory you want to explore",
                                                             initialdir=self.current_folder))

        # re-register the save states
        self._register_save_states()

        # now refresh the whole app
        self._refresh_all()

    def _refresh_image(self):

        short_path = self.list_pane.list_box.get(first=self._selected_index).split(" - ")[0]
        full_path = path.join(self.current_folder.path, short_path)

        images = [image for image in self.current_folder if image.path == full_path]
        self.current_folder.current_image = images[0] if images else None

        self.image_pane.change_image(str(self.current_folder.current_image))

    def _click_select_image(self, _):

        self._selected_index = _.widget.curselection()[0]
        self._refresh_all()

    def save(self):
        # open up the save state file, and save the current state
        with open(self.save_state_file, "w") as save_state_file:
            dump(str(self.current_folder), save_state_file)

    def run(self):
        # start the application
        self.root.mainloop()
