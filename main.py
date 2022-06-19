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
        self.timescale = None
        #self.root.bind('<Motion>', self.motion)


        self.main_loop()

    def motion(self,event):
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))

    def destroy(self):
        self.run = False
        self.root.destroy()
        sys.exit()     

    def stop(self):
        self.run = False
        
    def start(self):
        self.run = True
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
                self.update_text = self.frame_manager.active_frame.canvas.create_text(10, 10, anchor=NW, text=time_formatted, font="Poppins 8")
    
            except:
                pass

            self.plant_manager.update()

            if self.frame_manager.active_frame and self.frame_manager.active_frame != self.frame_manager.menu:
                self.frame_manager.active_frame.nav.update()
            
            if 'normal' != self.root.state():
                self.destroy()

            time.sleep(1/self.timescale)
       
# Frame manager
class frameManager():
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.menu = menu(self)

        self.bathroom = environment("Bathroom", self, [{"x":250, "y":375, "size":100}, {"x":733, "y":490, "size":200}, {"x":167, "y":545, "size":100}],
        5,"low",random.randint(85,89),random.randint(15,25))

        self.garden = environment("Garden", self, [{"x":835, "y":427, "size":100}, {"x":481, "y":352, "size":80}, {"x":322, "y":480, "size":105}, {"x":158, "y":420, "size":105}],
        9,"direct",random.randint(70,80),random.randint(21,30))

        self.window = environment("Window", self, [{"x":733, "y":504, "size":150}, {"x":539, "y":500, "size":130}, {"x":322, "y":460, "size":130}, {"x":158, "y":430, "size":130}],
        7,"indirect",random.randint(60,80),random.randint(10,25))

        self.shelf = environment("Shelf", self, [{"x":265, "y":300, "size":150}, {"x":415, "y":300, "size":150}, {"x":565, "y":300, "size":150}, {"x":715, "y":300, "size":150}],
        4,"low",random.randint(60,70),random.randint(10,20))

        self.menu.show()
        self.active_frame = None;

    def clear(self):
        for widgets in self.game_manager.frame.winfo_children():
            widgets.destroy()

    def show_instructions(self):
        instructions(self).show()
            
class plantManager():
    def __init__(self, game_manager):
        self.plants_info = [{"name": "Wavy Green", "image": "plant.png", "moisture_rate": 0.1, "moisture_low":50, "moisture_high":80, "sunlight_hours":4, "sunlight_intensity":"low", "temperature_low":15, "temperature_high":25, "humidity_low":75, "humidity_high":90},  # bathroom
            {"name": "Pointy Tropics", "image": "plant2.png", "moisture_rate": 0.3, "moisture_low":60, "moisture_high":90, "sunlight_hours":8, "sunlight_intensity":"direct", "temperature_low":15, "temperature_high":30, "humidity_low":60, "humidity_high":80}, #garden
            {"name": "Red Flowers", "image": "plant3.png", "moisture_rate": 0.2, "moisture_low":60, "moisture_high":80, "sunlight_hours":7, "sunlight_intensity":"indirect", "temperature_low":10, "temperature_high":25, "humidity_low":60, "humidity_high":80}, #window sill
            {"name": "Angry Goose", "image": "plant4.png", "moisture_rate": 0.2, "moisture_low":30, "moisture_high":90, "sunlight_hours":4, "sunlight_intensity":"low", "temperature_low":10, "temperature_high":20, "humidity_low":60, "humidity_high":70}] # shelf

        self.plants_spawned = [0,0,0,0]

        self.game_manager = game_manager 
        self.enviros = [self.game_manager.frame_manager.bathroom, self.game_manager.frame_manager.garden, self.game_manager.frame_manager.shelf, self.game_manager.frame_manager.window]
        self.plants = []
        self.spawner = False
        self.last_spawned = 0

    def spawn(self, environment=None):
        if environment is None:
            environment = random.choice(self.enviros)
            if environment.max_spawned <= len(environment.plants):
                return

        if len(environment.spawn_locations) != 0:
            random_index = random.randint(0, 3)
            if self.plants_spawned[random_index] == 3:
                return
            info = self.plants_info[random_index]
            self.plants_spawned[random_index] += 1
            
            random_index = random.randint(0, len(environment.spawn_locations)-1)
            location = environment.spawn_locations[random_index]
            x = location["x"]
            y = location["y"]
            size = location["size"]

            environment.spawn_locations.pop(random_index)

            temp = plant(environment, self, info, x, y, size)

            self.last_spawned = 0

            if environment == self.game_manager.frame_manager.active_frame:
                temp.draw()
    
    def update(self):
        self.last_spawned += 1
        if self.plants[0].alert == False and len(self.plants) == 1 and self.last_spawned > 10:
            self.spawner = True        
        
        for plant in self.plants:
            plant.update()

        if self.spawner and self.last_spawned > 60:
            self.spawn()

