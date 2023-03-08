"""
A little app that pick random picture from a folder and display them for a
determined time
"""

from os import listdir
from random import sample
from tkinter import Button, Canvas, Label, Scale, Tk

from PIL import Image, ImageTk

IMAGE_MAX_SIZE = 350, 500
IMAGE_PATH = "C:\\Users\\Damien\\Desktop\\DRAWING_\\Photo_ref"
IMAGE_FILES = [x for x in listdir(IMAGE_PATH)
               if x.lower().endswith((".jpg", ".png"))]


class SetupWindow(Tk):
    """This window allows to select how many images to show and for how long"""
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.attributes("-topmost", True)  # keep the window on top
        self.overrideredirect(True)
        self.configure(bg="black",
                       highlightthickness=2,
                       highlightbackground="DarkOrange",
                       highlightcolor="DarkOrange")

        self.time_slider = Scale(self,
                                 showvalue=False,
                                 from_=5,
                                 to=30,
                                 tickinterval=5,
                                 bigincrement=5,
                                 orient="horizontal",
                                 font=("Small Fonts", 10, "bold"),
                                 length=200,
                                 bg="black",
                                 fg="white",
                                 resolution=5,
                                 highlightthickness=1,
                                 highlightbackground="DarkOrange",
                                 border=10)
        self.image_slider = Scale(self,
                                  showvalue=False,
                                  from_=1,
                                  to=10,
                                  tickinterval=1,
                                  orient="horizontal",
                                  font=("Small Fonts", 10, "bold"),
                                  length=200,
                                  bg="black",
                                  fg="white",
                                  highlightthickness=1,
                                  highlightbackground="DarkOrange",
                                  border=10)
        self.time_info = Label(self,
                               text="MINUTES",
                               font=("Small Fonts", 15, "bold"),
                               bg="black",
                               fg="white",
                               highlightthickness=1,
                               highlightbackground="DarkOrange",
                               pady=10)
        self.image_info = Label(self,
                                text="IMAGE",
                                font=("Small Fonts", 15, "bold"),
                                bg="black",
                                fg="white",
                                highlightthickness=1,
                                highlightbackground="DarkOrange",
                                pady=10)
        self.confirm_button = Button(self,
                                     text="CONFIRM",
                                     font=("Small Fonts", 15, "bold"),
                                     bg="DarkOrange",
                                     fg="white",
                                     relief="groove",
                                     command=self.confirm)

        self.time_slider.set(1)
        self.image_slider.set(4)

        self.time_info.grid(row=0, sticky="nesw", )
        self.time_slider.grid(row=1)
        self.image_info.grid(row=0, column=1, sticky="nesw")
        self.image_slider.grid(row=1, column=1)
        self.confirm_button.grid(row=2, columnspan=2, sticky="nesw")
        self.recenter()

    def recenter(self):
        """Recenter the window"""
        screen_size = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.update()  # the window has to be updated to consider is new size
        self.geometry(f"+{screen_size[0]//2-self.winfo_width()//2}" +
                      f"+{screen_size[1]//2-self.winfo_height()//2}")

    def confirm(self):
        """Launch the reference window and close the setup window"""
        # must be in this order
        time_value = self.time_slider.get()
        image_value = self.image_slider.get()
        self.destroy()
        ReferenceWindow(time_value*60,
                        sample(IMAGE_FILES, image_value)).mainloop()


