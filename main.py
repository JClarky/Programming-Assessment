from tkinter import *

#
# Managers
#

# The game manager (runtime environment for the game)
class GameManager():
    def __init__(self):
        self.run = True
        self.root = Tk()
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
# Subclasses
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
        self.frame_manager.game_manager.root.title("menu")
        navbar(self, self.frame)
        navbar(self, self.frame)
        navbar(self, self.frame)


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