#
# Manager subclasses
#

class plant():
    def __init__(self, environment, plant_manager, info, x, y, size=100):
        self.environment = environment
        self.plant_manager = plant_manager
        self.plant_manager.plants.append(self)

        self.info = info  
        self.name = self.info["name"]

        self.environment.plants[id(self)] = self
        self.soil_moisture = random.randint(0, 30)

        self.spawn_time = self.environment.frame_manager.game_manager.time
        self.moisture_rate = self.info["moisture_rate"]
        self.sunlight_last_update = 600
        self.info_displayed = False        

        self.moisture_warning = None
        self.sunlight_warning = None
        self.humidity_warning = None
        self.temperature_warning = None

        self.alert = False

        self.alert_canvas = None

        self.size = size

        self.x = x
        self.y = y

    def draw(self):        
        self.img = ImageTk.PhotoImage(Image.open('assets/'+self.info["image"]).resize((self.size, self.size), Image.Resampling.LANCZOS))
        self.created = self.environment.canvas.create_image(self.x, self.y, image=self.img)
        self.environment.canvas.tag_bind(self.created, '<ButtonPress-1>', self.clicked)           
        
    def alert_show(self):
        if self.environment.frame_manager.active_frame == self.environment and self.info_displayed == False:
            if self.alert_canvas == None:
                img = ImageTk.PhotoImage(Image.open('assets/!.png').resize((25, 25), Image.Resampling.LANCZOS))
                self.alert_canvas = Canvas(self.environment.frame_manager.game_manager.frame, width=25, height=25, bg="red", bd=0, highlightthickness=0, relief='ridge')
                self.alert_canvas.background = img 
                self.alert_canvas.create_image(0, 0, anchor=NW, image=img)
                self.alert_canvas.place(anchor="e", x=self.x+40, y=self.y-10) 
        else:
            self.alert_hide()

    def alert_hide(self):
        if self.alert_canvas != None:
            self.alert_canvas.destroy()
            self.alert_canvas = None

    def clicked(self, event):
        if self.info_displayed == False:
            self.info_displayed = True
            self.canvas_plant_info = Canvas(self.environment.frame_manager.game_manager.frame, width=290, height=155, bg="#262626", relief="ridge", bd=0, highlightthickness=0)
            self.canvas_plant_info.place(anchor="e", x=self.x+150, y=self.y-80)        
            self.canvas_plant_info.create_rectangle(0,30,145,80, fill="white")
            self.canvas_plant_info.create_rectangle(145,30,290,80, fill="white")
            self.canvas_plant_info.create_rectangle(0,80,145,130, fill="white")
            self.canvas_plant_info.create_rectangle(145,80,290,130, fill="white")
            self.canvas_plant_info.create_text(5, 0, anchor=NW, text=self.info["name"], fill="white", font="Poppins 8")
            self.soil_moisture_text = self.canvas_plant_info.create_text(5, 30, font='Poppins 8 bold', anchor=NW, text="Soil Moisture "+ str(round(self.soil_moisture))+"%")
            self.sunlight_text = self.canvas_plant_info.create_text(150, 30, font='Poppins 8 bold', anchor=NW, text=self.environment.sunlight_intensity.capitalize() + " sunlight for " + str(self.environment.sunlight_hours)+" hrs")
            self.humidity_text = self.canvas_plant_info.create_text(5, 80, font='Poppins 8 bold', anchor=NW, text="Humidity " + str(self.environment.humidity)+"%")
            self.temperature_text = self.canvas_plant_info.create_text(150, 80, font='Poppins 8 bold', anchor=NW, text="Temperature " + str(self.environment.temperature)+"°C")
            button(self.canvas_plant_info, text="X", command=self.close, padx=6).place(x=264, y=0)

            self.canvas_plant_info.create_text(5, 45, anchor=NW, text="Requires:\n"+str(self.info["moisture_low"])+"-"+str(self.info["moisture_high"])+"%", font="Poppins 8")
            self.canvas_plant_info.create_text(150, 45, anchor=NW, text="Requires:\n" + self.info["sunlight_intensity"].capitalize() + " for " + str(self.info["sunlight_hours"])+" hrs", font="Poppins 8")
            self.canvas_plant_info.create_text(5, 95, anchor=NW, text="Requires:\n" + str(self.info["humidity_low"])+"-"+str(self.info["humidity_high"])+"%", font="Poppins 8")
            self.canvas_plant_info.create_text(150, 95, anchor=NW, text="Requires:\n"+ str(self.info["temperature_low"])+"-"+str(self.info["temperature_high"])+"°C", font="Poppins 8")

            button(self.canvas_plant_info, text="Move", command=self.move_menu_open, padx=2).place(x=0, y=130)
            button(self.canvas_plant_info, text="Water", command=self.water, padx=2).place(x=45, y=130)

    def create_info_warning(self, x, y):
        try:
            img = ImageTk.PhotoImage(Image.open('assets/!.png').resize((25, 25), Image.Resampling.LANCZOS))
            temp = Canvas(self.canvas_plant_info, width=25, height=25, bg="red", bd=0, highlightthickness=0, relief='ridge')
            temp.background = img 
            temp.create_image(0, 0, anchor=NW, image=img)
            temp.place(anchor="e", x=x, y=y) 
            return(temp)
        except:
            pass

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
        self.soil_moisture = 75

    def move_menu_open(self):
        self.close()
        self.info_displayed = True
        self.canvas_move_menu = Canvas(self.environment.frame_manager.game_manager.frame, width=210, height=60, bg="#262626", relief="ridge", bd=0, highlightthickness=0)
        self.canvas_move_menu.place(anchor="e", x=self.x+110, y=self.y-32)        
        self.canvas_move_menu.create_text(5, 0, anchor=NW, text="Move to:", fill="white", font="Poppins 8")
        button(self.canvas_move_menu, text="X", command=self.move_menu_close, padx=4, pady=0).place(x=188, y=0)
        button(self.canvas_move_menu, text="Bathroom", command=self.move_bathroom, padx=2).place(x=0, y=30)
        button(self.canvas_move_menu, text="Garden", command=self.move_garden, padx=2).place(x=65, y=30)
        button(self.canvas_move_menu, text="Shelf", command=self.move_shelf, padx=2).place(x=115, y=30)
        button(self.canvas_move_menu, text="Window", command=self.move_window, padx=2).place(x=154, y=30)

    def move_menu_close(self):
        self.canvas_move_menu.destroy()
        self.info_displayed = False

    def move_bathroom(self):        
        self.move(self.plant_manager.game_manager.frame_manager.bathroom)

    def move_garden(self):
        self.move_menu_close()
        self.move(self.plant_manager.game_manager.frame_manager.garden)

    def move_shelf(self):
        self.move_menu_close()
        self.move(self.plant_manager.game_manager.frame_manager.shelf)

    def move_window(self):
        self.move_menu_close()
        self.move(self.plant_manager.game_manager.frame_manager.window)

    def move(self, environment):
        if environment == self.environment:
            return
        if len(environment.spawn_locations) == 1:
            random_index = 0
        elif len(environment.spawn_locations) > 1:
            random_index = random.randint(0, len(environment.spawn_locations)-1)
        else:
            return
        location = environment.spawn_locations[random_index]
        environment.spawn_locations.pop(random_index)

        self.environment.spawn_locations.append({"x":self.x, "y":self.y, "size":self.size})

        x = location["x"]
        y = location["y"]
        size = location["size"]
        self.move_menu_close()

        self.environment.plants.pop(id(self))
        self.close()
        self.environment.canvas.delete(self.created)
        self.environment = environment

        self.environment.plants[id(self)] = self
        self.x = x
        self.y = y
        self.size = size
        self.spawn_time = self.environment.frame_manager.game_manager.time
        

    def close(self):
        self.canvas_plant_info.destroy()
        self.info_displayed = False

    def update(self):        

        if self.soil_moisture > 0:
            self.soil_moisture = self.soil_moisture - self.moisture_rate

        self.alert = False
        
        if self.soil_moisture < self.info["moisture_low"] or self.soil_moisture > self.info["moisture_high"]:
            self.show_info_warning("moisture")        
            self.alert = True
        else:
            self.destroy_info_warning("moisture")

        if self.environment.temperature < self.info["temperature_low"] or self.environment.temperature > self.info["temperature_high"]:            
            self.show_info_warning("temperature")   
            self.alert = True
        else:
            self.destroy_info_warning("temperature")

        if self.environment.humidity < self.info["humidity_low"] or self.environment.humidity > self.info["humidity_high"]:            
            self.show_info_warning("humidity")   
            self.alert = True
        else:
            self.destroy_info_warning("humidity")

        if self.environment.sunlight_intensity != self.info["sunlight_intensity"]:
            self.show_info_warning("sunlight")   
            self.alert = True
        else:
            self.destroy_info_warning("sunlight")

        if self.alert == False:
            self.alert_hide() 
        else:
            self.alert_show()

        try:
            self.canvas_plant_info.itemconfig(self.soil_moisture_text, text="Soil Moisture "+ str(round(self.soil_moisture))+"%")
            self.canvas_plant_info.itemconfig(self.sunlight_text, text=self.environment.sunlight_intensity.capitalize() + " sunlight for " + str(self.environment.sunlight_hours)+" hrs")
            self.canvas_plant_info.itemconfig(self.humidity_text, text="Humidity " + str(self.environment.humidity)+"%")
            self.canvas_plant_info.itemconfig(self.temperature_text, text="Temperature " + str(self.environment.temperature)+"°C")
        except:
            pass


