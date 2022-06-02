from tkinter import *
from PIL import Image, ImageTk

#
# Managers
#

# The game manager (runtime environment for the game)
class GameManager():
    def __init__(self):
        self.run = True
        self.root = Tk()
        self.height = 600
        self.width = 1000
        self.root.title("EzSoil Game")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.frame = Frame(self.root)
        self.frame.pack(side="top", expand=True, fill="both")
        frame_manager = frameManager(self)
        plantManager().spawn(frame_manager.bathroom)
        print("TICKERRR NEEDS TO BE HAPPENING ONCE A SECOND")
        self.main_loop()
       
    def main_loop(self):
        self.root.mainloop()

# Frame manager
class frameManager():
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.menu = menu(self)
        self.bathroom = bathroom(self)

        self.menu.show()

    def clear(self):
        for widgets in self.game_manager.frame.winfo_children():
            widgets.destroy()
            
class plantManager():
    def __init__(self):
        print("ahh yes")
    def spawn(self, environment=None):
        print("spawning plant in random location, unless otherwise requested")

#
# Manager subclasses
#

class plant():
    def __init__(self, environment):
        print("choosing type of plant (from database) and spawning at requested environment")
        
    def update(self):
        print("depending on the time elaspsed, update the plant conditiosns accordingly")

# Frame sub class
class bathroom():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame
        self.plants = []

    def show(self):
        self.frame_manager.clear()
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("Bathroom")
        canvas = Canvas(self.frame, width=self.frame_manager.game_manager.width, height=self.frame_manager.game_manager.height)
        canvas.pack()

        img = ImageTk.PhotoImage(Image.open('assets/bathroom.jpg').resize((self.frame_manager.game_manager.width, self.frame_manager.game_manager.height), Image.ANTIALIAS))
        canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = canvas.create_image(0, 0, anchor=NW, image=img)
        navbar(self, self.frame)

# Frame sub class
class menu():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame

    def show(self):
        self.frame_manager.clear()
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("Main Menu")

        container = Frame(self.frame, background = "white")
        container.place(anchor="center", relx=0.5, rely=0.7, height=500, width=800)

        image1 = Image.open("assets/logo.png")
        pixels_x, pixels_y = tuple([int(0.4 * x)  for x in image1.size])
        image1 = image1.resize((pixels_x, pixels_y))
        logo = ImageTk.PhotoImage(image1)
        label = Label(container, image=logo, background="white")
        label.image=logo 
        label.pack()

        Button(container, text="Play", command=lambda: self.frame_manager.bathroom.show()).pack()
        Button(container, text="Instructions", command=lambda: plantManager()).pack()
        Button(container, text="Exit", command=lambda: self.frame_manager.game_manager.root.destroy()).pack()

        copyright = Label(self.frame, text="Copyright EzSoil 2022", background="white")
        copyright.place(x = 20, y = self.frame_manager.game_manager.height-20, anchor = 'sw')

#
# Widgets
#

# Navbar widget
class navbar():
    def __init__(self, parent_frame, frame):
        self.parent_frame = parent_frame
        self.frame = frame
        
        container = Frame(self.frame, background = "white")
        container.place(anchor="n")

        Button(self.frame, text ="Bathroom", command = self.bathroom_button).place(anchor="e", x=self.parent_frame.frame_manager.game_manager.width/2, y=15)
        Button(self.frame, text ="Menu", command = self.menu_button).place(anchor="e", x=self.parent_frame.frame_manager.game_manager.width, y=15)

    def bathroom_button(self):
        self.parent_frame.frame_manager.bathroom.show()

    def menu_button(self):
        self.parent_frame.frame_manager.menu.show()

if __name__ == '__main__':
    GameManager()
