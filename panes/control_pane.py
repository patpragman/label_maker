import tkinter as tk


class ControlPane(tk.Frame):

    def __init__(self,
                 parent,
                 zero_button_callback=lambda: print('0 button clicked'),
                 one_button_callback=lambda: print('1 button clicked'),
                 two_button_callback=lambda: print('2 button clicked'),
                 three_button_callback=lambda: print('3 button clicked'),
                 mark_uncertain_button_callback=lambda: print('uncertain button clicked'),
                 next_button_callback=lambda: print('next button clicked'),
                 previous_button_callback=lambda: print('previous button clicked'), ):

        super().__init__(parent)

        # dummy frame to hold things more conveniently
        self._frame = tk.Frame()

        # call back functions
        self.zero_button_callback = zero_button_callback
        self.one_button_callback = one_button_callback
        self.two_button_callback = two_button_callback
        self.three_button_callback = three_button_callback
        self.mark_uncertain_button_callback = mark_uncertain_button_callback
        self.next_button_callback = next_button_callback
        self.previous_button_callback = previous_button_callback

        # scoring buttons
        self.zero_button = tk.Button(self._frame, text="0",
                                    command=self.zero_button_callback)
        self.one_button = tk.Button(self._frame, text="1",
                                    command=self.one_button_callback)
        self.two_button = tk.Button(self._frame, text="2",
                                      command=self.two_button_callback)
        self.three_button = tk.Button(self._frame, text="3",
                                     command=self.three_button_callback)
        self.mark_uncertain_button = tk.Button(self._frame, text="mark uncertain",
                                               command=self.mark_uncertain_button_callback)

        # navigation buttons
        self.next_button = tk.Button(self._frame, text="->", command=self.next_button_callback)
        self.previous_button = tk.Button(self._frame, text="<-", command=self.previous_button_callback)


    def grid(self, **kwargs):
        self.zero_button.grid(row=0, column=0)
        self.one_button.grid(row=0, column=1)
        self.two_button.grid(row=0, column=2)
        self.three_button.grid(row=0, column=3)
        self.previous_button.grid(row=1, column=0)
        self.mark_uncertain_button.grid(row=1, column=1, columnspan=2)
        self.next_button.grid(row=1, column=3)

        self._frame.grid(kwargs)




if __name__ == "__main__":
    # module testing code

    root = tk.Tk()
    root.geometry("660x500")
    control_pane = ControlPane(root)

    control_pane.grid()

    root.mainloop()
