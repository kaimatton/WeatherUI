import json 
from urllib.request import urlopen 
import requests

import customtkinter
from tkinter import *


import pytz
from datetime import datetime
from time import strftime


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

# User Entry For Location
def return_key(event):
    entered_zip = enter_zip.get()
    zipcode = str(entered_zip)
    window.focus_set()

# API OPEN WEATHER APP 
    response = urlopen("https://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "&appid=310f40723630e5becce6757a5dacd2c6&units=imperial") 
    string = response.read().decode('utf-8')
    info = json.loads(string)
    print(info)

    name = str(info['name'])
    temp = round(float(info['main']['temp']))

# API DATE AND TIME 
    url = "https://timezone.abstractapi.com/v1/current_time"
    locations = name 
    querystring = {"location": locations,"api_key":"27da52e5747d4f85a92c79956984d475"}
    response2 = requests.request("GET", url, params=querystring)

    string2 = response2.content.decode('utf-8') 
    info2 = json.loads(string2)                 
    timezone = str(info2['timezone_location'])          
    print(timezone)

# Displays real time
    def update_time():
        time_zone = pytz.timezone(timezone)
        current_time = datetime.now(time_zone).strftime('%H:%M %p')
        timelabel = customtkinter.CTkLabel(window,
                                       padx= 4,
                                       pady= 4,
                                       height= 40,
                                       width= 400,
                                       text= (f'The Current Time Is {current_time}')
                                       )
        timelabel.after(1000, update_time)
        timelabel.place(relx=0.30,rely=0.3)
    update_time()
        
# Checks if given city is real
    if info == json.loads(string):
        check = True
    outcast = (f"The Current Weather In {name} is {temp}° Fahrenheit")
    if check is True:
        label = customtkinter.CTkLabel(window,
                                       text= outcast,
                                       padx= 2,
                                       pady= 2,
                                       height= 40,
                                       width= 400,                                       
                                       )
        label.place(relx=0.30,rely=0.35)

#Main Window 
window = customtkinter.CTk()
window.geometry('1005x650')
window.title("Weather App")

#Images
PhotoBg = PhotoImage(file = '/Users/matton/Downloads/background 2.png')

#Labels
bg = Label(window, image=PhotoBg,)
bg.pack()

#Entry 
enter_zip = customtkinter.CTkEntry(window,                              
                                 placeholder_text= 'Enter Zip Code',
                                 width= 500,
                                 height=50,
                                 justify='center',
                                 corner_radius=5,
                                 border_width=1,
                                 border_color='grey',
                                 fg_color='black',
                                 bg_color='grey'
                                 )
enter_zip.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
enter_zip.bind('<Return>' , return_key)

#buttons 

window.mainloop()