import os
import random
import tkinter as tk

from panes.control_pane import ControlPane
from panes.image_pane import ImagePane
from panes.list_pane import ListPane

if __name__ == "__main__":
    rt = tk.Tk()
    image_pane = ImagePane(rt)
    control_pane = ControlPane(rt)



    test_file_list = [(random.randint(-1, 3), name) for name in os.listdir()]
    list_pane = ListPane(rt, test_file_list)

    image_pane.grid(row=0, column=0)
    control_pane.grid(row=1, column=0)
    list_pane.grid(row=0, column=1)

    rt.mainloop()