class ReferenceWindow(Tk):
    """This window allows to select how many images to show and for how long"""
    def __init__(self, time, images):
        super().__init__()
        self.overrideredirect(True)
        self.geometry("+0+80")
        self.attributes("-topmost", True)
        self.focus_force()

        self.grid_columnconfigure(1, weight=2)

        self.duration = time
        self.remaining_time = self.duration

        self.images = self.prepare_image(images)
        self.current_image = 0

        self.paused = False

        # store Tk.after call from the timer function
        self.timer_update = None

        # value used during the dragging to keep the cursor
        # in place relative to the window
        self.start_x, self.start_y = None, None

        self.configure(bg="black",
                       highlightcolor="black",
                       highlightbackground="black",
                       highlightthickness=2)
        # place holder for the timer
        self.timer = Label(self)
        self.cover = Canvas(self,
                            bg="gray20",
                            border=0,
                            highlightthickness=1,
                            highlightbackground="black",
                            highlightcolor="black")
        self.picture = Label(self,
                             image=self.images[self.current_image],
                             highlightbackground="black",
                             bg="black")
        self.exit_button = Button(self,
                                  text="X",
                                  bg="white",
                                  fg="black",
                                  font=("Small Fonts", 10, "bold"),
                                  highlightcolor="black",
                                  highlightbackground="white",
                                  relief="flat",
                                  height=1,
                                  width=2,
                                  command=self.destroy)
        self.pause_button = Button(self,
                                   text="II",
                                   bg="white",
                                   fg="black",
                                   font=("Small Fonts", 10, "bold"),
                                   highlightcolor="black",
                                   highlightbackground="white",
                                   relief="flat",
                                   height=1,
                                   width=2,
                                   command=self.pause)

        self.timer.grid(row=0, column=1, sticky="nesw")
        self.picture.grid(row=1, column=0, columnspan=3)
        self.pause_button.grid(row=0, column=0, sticky="nesw", pady=2, padx=2)
        self.exit_button.grid(row=0, column=2, sticky="nesw", pady=2, padx=2)

        # handle the dragging feature
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

        self.update_clock()  # start the timer

    def prepare_image(self, images):
        """Convert a list of images into a list of ImageTk.PhotoImage"""
        prepared_images = []
        for image in images:
            loaded_image = Image.open(f"{IMAGE_PATH}\\{image}")
            resized_image = loaded_image.resize((loaded_image.size[0]*2,
                                                 loaded_image.size[1]*2))
            resized_image.thumbnail(IMAGE_MAX_SIZE)
            prepared_images.append(ImageTk.PhotoImage(resized_image))
        return prepared_images

    def pause(self):
        """Allow the user to pause and hide the picture"""
        self.paused = not self.paused
        if self.paused:
            self.after_cancel(self.timer_update)
            self.cover.configure(height=self.picture.winfo_height()-2,
                                 width=self.picture.winfo_width()-2)
            self.picture.grid_forget()
            self.cover.grid(row=1, column=0, columnspan=3)
        else:
            self.picture.grid(row=1, column=0, columnspan=3)
            self.cover.grid_forget()
            self.timer_update = self.after(500, self.update_clock)

    def next_image(self):
        """Reset the timer and switch for the next image"""
        self.current_image += 1
        if self.current_image <= len(self.images)-1:
            self.picture.configure(image=self.images[self.current_image])
            self.after_cancel(self.timer_update)
            self.remaining_time = self.duration
            self.update_clock()
        else:
            self.destroy()

    def update_clock(self):
        """This function act as a timer, calling it self after 1s"""
        text = f"{(self.remaining_time//60):02}:{(self.remaining_time%60):02}"
        self.timer.configure(text=text,
                             font=("Small Fonts", 15, "bold"),
                             bg="white",
                             highlightbackground="black",
                             highlightthickness=2)

        if self.remaining_time >= 0:
            self.timer_update = self.after(1000, self.update_clock)
        else:
            self.next_image()
        if not self.paused:
            self.remaining_time -= 1

    def start_move(self, event):
        """Keep the position where the window start moving"""
        self.start_x, self.start_y = event.x, event.y

    def stop_move(self, _):
        """Reset start_x and start_y """
        self.start_x, self.start_y = None, None

    def do_move(self, event):
        """Allow the user to move the window"""
        self.geometry(f"+{self.winfo_x() + event.x - self.start_x}" +
                      f"+{self.winfo_y() + event.y - self.start_y}")


def main():
    """
    Execute the setup window to define the parameters,
    then select randomly some images from a folder and finally
    initialize the reference window
    """
    SetupWindow().mainloop()


if __name__ == "__main__":
    main()