# Frame sub class
class environment():
    def __init__(self, name, frame_manager, spawn_locations, sunlights_hours, sunlight_intensity, humidity, temperature):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame
        self.plants = {}
        self.canvas = None
        self.temperature = temperature
        self.humidity = humidity
        self.sunlight_intensity = sunlight_intensity
        self.sunlight_hours = sunlights_hours
        self.spawn_locations = spawn_locations
        self.name = name
        self.max_spawned = len(spawn_locations)-1

    def show(self):
        self.frame_manager.clear()
        self.frame_manager.active_frame = self
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title(self.name)
        self.canvas = Canvas(self.frame, width=self.frame_manager.game_manager.width, height=self.frame_manager.game_manager.height)
        self.canvas.pack()       

        img = ImageTk.PhotoImage(Image.open('assets/'+self.name+'.jpg').resize((self.frame_manager.game_manager.width, self.frame_manager.game_manager.height), Image.Resampling.LANCZOS))
        self.canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.nav = navbar(self, self.frame)

        for id, plant in self.plants.items():
            plant.draw()

class button(Button):
    def __init__(self, parent, padx=None, pady=None, *args, **kwargs):
        self.parent = parent        

        if padx == None:
            padx = 20
        if pady == None:
            pady = -1

        Button.__init__(self, parent, borderwidth=1, relief='solid', bg="#6bb846", padx=padx, pady=pady, font="Poppins 8",  *args, **kwargs)

        self.pack(padx=15, pady=5)
        
