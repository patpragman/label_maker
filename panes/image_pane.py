import os.path
import tkinter as tk
from PIL import ImageTk, Image
import os

DISPLAY_IMAGE_WIDTH = 640
DISPLAY_IMAGE_HEIGHT = 480
WORKING_DIR = os.getcwd()

class ImagePane(tk.Frame):

    def __init__(self, parent,
                 image_path=None):

        super().__init__(parent)
        self.configure(width=DISPLAY_IMAGE_WIDTH,
                       height=DISPLAY_IMAGE_HEIGHT)

        # this contains the file path to the image
        self.image_path = image_path

        # this frame object contains all the information so that multiple styles, etc. could be used
        self._frame = tk.Frame()
        self._image_object = None

        # this label actually holds the image
        self.image_holder = tk.Label(self._frame)
        self.image_label_variable = tk.StringVar(self.image_path)
        self.image_label = tk.Label(self._frame, textvariable=self.image_label_variable)

        self.change_image(self.image_path)

    def change_image(self, image_path):
        # in this function, we need to load the image object, or if it's not available display an error message


        """
        we have 4 cases here:
            case 1:
                None type passed to the "change image function"

                in this case we should load up the image that specifies that you should a folder

            case 2:
                Bad path is passed to the "change image function"

                in this case we need to alert the user that this was a bad path

            case 3:

                the image isn't a JPEG or PNG or jpeg, so we alert the user

            case 4:

                finally, everything was fine, so we load the image
        """

        # handle case 1
        if not image_path:
            self.image_label_variable.set('no image folder currently loaded')
            self.image_path = os.path.join(WORKING_DIR,"panes/images/load_an_image.png")
        else:
            # handle case 2
            if not os.path.exists(image_path):
                self.image_label_variable.set(f"path: {image_path} is a bad path, try something else")
                self.image_path = os.path.join(WORKING_DIR,"panes/images/bad_path.png")
            else:
                # handle case 3
                if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.image_label_variable.set(
                        f"can only load .png, .jpeg, or .jpg files, not .{image_path.split('.')[-1]}")
                    self.image_path = os.path.join(WORKING_DIR, "panes/images/wrong_format.png")
                else:
                    # otherwise case 4
                    self.image_path = image_path
                    self.image_label_variable.set(image_path)

        # now load the image
        self._image_object = ImageTk.PhotoImage(
            Image.open(self.image_path)
        )
        self.image_holder.configure(image=self._image_object)


    def grid(self, **kwargs):
        self.image_label.grid(row=0)
        self.image_holder.grid(column=0)
        self._frame.grid(kwargs)

    def pack(self, **kwargs):
        self.image_label.pack(side=tk.TOP)
        self.image_holder.pack(side=tk.BOTTOM)
        self._frame.pack(kwargs)


if __name__ == "__main__":
    # manual test code

    # check grid layout
    root = tk.Tk()
    root.geometry("660x500")
    image_pane = ImagePane(root)
    image_pane.grid(row=0, column=0)

    # press any key to load an image
    root.bind('<a>', lambda x: image_pane.change_image("imagasdfes/gradschoolitis.jpg"))
    root.bind('<s>', lambda x: image_pane.change_image("image_pane.py"))
    root.bind('<d>', lambda x: image_pane.change_image("images/gradschoolitis.jpg"))
    root.bind("<f>", lambda x: image_pane.change_image(None))

    root.mainloop()

    # check pack layout
    root_2 = tk.Tk()
    root_2.geometry("660x500")
    image_pane = ImagePane(root_2)
    image_pane.pack()

    # press any key to load an image
    root_2.bind('<a>', lambda x: image_pane.change_image("imagasdfes/gradschoolitis.jpg"))
    root_2.bind('<s>', lambda x: image_pane.change_image("image_pane.py"))
    root_2.bind('<d>', lambda x: image_pane.change_image("images/gradschoolitis.jpg"))
    root_2.bind("<f>", lambda x: image_pane.change_image(None))

    root_2.mainloop()