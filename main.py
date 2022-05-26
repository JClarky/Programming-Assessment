import tkinter

# The game manager (runtime environment for the game)
class GameManager():
    def __init__(self):
        self.run = True
        self.root = tkinter.Tk()
        self.root.title("EzSoil Game")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(side="top", expand=True, fill="both")
        windowManager(self)
        self.main_loop()
        
    def main_loop(self):
        self.root.mainloop()

# Window sub class
class bathroom():
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.root = window_manager.game_manager.frame

    def show(self):
        self.window_manager.clear()
        self.root.configure(background='white')
        tkinter.Button(self.root, text ="Hello", command = self.button).pack()

    def button(self):
        self.window_manager.menu.show()

# Window sub class
class menu():
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.root = window_manager.game_manager.frame

    def show(self):
        self.window_manager.clear()
        self.root.configure(background='white')
        tkinter.Button(self.root, text ="Bathroom", command = self.button).pack()

    def button(self):
        self.window_manager.bathroom.show()

# Window manager
class windowManager():
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.menu = menu(self)
        self.bathroom = bathroom(self)

        self.menu.show()

    def clear(self):
        for widgets in self.game_manager.frame.winfo_children():
            widgets.destroy()
        
if __name__ == '__main__':
    GameManager()
