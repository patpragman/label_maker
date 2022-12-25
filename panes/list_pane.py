import tkinter as tk
import os

LIST_BOX_COLOR_MAPPING = {
    0: {'bg': 'red'},
    1: {'bg': 'orange'},
    2: {'bg': 'yellow'},
    3: {'bg': 'green'},
    -1: {'bg': 'blue'},
}


class ListPane(tk.Frame):

    def __init__(self, parent,
                 score_paths=None,
                 # the lambda function in here just returns the selected item by default, change this to
                 # something you can use
                 click_select_callback=lambda _: print(f'Selected {_.widget.get(_.widget.curselection()[0])}'),
                 choose_folder_callback=lambda: print("choose folder button pressed")):
        super().__init__(parent)

        # click select callback
        self.click_select_callback = click_select_callback
        self.choose_folder_callback = choose_folder_callback

        # frame to hold all the widgets
        self._frame = tk.Frame(parent)

        self.score_paths = score_paths

        # label for the whole column
        self.pane_label = tk.Label(self._frame, text="Select Filters and Folders")

        # list box configuration
        self._list_box_frame = tk.Frame()
        self.list_box = tk.Listbox(self._frame,
                                   height=24,
                                   selectmode=tk.SINGLE,
                                   selectforeground="Black",
                                   activestyle="none")
        self.list_box.bind("<<ListboxSelect>>", self.click_select_callback)

        # select folders, or filters
        self.select_folder_button = tk.Button(self._frame,
                                              text="Select Folder",
                                              command=self.choose_folder_callback)
        self.select_filter_label = tk.Label(self._frame,
                                            text="Score Filter:")
        self.selected_filter = tk.StringVar()
        self.selected_filter.trace("w",
                                   self.refresh_list_box)
        self.select_score_filter = tk.OptionMenu(self._frame,
                                                 self.selected_filter,
                                                 *["None", -1, 0, 1, 2, 3])

        self.refresh_list_box()

    def refresh_list_box(self, *args):
        self._clear_list_box()

        score_filter = self.selected_filter.get()

        self.list_box.insert(tk.END)

        if self.score_paths:
            for score, path in self.score_paths:

                if score_filter == "None" or score_filter == "":
                    score_filter = -2  # dummy variable to avoid even thinking about it
                else:
                    score_filter = int(score_filter)

                if score == score_filter:
                    continue

                file_name = os.path.split(path)[-1]  # get the filename
                display_string = f"{file_name} - {score}"

                # add it to the list
                self.list_box.insert(tk.END, display_string)
                self.list_box.itemconfig(tk.END, LIST_BOX_COLOR_MAPPING[score])

    def _clear_list_box(self):
        self.list_box.delete(0, tk.END)

    def grid(self, **kwargs):
        self.pane_label.grid(
            row=0, column=0, columnspan=3,
            sticky="ew"
        )

        self.select_folder_button.grid(
            row=1, column=0,
            sticky="ew")
        self.select_filter_label.grid(
            row=1, column=1,
            sticky="ew"
        )
        self.select_score_filter.grid(
            row=1, column=2,
            sticky="ew"
        )

        # set up the list box
        self.list_box.grid(row=2,
                           columnspan=3,
                           sticky="ews")
        self._frame.grid(kwargs, sticky='nsew')


if __name__ == "__main__":
    # manual test code
    import random

    # check grid layout
    root = tk.Tk()
    root.geometry("660x500")

    file_list = [(random.randint(-1, 3), name) for name in os.listdir()]
    print(file_list)
    list_pane = ListPane(root, score_paths=file_list)
    list_pane.grid()

    root.mainloop()
