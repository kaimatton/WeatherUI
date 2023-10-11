import json 
from urllib.request import urlopen 
import requests

import customtkinter
from tkinter import *
import tkintermapview


import pytz
from datetime import datetime
from time import strftime


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

my_label = None
timelabel = None
# User Entry For Location
def return_key(event):
    entered_zip = enter_zip.get()
    zipcode = str(entered_zip)
    window.focus_set()
    if my_label is not None:
        my_label.destroy()
        my_frame.destroy()
        addPoint.destroy()
    if timelabel is not None:
        timelabel.destroy()


# API OPEN WEATHER APP 
    response = urlopen("https://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "&appid=310f40723630e5becce6757a5dacd2c6&units=imperial") 
    string = response.read().decode('utf-8')
    info = json.loads(string)

    name = str(info['name'])
    temp = round(float(info['main']['temp']))
    lat = float(info['coord']['lat'])
    lon = float(info['coord']['lon'])

# API DATE AND TIME cle
    url = "https://timezone.abstractapi.com/v1/current_time"
    locations = name 
    querystring = {"location": locations,"api_key":"27da52e5747d4f85a92c79956984d475"}
    response2 = requests.request("GET", url, params=querystring)

    string2 = response2.content.decode('utf-8') 
    info2 = json.loads(string2)                 
    timezone = str(info2['timezone_location'])  

    # Displays real time
    def update_time():
        global current_time
        global timelabel
        time_zone = pytz.timezone(timezone)
        current_time = datetime.now(time_zone).strftime('%I:%M %p')
        timelabel = customtkinter.CTkLabel(window,
                                       padx= 4,
                                       pady= 4,
                                       height= 40,
                                       width= 400,
                                       text= (f'The Local Time Is {current_time}'),
                                       
                                       )
        timelabel.after(1000, update_time)
        timelabel.place(relx=0.30,rely=0.27)    
    update_time()   

# Checks if given city is real
    def validate():
        if info == json.loads(string):
            check = True
        outcast = (f"The Current Weather In {name} is {temp}° Fahrenheit")
        if check is True:
            bg.configure(image=PhotoNight) 
            label = customtkinter.CTkLabel(window,
                                       text= outcast,
                                       padx= 2,
                                       pady= 2,
                                       height= 40,
                                       width= 400,   
                                    
                                       )
            label.place(relx=0.30,rely=0.32)
        
            def check_box():
                global my_label
                global my_frame
                global addPoint
                if check_var.get() == "on":
                    
                    def add_checkmark():
                        map_widget.set_address(name,marker= True)

                    my_frame = customtkinter.CTkFrame(window,
                                                      border_width=2,
                                                      border_color='black',
                                                      corner_radius=0,
                                                      width=700,
                                                      height=380)
                    my_frame.place(relx=0.16,rely=0.44)

                    addPoint = customtkinter.CTkButton(window,
                                                       text='Mark Location',
                                                       width=30,
                                                       height=20,
                                                       command= add_checkmark
                                                       )
                    addPoint.place(relx=.17, rely=0.50)

                    my_label = LabelFrame(window,height=450,
                                          width=350,
                                          borderwidth=0)
                    my_label.place(relx= 0.28, rely= 0.45)

                    map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=350, corner_radius= 0, )
                    map_widget.set_position(lat,lon)
                    map_widget.set_zoom(13)
                    map_widget.pack()

                else:
                    if my_label:
                        my_label.destroy()
                        my_frame.destroy()
                        addPoint.destroy()

            check_var = customtkinter.StringVar(value='off')
            checkBox = customtkinter.CTkCheckBox(window, 
                                                command= check_box,
                                                variable= check_var,
                                                text= 'Open Map',
                                                onvalue='on',
                                                offvalue='off',
                                                checkmark_color='white',
                                                hover_color='grey',
                                                corner_radius=20,
                                                border_color='grey',
                                                border_width=1,                                
                                                )
            checkBox.place(relx=0.45, rely=0.40)
       
    validate()

#Main Window 
window = customtkinter.CTk()
window.geometry('1005x650')
window.title("Weather App")

#Images
PhotoBg = PhotoImage(file = '/Users/matton/Downloads/background 2.png')
PhotoNight = PhotoImage(file = '/Users/matton/Downloads/weather 2.png')

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
                                 border_width=2,
                                 border_color='black',
                                 fg_color='grey10'
                                 )
enter_zip.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
enter_zip.bind('<Return>' , return_key)

window.mainloop()