# Frame sub class
class menu():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame
        self.age = None
        self.timescale = None

    def set_age(self):
        age = self.age_input.get()
        try:
            age = int(age)
            if 0 <= age < 13:
                self.message.set('You must be 13 or older to play')
                self.age_input.destroy()
                self.continue_button.config(text="Exit", command=self.frame_manager.game_manager.destroy)
            elif 13 <= age < 120:
                self.age = age
                self.show()
            else:
                raise ValueError
                
        except ValueError:
            self.message.set('Please enter a valid age')      

    def set_timescale(self):
        timescale = self.timescale_input.get()
        try:
            timescale = int(timescale)
            if 50 < timescale:
                self.message.set('Sorry, but the maximum timescale is 50, the minimum is 10. Try again.\n(10 = 10 minute per second, 15 = 15 minutes per second, no decimals, timescale between 10 and 50)')
            elif 9 < timescale:
                self.timescale = timescale
                self.frame_manager.game_manager.timescale = timescale
                self.show()
            else:
                raise ValueError
                
        except ValueError:
            self.message.set('Please enter a valid timescale\n(10 = 10 minute per second, 15 = 15 minutes per second, no decimals, timescale between 10 and 50)')    


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

        if self.age == None:
            self.message = StringVar()
            self.message.set('Before playing, enter your age:')
            Label(container, textvariable=self.message, font="Poppins 10", bg="white").pack()
            self.age_input = Entry(container, font="Poppins 10")
            self.age_input.pack()
            self.continue_button = button(container, text="Continue",command=self.set_age)
            self.continue_button.pack()
        elif self.timescale == None:
            self.message = StringVar()
            self.message.set('Please enter your timescale\n(10 = 10 minute per second, 15 = 15 minutes per second, no decimals, timescale between 10 and 50):')
            Label(container, textvariable=self.message, font="Poppins 10", bg="white").pack()
            self.timescale_input = Entry(container, font="Poppins 10")
            self.timescale_input.pack()
            self.continue_button = button(container, text="Continue",command=self.set_timescale)
            self.continue_button.pack()
        else:
            button(container, text="Play", command=self.frame_manager.game_manager.start)
            button(container, text="Instructions", command=self.frame_manager.show_instructions)
            button(container, text="Exit", command=self.frame_manager.game_manager.destroy)

        copyright = Label(self.frame, text="Copyright EzSoil 2022", background="white", font="Poppins 8")
        copyright.place(x = 20, y = self.frame_manager.game_manager.height-20, anchor = 'sw')

