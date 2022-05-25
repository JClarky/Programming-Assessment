import tkinter

class GameManager():
    def __init__(self):
        self.run = True
        self.root = tkinter.Tk()
        self.root.title("EzSoil Game")
        self.root.geometry("1000x600")
        #root.resizable(False, False)
        self.main_loop()
    def main_loop(self):
        self.root.mainloop()

if __name__ == '__main__':
    GameManager()
