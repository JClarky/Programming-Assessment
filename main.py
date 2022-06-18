from tkinter import *
from xmlrpc.client import FastParser
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

            hours = int(str(self.time)[:colon_index])

            if hours > 23:
                hours = hours % 24
            
            time_formatted = str(self.time)
            time_formatted = str(hours)+":"+time_formatted[colon_index:]

            self.time_formatted = int(str(hours)+str(self.time)[colon_index:])
            
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
        for plant in self.plants:
            plant.update()

#
# Manager subclasses
#

class plant():
    def __init__(self, environment, plant_manager):
        plants = [{"name": "plant1", "image": "Plant-image.webp", "moisture_rate": 0.2, "moisture_low":40, "moisture_high":90, "sunlight_hours":5, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":90}, 
            {"name": "plant2", "image": "plant.png", "moisture_rate": 0.2, "moisture_low":40, "moisture_high":90, "sunlight_hours":5, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":90}, 
            {"name": "plant3", "image": "plant.png", "moisture_rate": 0.2, "moisture_low":40, "moisture_high":90, "sunlight_hours":5, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":90}]

        self.environment = environment
        self.plant_manager = plant_manager
        self.plant_manager.plants.append(self)

        self.info = random.choice(plants)   
        self.name = self.info["name"]
        self.environment.plants.append(self)
        self.soil_moisture = random.randint(0, 30)

        self.spawn_time = self.environment.frame_manager.game_manager.time
        self.moisture_rate = self.info["moisture_rate"]
        self.sunlight_last_update = 600
        self.out_of_range = 0
        self.info_displayed = False        

        self.moisture_warning = None
        self.sunlight_warning = None
        self.humidity_warning = None
        self.temperature_warning = None

    def draw(self):
        img = ImageTk.PhotoImage(Image.open('assets/'+self.info["image"]).resize((100, 100), Image.Resampling.LANCZOS))
        created = self.environment.canvas.create_image(200, 325, image=img, anchor=NW)
        self.environment.canvas.tag_bind(created, '<ButtonPress-1>', self.clicked) 
        created.tkraise()            
        
    def alert_show(self, location=None):
        try:
            if self.environment.frame_manager.active_frame == self.environment and self.info_displayed == False:
                img = ImageTk.PhotoImage(Image.open('assets/!.png').resize((25, 25), Image.Resampling.LANCZOS))
                self.alert_canvas = Canvas(self.environment.frame_manager.game_manager.frame, width=25, height=25, bg="red", bd=0, highlightthickness=0, relief='ridge')
                self.alert_canvas.background = img 
                self.alert_canvas.create_image(0, 0, anchor=NW, image=img)
                self.alert_canvas.place(anchor="e", x=280, y=350) 
            else:
                self.alert_hide()
        except Exception as e:
            print(e)

    def alert_hide(self):
        try:
            self.alert_canvas.destroy()
        except:
            pass

    def clicked(self, event):
        self.info_displayed = True
        self.canvas_plant_info = Canvas(self.environment.frame_manager.game_manager.frame, width=290, height=155, bg="#262626", relief="ridge", bd=0, highlightthickness=0)
        self.canvas_plant_info.place(anchor="e", x=400, y=320)        
        self.canvas_plant_info.create_rectangle(0,30,145,80, fill="white")
        self.canvas_plant_info.create_rectangle(145,30,290,80, fill="white")
        self.canvas_plant_info.create_rectangle(0,80,145,130, fill="white")
        self.canvas_plant_info.create_rectangle(145,80,290,130, fill="white")
        self.canvas_plant_info.create_text(5, 0, anchor=NW, text=self.info["name"], fill="white")
        self.soil_moisture_text = self.canvas_plant_info.create_text(5, 30, font='Helvetica 8 bold', anchor=NW, text="Soil Moisture "+ str(round(self.soil_moisture))+"%")
        self.sunlight_text = self.canvas_plant_info.create_text(150, 30, font='Helvetica 8 bold', anchor=NW, text=self.environment.sunlight_intensity + " sunlight for " + str(self.environment.sunlight_hours)+" hrs")
        self.humidity_text = self.canvas_plant_info.create_text(5, 80, font='Helvetica 8 bold', anchor=NW, text="Humidity " + str(self.environment.humidity)+"%")
        self.temperature_text = self.canvas_plant_info.create_text(150, 80, font='Helvetica 8 bold', anchor=NW, text="Temperature " + str(self.environment.temperature)+"°C")
        button(self.canvas_plant_info, text="X", command=self.close, padx=6).place(x=265, y=0)

        self.canvas_plant_info.create_text(5, 45, anchor=NW, text="Recommended\n"+str(self.info["moisture_low"])+"-"+str(self.info["moisture_high"])+"%")
        self.canvas_plant_info.create_text(150, 45, anchor=NW, text="Recommended\n" + self.info["sunlight_intensity"] + " for " + str(self.info["sunlight_hours"])+" hrs")
        self.canvas_plant_info.create_text(5, 95, anchor=NW, text="Recommended\n" + str(self.info["humidity_low"])+"-"+str(self.info["humidity_high"])+"%")
        self.canvas_plant_info.create_text(150, 95, anchor=NW, text="Recommended\n"+ str(self.info["temperature_low"])+"-"+str(self.info["temperature_high"])+"°C")

        button(self.canvas_plant_info, text="Move", command=self.move, padx=2).place(x=0, y=130)
        button(self.canvas_plant_info, text="Water", command=self.water, padx=2).place(x=45, y=130)

    def create_info_warning(self, x, y):
        img = ImageTk.PhotoImage(Image.open('assets/!.png').resize((25, 25), Image.Resampling.LANCZOS))
        temp = Canvas(self.canvas_plant_info, width=25, height=25, bg="red", bd=0, highlightthickness=0, relief='ridge')
        temp.background = img 
        temp.create_image(0, 0, anchor=NW, image=img)
        temp.place(anchor="e", x=x, y=y) 
        return(temp)

    def destroy_info_warning(self, name):
        if name == "moisture" and self.moisture_warning != None:            
            self.moisture_warning.destroy()        
            self.moisture_warning = None         
        elif name == "sunlight" and self.sunlight_warning != None:
            self.sunlight_warning.destroy()
            self.sunlight_warning = None
        elif name == "temperature" and self.temperature_warning != None:
            self.temperature_warning.destroy()
            self.temperature_warning = None
        elif name == "humidity" and self.humidity_warning != None:
            self.humidity_warning.destroy()
            self.humidity_warning = None
        
    def show_info_warning(self, name):
        if self.info_displayed:
            if name == "moisture" and self.moisture_warning == None:
                self.moisture_warning = self.create_info_warning(145,67)
            elif name == "sunlight" and self.sunlight_warning == None:
                self.sunlight_warning = self.create_info_warning(290,67)
            elif name == "temperature" and self.temperature_warning == None:
                self.temperature_warning = self.create_info_warning(290,116)
            elif name == "humidity" and self.humidity_warning == None:
                self.humidity_warning = self.create_info_warning(145,116)
        else:
            self.destroy_info_warning("moisture")
            self.destroy_info_warning("sunlight")
            self.destroy_info_warning("temperature")
            self.destroy_info_warning("humidity")

    def water(self):
        print("water")
        self.soil_moisture = 75

    def move(self):
        print("move")

    def die(self):
        print("plant deadd")

    def close(self):
        self.canvas_plant_info.destroy()
        self.info_displayed = False

    def update(self):        

        if self.soil_moisture > 0:
            self.soil_moisture = self.soil_moisture - self.moisture_rate

        alert = False
        
        if self.soil_moisture < self.info["moisture_low"] or self.soil_moisture > self.info["moisture_high"]:
            self.out_of_range += 1
            self.show_info_warning("moisture")        
            alert = True
        else:
            self.destroy_info_warning("moisture")
            alert = False

        if self.environment.temperature < self.info["temperature_low"] or self.environment.temperature > self.info["temperature_high"]:            
            self.out_of_range += 1
            self.show_info_warning("temperature")   
            alert = True
        else:
            self.destroy_info_warning("temperature")
            alert = False

        if self.environment.humidity < self.info["humidity_low"] or self.environment.humidity > self.info["humidity_high"]:            
            self.out_of_range += 1
            self.show_info_warning("humidity")   
            alert = True
        else:
            self.destroy_info_warning("humidity")
            alert = False

        if self.environment.sunlight_intensity != self.info["sunlight_intensity"]:
            self.out_of_range += 1
            self.show_info_warning("sunlight")   
            alert = True
        else:
            self.destroy_info_warning("sunlight")
            alert = False


        if alert == False:
            self.alert_hide()
            self.out_of_range = 0   
        else:
            self.alert_show()

        try:
            self.canvas_plant_info.itemconfig(self.soil_moisture_text, text="Soil Moisture "+ str(round(self.soil_moisture))+"%")
            self.canvas_plant_info.itemconfig(self.sunlight_text, text=self.environment.sunlight_intensity + " sunlight for " + str(self.environment.sunlight_hours)+" hrs")
            self.canvas_plant_info.itemconfig(self.humidity_text, text="Humidity " + str(self.environment.humidity)+"%")
            self.canvas_plant_info.itemconfig(self.temperature_text, text="Temperature " + str(self.environment.temperature)+"°C")
        except:
            pass

        # if any value are outside range for more then 24 hours, die            
        if self.out_of_range > 1440:
            self.die()

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
        self.sunlight_hours = 7

    def show(self):
        self.frame_manager.clear()
        self.frame_manager.active_frame = self
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("Bathroom")
        self.canvas = Canvas(self.frame, width=self.frame_manager.game_manager.width, height=self.frame_manager.game_manager.height)
        self.canvas.pack()       

        img = ImageTk.PhotoImage(Image.open('assets/bathroom.jpg').resize((self.frame_manager.game_manager.width, self.frame_manager.game_manager.height), Image.Resampling.LANCZOS))
        self.canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = self.canvas.create_image(0, 0, anchor=NW, image=img)
        navbar(self, self.frame)

        for plant in self.plants:
            plant.draw()

class button(Button):
    def __init__(self, parent, padx=None, pady=None, *args, **kwargs):
        self.parent = parent        

        if padx == None:
            padx = 20
        if pady == None:
            pady = 2

        Button.__init__(self, parent, borderwidth=1, relief='solid', bg="#6bb846", padx=padx, pady=pady,  *args, **kwargs)

        self.pack(padx=15, pady=5)
        
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

        button(container, text="Play", command=lambda: self.frame_manager.game_manager.start())
        button(container, text="Instructions", command=lambda: plantManager())
        button(container, text="Exit", command=lambda: self.frame_manager.game_manager.destroy())

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

        button(self.frame, text ="Bathroom", command = self.bathroom_button).place(anchor="e", x=self.parent_frame.frame_manager.game_manager.width/2, y=15)
        button(self.frame, text ="Exit to Menu", command = self.menu_button).place(anchor="e", x=self.parent_frame.frame_manager.game_manager.width, y=15)

    def bathroom_button(self):
        self.parent_frame.frame_manager.bathroom.show()
        self.parent_frame.frame_manager.game_manager.clock()

    def menu_button(self):
        self.parent_frame.frame_manager.menu.show()

if __name__ == '__main__':
    GameManager()


print("end")