class instructions():
    def __init__(self, frame_manager):
        self.frame_manager = frame_manager
        self.frame = frame_manager.game_manager.frame

    def show(self):
        self.frame_manager.clear()
        self.frame.configure(background='white')
        self.frame_manager.game_manager.root.title("Instructions")
        self.frame_manager.active_frame = self

        container = Frame(self.frame, background = "white")
        container.place(anchor="center", relx=0.5, rely=0.6, height=500, width=800)

        image1 = Image.open("assets/logo.png")
        pixels_x, pixels_y = tuple([int(0.4 * x)  for x in image1.size])
        image1 = image1.resize((pixels_x, pixels_y))
        logo = ImageTk.PhotoImage(image1)
        label = Label(container, image=logo, background="white")
        label.image=logo 
        label.pack()

        t = Text(container, background="white", height=14, width=52, wrap=WORD, font="Poppins 8")
        t.pack()

        t.insert(END, "Welcome to the EzSoil game!\nThe purpose of this game is to show you how Sprout can help monitor plant health.\n\nWhen you play, click on plants to see their health status and requirements. From that menu you can water or move the plants to a better climate. \nOn the top of your screen you will see the different environments (click to go to different environment), including how many plants are at each locations, and how many need tending to. \n\n There is no time limit, and the plants will not die. Tend to the first plant that is spawned to continue.")
        t.config(state=DISABLED)

        button(container, text="Back", command=self.frame_manager.menu.show)

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

        self.offset = self.parent_frame.frame_manager.game_manager.width/2 - 100

        button(self.frame, text ="Bathroom", command = self.parent_frame.frame_manager.bathroom.show).place(anchor="e", x=self.offset, y=15)
        button(self.frame, text ="Garden", command = self.parent_frame.frame_manager.garden.show).place(anchor="e", x=self.offset+90, y=15)
        button(self.frame, text ="Shelf", command = self.parent_frame.frame_manager.shelf.show).place(anchor="e", x=self.offset+167, y=15)
        button(self.frame, text ="Window", command = self.parent_frame.frame_manager.window.show).place(anchor="e", x=self.offset+262, y=15)
        button(self.frame, text ="Exit to Menu", command = self.exit_button).place(anchor="e", x=self.parent_frame.frame_manager.game_manager.width, y=15)

    def exit_button(self):
        self.parent_frame.frame_manager.game_manager.stop()
        self.parent_frame.frame_manager.menu.show()

    def update(self):
        try:
            no_alerts = 0
            no_plants = len(self.parent_frame.frame_manager.bathroom.plants)
            for id, plant in self.parent_frame.frame_manager.bathroom.plants.items():
                if plant.alert:
                    no_alerts += 1
                
            Label(self.frame, text=str(no_alerts), background="red", padx=5, font="Poppins 8").place(anchor="e", x=self.offset, y=30) 
            Label(self.frame, text=str(no_plants), background="white", padx=5, font="Poppins 8").place(anchor="e", x=self.offset-83, y=30) 

            no_alerts = 0
            no_plants = len(self.parent_frame.frame_manager.garden.plants)
            for id, plant in self.parent_frame.frame_manager.garden.plants.items():
                if plant.alert:
                    no_alerts += 1
                
            Label(self.frame, text=str(no_alerts), background="red", padx=5, font="Poppins 8").place(anchor="e", x=self.offset+90, y=30) 
            Label(self.frame, text=str(no_plants), background="white", padx=5, font="Poppins 8").place(anchor="e", x=self.offset+23, y=30) 

            no_alerts = 0
            no_plants = len(self.parent_frame.frame_manager.shelf.plants)
            for id, plant in self.parent_frame.frame_manager.shelf.plants.items():
                if plant.alert:
                    no_alerts += 1
                
            Label(self.frame, text=str(no_alerts), background="red", padx=5, font="Poppins 8").place(anchor="e", x=self.offset+167, y=30) 
            Label(self.frame, text=str(no_plants), background="white", padx=5, font="Poppins 8").place(anchor="e", x=self.offset+114, y=30) 

            no_alerts = 0
            no_plants = len(self.parent_frame.frame_manager.window.plants)
            for id, plant in self.parent_frame.frame_manager.window.plants.items():
                if plant.alert:
                    no_alerts += 1
                
            Label(self.frame, text=str(no_alerts), background="red", padx=5, font="Poppins 8").place(anchor="e", x=self.offset+262, y=30) 
            Label(self.frame, text=str(no_plants), background="white", padx=5, font="Poppins 8").place(anchor="e", x=self.offset+191, y=30) 
        except:
            pass

if __name__ == '__main__':
    GameManager()
