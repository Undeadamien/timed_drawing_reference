from os import listdir
from random import sample
from tkinter import Button, Label, Tk
from PIL import ImageTk, Image


IMAGE_PATH = "images"  # folder where the images should be located, can be modfied
SLIDE_OFFSET = (0, 80)  # used to adjust the placement of the photo reference
MAX_SLIDE_SIZE = (300, 500)


class OptionWindow(Tk):
    
    """
    This first window allow the user, 
    to set how many image should be displayed and for how long. 
    """
    
    def __init__(self):

        super().__init__()
        self.attributes("-topmost", True)  # keep the fen on top
        self.overrideredirect(True)  # delete the title bar
        self.focus_force()
        
        #set available options
        self.time_duration = [5, 10, 15, 20, 30, 60, 90]  # in minutes
        self.number_of_slide = [x for x in range(1,6)]
        
        #set default choices
        self.time_choice = 0
        self.slide_choice = 4

        self.time_button =  Button(self, text = f"MINUTES\n{self.time_duration[self.time_choice]}",
                                         font = "arial 16 bold",
                                         command = lambda: increase_time(self),
                                         width = 10)

        self.slide_button = Button(self, text=f"SLIDE\n{self.number_of_slide[self.slide_choice]}",
                                         font="arial 16 bold", 
                                         command=lambda: increase_slide(self), 
                                         width = 10)

        self.confirm_button = Button(self,text="CONFIRM",
                                          font="arial 16 bold",
                                          bg="light green",
                                          command=lambda: confirm_choice(self),
                                          width = 10)
        
        #place the button on the window
        self.time_button.grid(column=0, row=0, sticky="nesw")
        self.slide_button.grid(column=1, row=0, sticky="nesw")
        self.confirm_button.grid(columnspan=2, row=1, sticky="nesw")

        #center the window
        SCREEN_SIZE = (self.winfo_screenwidth(), self.winfo_screenheight())
        self.update()
        self.geometry(f"+{SCREEN_SIZE[0]//2-self.winfo_width()//2}"
                      +f"+{SCREEN_SIZE[1]//2-self.winfo_height()//2}")

        def increase_time(self):
            self.time_choice = (self.time_choice+1) % len(self.time_duration)
            self.time_button.configure(text=f"MINUTES\n{self.time_duration[self.time_choice]}")

        def increase_slide(self):
            self.slide_choice = (self.slide_choice+1) % len(self.number_of_slide)
            self.slide_button.configure(text=f"SLIDE\n{self.number_of_slide[self.slide_choice]}")

        def confirm_choice(self):
            global SELECTED_TIME_OPTIONS, SELECTED_SLIDE_OPTIONS
            
            #retrieve the selected options before destroying the window
            SELECTED_TIME_OPTIONS = self.time_duration[self.time_choice] * 60  # convert to seconds
            SELECTED_SLIDE_OPTIONS = self.number_of_slide[self.slide_choice]
            self.destroy()


class SlideWindow(Tk):

    def __init__(self, image_file, time):

        super().__init__()
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.focus_force()
        self.geometry(f"+{SLIDE_OFFSET[0]}+{SLIDE_OFFSET[1]}")  # adjust the placement of the window
        self.configure(bg="black",
                       highlightbackground="black",
                       highlightthickness=2)

        def prepare_image(image):
            loaded_image = Image.open(f"{IMAGE_PATH}\\{image}")
            resized_image = loaded_image.resize((loaded_image.size[0]*2, loaded_image.size[1]*2))
            resized_image.thumbnail(MAX_SLIDE_SIZE)
            return ImageTk.PhotoImage(resized_image)

        def update_timer(self, time):
            time -= 1
            
            if time >= 0: self.after(1000, lambda:update_timer(self, time))
            else: self.destroy()
                
            self.timer.configure(text=f"{(time//60):02}:{(time%60):02}",
                                 font="arial 16 bold", 
                                 bg="white",
                                 highlightbackground="black",
                                 highlightthickness=2)

        self.converted_image = prepare_image(image_file)

        self.timer = Label(self, text="")
        self.slide = Label(self, image=self.converted_image, 
                                 highlightbackground="black",
                                 bg="black")
        
        #place the timer and image on the window
        self.slide.grid(row=1)
        self.timer.grid(row=0, sticky="nesw")
        
        update_timer(self, time+1)  #start the timer

        
def main():

    OptionWindow().mainloop()

    #select randomly k number of image from the image folder
    SELECTED_IMAGES = sample([x for x in listdir(IMAGE_PATH) if x.lower().endswith((".jpg"))], 
                              k=SELECTED_SLIDE_OPTIONS)

    for IMAGE in SELECTED_IMAGES:
        SlideWindow(IMAGE, SELECTED_TIME_OPTIONS).mainloop()


if __name__ == "__main__":
    main()
