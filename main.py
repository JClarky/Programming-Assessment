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
        frameManager(self)
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

#
# Manager subclasses
#

# Frame sub class
class bathroom():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame

    def show(self):
        self.frame_manager.clear()
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("bathroom")
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

        image1 = Image.open("assets/logo.png")
        pixels_x, pixels_y = tuple([int(0.5 * x)  for x in image1.size])
        image1 = image1.resize((pixels_x, pixels_y))
        logo = ImageTk.PhotoImage(image1)
        label = Label(self.frame, image=logo, background="white")
        label.image=logo 
        label.pack()

        Button(self.frame, text="Play", command=lambda: self.frame_manager.bathroom.show()).pack()
        Button(self.frame, text="Instructions", command=lambda: print("show intructions")).pack()
        Button(self.frame, text="Exit", command=lambda: self.frame_manager.game_manager.root.destroy()).pack()

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
        Button(self.frame, text ="Bathroom", command = self.bathroom_button).pack()
        Button(self.frame, text ="Menu", command = self.menu_button).pack()

    def bathroom_button(self):
        self.parent_frame.frame_manager.bathroom.show()

    def menu_button(self):
        self.parent_frame.frame_manager.menu.show()

        
if __name__ == '__main__':
    GameManager()
