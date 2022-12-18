import tkinter as tk
from panes.control_pane import ControlPane
from panes.image_pane import ImagePane


if __name__ == "__main__":
    rt = tk.Tk()
    image_pane = ImagePane(rt)
    control_pane = ControlPane(rt)

    image_pane.grid(row=0, column=0)
    control_pane.grid(row=1, column=0)

    rt.mainloop()