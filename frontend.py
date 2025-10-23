import tkinter as tk 
from threading import Thread as thread
import serial  
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#front 
# looking side , the window

r = tk.Tk()
r.geometry('1200x700')
r.resizable(False,False)


#--------------------------gui part-----------------------

no_of_cols = 4

bg_colour = '#151515'
#sub frame settings for easy access
sub_frame_bg_colour = '#282828'
sub_frame_height = 200
sub_frame_width = 475
sub_frame_heading_settings = "Arial" , 20
heading_color = 'white'

#readings config
readings_colour = 'green'
readings_bg_colour = sub_frame_bg_colour
readings_font_settings = "Arial" , 90
#main frame
main_frame = tk.Frame(r, bg =bg_colour,padx=15,pady=35)
main_frame.pack(fill='both')

heading=tk.Label(main_frame,text='MONITOR',font=('Arial',50),bg=sub_frame_bg_colour,fg='white')
heading.pack(fill='x',pady=25)
#data frame
data_frame = tk.Frame(main_frame,bg=bg_colour,pady=10)
data_frame.pack(expand=True, fill='both')

#heading

#grid config in data frame/ parent frame
data_frame.rowconfigure(1,weight=1)
for i in range(2,4):
    data_frame.rowconfigure(i,weight=2,pad=25)

for i in range(4):
    data_frame.columnconfigure(i,weight=1,pad=25)

#sub frame config
#configures rows
def col_config(frame):
    for i in range(2):
        frame.rowconfigure(i,weight=1,pad=25)
padd=7
#------------------------skeleton 
temp_frame = tk.Frame(data_frame,bd=10,bg=sub_frame_bg_colour,height=sub_frame_height,width=sub_frame_width,padx=10,pady=10)
temp_frame.grid(row=0,column=1,padx=padd)
temp_frame.pack_propagate(False)
col_config(temp_frame)

humid_frame = tk.Frame(data_frame, bd=10 ,bg = sub_frame_bg_colour, height=sub_frame_height,width=sub_frame_width,padx=10,pady=10)
humid_frame.grid(row=0,column=0,padx=padd)
humid_frame.pack_propagate(False)
col_config(humid_frame)

moisture_frame = tk.Frame(data_frame,bd=10,bg=sub_frame_bg_colour,height=sub_frame_height,width=sub_frame_width,padx=10,pady=10)
moisture_frame.grid(row=0,column=2,padx=padd)
moisture_frame.pack_propagate(False)
col_config(moisture_frame)

pressure_frame = tk.Frame(data_frame,bd=10,bg=sub_frame_bg_colour,height=sub_frame_height,width=sub_frame_width,padx=10,pady=10)
pressure_frame.grid(row=0,column=3,padx=padd)
pressure_frame.pack_propagate(False)
col_config(pressure_frame)

#----------------adding content to the frames
temperature_heading = tk.Label(temp_frame, text="Temperature(C) -" , bg=sub_frame_bg_colour , font=sub_frame_heading_settings,fg=heading_color)
temperature_heading.grid(row=0,column=0)
temperature_reading = tk.Label(temp_frame,text='0' , font = readings_font_settings, fg='#F8A136' , bg=readings_bg_colour)
temperature_reading.grid(row=1,column=0)

humid_heading = tk.Label(humid_frame,text = "humidity(%) -" , font=sub_frame_heading_settings, bg=sub_frame_bg_colour, fg=heading_color)
humid_heading.grid(row=0,column=0)
humid_reading = tk.Label(humid_frame,text='0' , font = readings_font_settings, fg='#21D8D8' , bg=readings_bg_colour)
humid_reading.grid(row=1,column=0)

moisture_heading= tk.Label(moisture_frame, text = "Moisture in Soil(%) -" , font=sub_frame_heading_settings,bg=sub_frame_bg_colour,fg=heading_color)
moisture_heading.grid(row=0,column=0)
moisture_reading = tk.Label(moisture_frame,text='0' , font = readings_font_settings, fg='#F01010' , bg=readings_bg_colour)
moisture_reading.grid(row=1,column=0)

pressure_frame_heading= tk.Label(pressure_frame,text="Air Pressure(psi)", font=sub_frame_heading_settings, bg=sub_frame_bg_colour,fg=heading_color)
pressure_frame_heading.grid(row=0,column=0)
pressure_frame_reading= tk.Label(pressure_frame,text="0",font=readings_font_settings, fg=readings_colour, bg=readings_bg_colour)
pressure_frame_reading.grid(row=1,column=0)

#-----------------------graph-----------------------

#temp
def graph(frame,x_data,y_data,color):

    fig,ax = plt.subplots(figsize=(2,2))
    ax.set_xlabel("Time")
    ax.set_ylabel("temperature")
    ax.set_facecolor((0,0,0,0.8))
    fig.patch.set_facecolor((0,0,0,0.8))

    line = ax.plot(x_data,y_data,color=color,line_width=2)

    canvas = FigureCanvasTkAgg(fig,master=frame)
    canvas.get_tk_widget().grid(row=2,column=0)
    
    if len(x_data)>20:
        x_data

graph(temp_frame,0,0,'orange')
graph(humid_frame,0,0,'blue')
graph(moisture_frame,0,0,'red')
graph(pressure_frame,0,0,'green')



#--------------------------back part OR  recieveing readings-------


ser = serial.Serial('/dev/ttyACM1', 9600,  timeout=2)
def read_data():
    while True:

        data = ser.readline().decode('utf').strip()
        values = [x.strip() for x in data.split(',')]
        
    #if failed to recieve any reading arduino returns nan and that messup everything so to eliminate that 
        
    # when arduino doesn't respond on time python makes it a string with a space which is invalid to convert into interger 
        try:
            #r.after(1,updt_readings,nums)#giving a list
            updt_readings(values)
            print(values)
        except Exception as e:
            print(e)
#--------------------------data reading done-----------------------
def updt_readings(values):#gettings a list
    #1st /2nd readings comes as empty list to avoid out of range index error
    try:

        humidity,temperature,moisture = values[0],values[1],values[2]
    
        temperature_reading.configure(text=temperature)
        humid_reading.configure(text=humidity)
        moisture_reading.configure(text=moisture)
        print(humidity,temperature,moisture)
    except Exception as e:
        print(e)
        print(values)
    
"""

while True :
    data = read_data()
    if data:
        humidity,temperature,moisture = data[0],data[1],data[2]
        print(humidity,temperature,moisture)
"""
thread(target=read_data,daemon=True).start()
r.mainloop()
