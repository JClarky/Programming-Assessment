import tkinter

# The game manager (runtime environment for the game)
class GameManager():
    def __init__(self):
        self.run = True
        self.root = tkinter.Tk()
        self.root.title("EzSoil Game")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        windowManager(self)
        self.main_loop()
        
    def main_loop(self):
        self.root.mainloop()

# Window sub class
class menu():
    def __init__(self, window_manager):
        window_manager.game_manager.root.configure(background='black')

# Window manager
class windowManager():
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.menu = menu(self)
        
if __name__ == '__main__':
    GameManager()
