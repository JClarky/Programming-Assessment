from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import time, random, sys

#
# Managers
#

# The game manager (runtime environment for the game)
class GameManager():
    def __init__(self):
        self.run = True
        self.root = Tk()
        self.time = 700
        self.height = 600
        self.width = 1000
        self.root.title("EzSoil Game")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        self.frame = Frame(self.root)
        self.frame.pack(side="top", expand=True, fill="both")
        self.frame_manager = frameManager(self)      
        self.plant_manager = plantManager(self)
        self.plant_manager.spawn(self.frame_manager.bathroom)
        #self.root.bind('<Motion>', self.motion)
        self.main_loop()

    def motion(self,event):
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))

    def destroy(self):
        self.run = False
        self.root.destroy()
        sys.exit()     

    def start(self):
        Thread(target=self.clock).start()
        self.frame_manager.bathroom.show()

    def main_loop(self):
        self.root.mainloop()

    def clock(self):   
        while self.run:     
            minutes = int(str(self.time)[len(str(self.time))-2:])
            if minutes == 59:
                self.time += 41
            else:
                self.time += 1 

            colon_index = 1
            if self.time > 999: 
                colon_index = 2

            time_formatted = str(self.time)
            time_formatted = time_formatted[:colon_index]+":"+time_formatted[colon_index:]
            
            try:
                try:
                    self.frame_manager.active_frame.canvas.delete(self.update_text)
                except:
                    pass
                self.update_text = self.frame_manager.active_frame.canvas.create_text(10, 10, anchor=NW, text=time_formatted)
            except:
                pass


            self.plant_manager.update()
            
            if 'normal' != self.root.state():
                self.destroy()
                
            time.sleep(0.005)
       
# Frame manager
class frameManager():
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.menu = menu(self)
        self.bathroom = bathroom(self)
        self.menu.show()
        self.active_frame = None;

    def clear(self):
        for widgets in self.game_manager.frame.winfo_children():
            widgets.destroy()
            
class plantManager():
    def __init__(self, game_manager):
        self.game_manager = game_manager 
        self.enviros = [self.game_manager.frame_manager.bathroom]
        self.plants = []

    def spawn(self, environment=None):
        if environment is None:
            environment = random.choice(self.enviros)
        plant(environment, self)
    
    def update(self):
        for enviro in self.enviros:
            enviro.update()

        for plant in self.plants:
            plant.update()

#
# Manager subclasses
#

