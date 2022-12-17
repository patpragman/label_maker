import tkinter as tk


class ControlPane(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # dummy frame to hold things more conveniently
        self._frame = tk.Frame()

        # scoring buttons
        self.one_button = tk.Button()
        self.two_button = tk.Button()
        self.three_button = tk.Button()
        self.four_button = tk.Button()
        self.mark_uncertain_button = tk.Button()

        # navigation buttons
        self.next_button = tk.Button()
        self.previous_button = tk.Button()





if __name__ == "__main__":
    # module testing code

    root = tk.Tk()
    root.geometry("660x500")
    image_pane = ControlPane(root)