class plant():
    def __init__(self, environment, plant_manager):
        plants = [{"name": "plant1", "image": "Plant-image.webp", "moisture_rate": 0.2, "moisture_low":40, "sunlight_hours":5, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":90}, 
            {"name": "plant2", "image": "Plant-image.webp", "moisture_rate": 0.2, "moisture_low":40, "sunlight_hours":5, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":90}, 
            {"name": "plant3", "image": "Plant-image.webp", "moisture_rate": 0.2, "moisture_low":40, "sunlight_hours":5, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":90}]

        self.environment = environment
        self.plant_manager = plant_manager
        self.plant_manager.plants.append(self)

        print("choosing type of plant (from database) and spawning at requested environment")
        self.info = random.choice(plants)   
        self.name = self.info["name"]
        self.environment.plants.append(self)
        self.soil_moisture = random.randint(0, 30)
        self.sunlight_hours = 0
        self.sunlight_log = []
        self.spawn_time = self.environment.frame_manager.game_manager.time
        self.moisture_rate = self.info["moisture_rate"]
        self.sunlight_last_update = 600

    def draw(self):
        self.canvas = Canvas(self.environment.frame_manager.game_manager.frame, width=100, height=100)

        img = ImageTk.PhotoImage(Image.open('assets/'+self.info["image"]).resize((100, 100), Image.LANCZOS))
        self.canvas.background = img 
        bg = self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.place(anchor="e", x=280, y=400)
        self.canvas.tag_bind(bg, '<ButtonPress-1>', self.clicked)       

        img = ImageTk.PhotoImage(Image.open('assets/!.png').resize((25, 25), Image.LANCZOS))
        self.alert_canvas = Canvas(self.environment.frame_manager.game_manager.frame, width=25, height=25, bg="red", bd=0, highlightthickness=0, relief='ridge')
        self.alert_canvas.background = img 
        self.alert_canvas.create_image(0, 0, anchor=NW, image=img)
        self.alert_canvas.place(anchor="e", x=280, y=350) 
        
    def alert_show(self):
        try:
            if self.environment.frame_manager.active_frame == self.environment:
                self.alert_canvas.itemconfig(1, state='normal')
            else:
                self.alert_hide()
        except:
            pass

    def alert_hide(self):
        try:
            self.alert_canvas.itemconfig(1, state='hidden')
        except:
            pass

    def clicked(self, event):
        self.canvas_plant_info = Canvas(self.environment.frame_manager.game_manager.frame, width=200, height=150)
        self.canvas_plant_info.place(anchor="e", x=305, y=350)        
        self.canvas_plant_info.create_rectangle(0,50,100,100, fill="white")
        self.canvas_plant_info.create_rectangle(100,50,200,100, fill="white")
        self.canvas_plant_info.create_rectangle(0,100,100,150, fill="white")
        self.canvas_plant_info.create_rectangle(100,100,200,150, fill="white")
        self.canvas_plant_info.create_text(5, 0, anchor=NW, text=self.info["name"])
        self.canvas_plant_info.create_text(5, 50, anchor=NW, text="Soil Moisture")
        self.canvas_plant_info.create_text(105, 50, anchor=NW, text="Sunlight")
        self.canvas_plant_info.create_text(5, 100, anchor=NW, text="Humidity")
        self.canvas_plant_info.create_text(105, 100, anchor=NW, text="Temperature")
        Button(self.canvas_plant_info, text="X", command=self.close).place(x=185, y=0)

        self.canvas_plant_info.create_text(5, 75, anchor=NW, text=str(round(self.soil_moisture))+"%")
        self.canvas_plant_info.create_text(105, 65, anchor=NW, text=str(self.get_sunlight())+" hours \n" + str(self.environment.sunlight_intensity) + " sunlight")
        self.canvas_plant_info.create_text(5, 125, anchor=NW, text=str(self.environment.humidity)+"%")
        self.canvas_plant_info.create_text(105, 125, anchor=NW, text=str(self.environment.temperature)+"°C")

    def close(self):
        self.canvas_plant_info.destroy()

    def get_sunlight(self):
        if len(self.sunlight_log) < 24:
            last_24_hours = self.sunlight_log
        else:
            last_24_hours = self.sunlight_log[-24:]

        hours = 0

        for point in last_24_hours:
            if point["intensity"] != "none":
                hours += 1
        
        return(hours)

    def update(self):        
        self.soil_moisture = self.soil_moisture - self.moisture_rate
        if self.environment.frame_manager.game_manager.time - self.sunlight_last_update > 60:
            if self.environment.sunlight_log == 1:
                self.sunlight_hours += 1
            self.sunlight_log.append({"time":self.environment.frame_manager.game_manager.time, "intensity":self.environment.sunlight_intensity})
            self.sunlight_last_update = self.environment.frame_manager.game_manager.time

        if self.soil_moisture < self.info["moisture_low"]:
            self.alert_show()
        elif self.environment.temperature < self.info["temperature_low"]:
            self.alert_show()
        elif self.environment.temperature > self.info["temperature_high"]:
            self.alert_show()
        elif self.environment.humidity < self.info["humidity_low"]:
            self.alert_show()
        elif self.environment.humidity > self.info["humidity_high"]:
            self.alert_show()
        elif self.environment.sunlight_intensity != self.info["sunlight_intensity"]:
            self.alert_show()
        else: 
            self.alert_hide()

    

# Frame sub class
class bathroom():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame
        self.plants = []
        self.canvas = None
        self.temperature = random.randint(15,25)
        self.humidity = random.randint(70,95)
        self.sunlight_intensity = "indirect"
        self.sunlight_log = None
        self.sunlight_last_log = 600

    def show(self):
        self.frame_manager.clear()
        self.frame_manager.active_frame = self
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("Bathroom")
        self.canvas = Canvas(self.frame, width=self.frame_manager.game_manager.width, height=self.frame_manager.game_manager.height)
        self.canvas.pack()       

        img = ImageTk.PhotoImage(Image.open('assets/bathroom.jpg').resize((self.frame_manager.game_manager.width, self.frame_manager.game_manager.height), Image.LANCZOS))
        self.canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = self.canvas.create_image(0, 0, anchor=NW, image=img)
        navbar(self, self.frame)

        for plant in self.plants:
            plant.draw()

    def update(self):
        if self.frame_manager.game_manager.time - self.sunlight_last_log > 60:
            if 700 < self.frame_manager.game_manager.time < 1300: # Morning sun
                self.sunlight_log = 1
            self.sunlight_last_log = self.frame_manager.game_manager.time


# Frame sub class
class menu():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame

    def show(self):
        self.frame_manager.clear()
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("Main Menu")
        self.frame_manager.active_frame = self

        container = Frame(self.frame, background = "white")
        container.place(anchor="center", relx=0.5, rely=0.7, height=500, width=800)

        image1 = Image.open("assets/logo.png")
        pixels_x, pixels_y = tuple([int(0.4 * x)  for x in image1.size])
        image1 = image1.resize((pixels_x, pixels_y))
        logo = ImageTk.PhotoImage(image1)
        label = Label(container, image=logo, background="white")
        label.image=logo 
        label.pack()

        Button(container, text="Play", command=lambda: self.frame_manager.game_manager.start()).pack()
        Button(container, text="Instructions", command=lambda: plantManager()).pack()
        Button(container, text="Exit", command=lambda: self.frame_manager.game_manager.destroy()).pack()

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
        self.parent_frame.frame_manager.game_manager.clock()

    def menu_button(self):
        self.parent_frame.frame_manager.menu.show()

if __name__ == '__main__':
    GameManager()


print("end")