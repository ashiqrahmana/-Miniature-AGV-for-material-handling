from tkinter import *
from matplotlib.figure import Figure
import random
from numpy import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import ipoprpitobs2 as pop

current_pose = [0,0,0]
prev_x,prev_y,prev_w1,prev_w2 = [0,0,0,0]

lmotor_max = 1500
rmotor_max = 0

lmotor_min = 750
rmotor_min = 750
end_point = [50,50]
rotate = 1


root = Tk()
root.title("HMI for AGV")

#root.geometry("640x480")


#Define title label
title_gui = Label(root, text="AGV HMI")
title_gui.grid(row=0,column=0,columnspan=5)


def submit(pick_position_x, pick_position_y, place_position_x, place_position_y, submit_input):

    #Disable Inputs
    submit_input.config(state="disabled")
    pick_position_x.config(state="disabled")
    pick_position_y.config(state="disabled")
    place_position_x.config(state="disabled")
    place_position_y.config(state="disabled")


#Input Validator
def validate(action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


#Input Section
def static_input():

    vcmd = (root.register(validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    Input_section = LabelFrame(root, text="Input Section", padx=50, pady=50)
    Input_section.grid(row=2,column=0,columnspan=5)

    pick_text = Label(Input_section, text="Pick Position Coordinates:")
    pick_text.grid(row=0,column=0,columnspan=4)
    pick_position_x_text = Label(Input_section, text="X: ")
    pick_position_x_text.grid(row=1,column=0)
    pick_position_x = Entry(Input_section, width="7", bd=4, justify=CENTER, font="Arial 18", validate = 'key', validatecommand = vcmd)
    pick_position_x.grid(row=1,column=1)
    pick_position_y_text = Label(Input_section, text="Y: ")
    pick_position_y_text.grid(row=1,column=2)
    pick_position_y = Entry(Input_section, width="7", bd=4, justify=CENTER, font="Arial 18", validate = 'key', validatecommand = vcmd)
    pick_position_y.grid(row=1,column=3)


    place_text = Label(Input_section, text="Place Position Coordinates:")
    place_text.grid(row=0,column=5,columnspan=4)
    place_position_x_text = Label(Input_section, text="X: ")
    place_position_x_text.grid(row=1,column=5)
    place_position_x = Entry(Input_section, width="7",  bd=4, justify=CENTER, font="Arial 18", validate = 'key', validatecommand = vcmd)
    place_position_x.grid(row=1,column=6)
    place_position_y_text = Label(Input_section, text="Y: ")
    place_position_y_text.grid(row=1,column=7)
    place_position_y = Entry(Input_section, width="7",  bd=4, justify=CENTER, font="Arial 18", validate = 'key', validatecommand = vcmd)
    place_position_y.grid(row=1,column=8)


    dummy_line = Label(Input_section, text="  ")
    dummy_line.grid(row=2,column=0)

        
    submit_input = Button(Input_section, text = "SUBMIT", command=lambda: submit(pick_position_x, pick_position_y, place_position_x, place_position_y, submit_input), width=8, bd=4)
    submit_input.grid(row=3,column=4)
    
    #Font Styling
    title_font = ("Courier New",26,"bold","roman")
    Input_section_font = ("Arial",14,"bold","roman")

    #Apply font Styling
    title_gui.configure(font = title_font)
    Input_section.configure(font = Input_section_font)
    pick_text.configure(font = Input_section_font)
    place_text.configure(font = Input_section_font)
    submit_input.configure(font = Input_section_font)
    pick_position_x_text.configure(font = Input_section_font)
    pick_position_y_text.configure(font = Input_section_font)
    place_position_x_text.configure(font = Input_section_font)
    place_position_y_text.configure(font = Input_section_font)

    return(pick_position_x, pick_position_y, place_position_x, place_position_y, submit_input)


#Output Section
def plot(pick_point, place_point, current_point, section, output_section):
    #the figure that will contain the plot
    fig = Figure(figsize = (3, 3), dpi = 100)

    if (section==1):
        start_point = [0.1,0]
        end_point = current_point
        x = linspace(0, end_point[0])
        #print(x)
        y = (end_point[1]-start_point[1])/(end_point[0]-start_point[0])*x
    elif (section==2): 
        start_point = pick_point
        end_point = current_point
        x = linspace(start_point[0],end_point[0])
        y = (end_point[1]-start_point[1])/(end_point[0]-start_point[0])*x + ((start_point[1]*end_point[0]-start_point[0]*end_point[1])/(end_point[0]-start_point[0]))

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(pick_point[0],pick_point[1],'ro')
    plot1.plot(place_point[0],place_point[1],'bo') 
    plot1.plot(x,y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = output_section)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=3, column=1, columnspan=5)


def static_output(pick_position_x, pick_position_y, place_position_x, place_position_y, current_pose, curve_section, submit_input):
    output_section = LabelFrame(root, text="Output Section", padx=50, pady=50)
    output_section.grid(row=4,column=0,columnspan=5)

    pick_rec_text = Label(output_section, text="Recieved Pick Position: ")
    pick_rec_text.grid(row=0,column=0,columnspan=2)

    dummy_line = Label(output_section, text="        ")
    dummy_line.grid(row=0,column=3)

    place_rec_text = Label(output_section, text="Recieved Place Position: ")
    place_rec_text.grid(row=0,column=4,columnspan=2)

    current_text = Label(output_section, text="Current Position: ")
    current_text.grid(row=1,column=0,columnspan=2)

    dummy_line = Label(output_section, text="        ")
    dummy_line.grid(row=1,column=3)

    current_orientation_text = Label(output_section, text="Current Orientation: ")
    current_orientation_text.grid(row=1,column=4,columnspan=2)

    dynamic_data(output_section, pick_position_x, pick_position_y, place_position_x, place_position_y, current_pose, curve_section, submit_input)
    
    #defining font style
    Output_section_font = ("Arial",14,"bold","roman")
    Output_section_sub_font = ("Arial",14,"roman")

    #Apply font style
    output_section.configure(font = Output_section_font)
    pick_rec_text.configure(font = Output_section_font)
    place_rec_text.configure(font = Output_section_font)
    current_text.configure(font = Output_section_font)
    current_orientation_text.configure(font = Output_section_font)


#Dynamic Data update function
def dynamic_data(output_section, pick_position_x, pick_position_y, place_position_x, place_position_y, current_pose, curve_section, submit_input):

    pick_pos = [0.,0.]
    place_pos = [0.,0.]
    global prev_w1,prev_w2
    
    if (str(submit_input['state'])=='disabled'):                
        pick_pos = [float(pick_position_x.get())*102, float(pick_position_y.get())*102]
        place_pos = [float(place_position_x.get())*102, float(place_position_y.get())*102]

        plot(pick_pos, place_pos, current_pose, curve_section, output_section)

        pick_rec = Label(output_section, text=("["+str(pick_pos[0])+","+str(pick_pos[1])+"]"))
        pick_rec.grid(row=0,column=2)

        place_rec = Label(output_section, text=("["+str(place_pos[0])+","+str(place_pos[1])+"]"))
        place_rec.grid(row=0,column=6)

        current_loc = Label(output_section, text=("["+str(current_pose[0])+","+str(current_pose[1])+"]"))
        current_loc.grid(row=1,column=2)
        
        current_ori = Label(output_section, text=("["+str(current_pose[2])+"]"))
        current_ori.grid(row=1,column=6)
        
        print(curve_section)
        if curve_section == 1:
            current_pose,prev_w1,prev_w2 = pop.main(ser,prev_x,prev_y,prev_w1,prev_w2,pick_pos)

        if curve_section == 2:
            current_pose,prev_w1,prev_w2 = pop.main(ser,prev_x,prev_y,prev_w1,prev_w2,place_pos)
        
        if abs(current_pose[0] - pick_pos[0]) < 5 and abs(current_pose[1] - pick_pos[1]) < 5:
            curve_section = 2

        if abs(current_pose[0] - place_pos[0]) < 5 and abs(current_pose[1] - place_pos[1]) < 5:
            pick_position_x, pick_position_y, place_position_x, place_position_y, submit_input = static_input()
            curve_section = 1
            static_output(pick_position_x, pick_position_y, place_position_x, place_position_y, current_pose, curve_section, submit_input)
    
      
            
    else:
        pick_rec = Label(output_section, text=("[0,0]"))
        pick_rec.grid(row=0,column=2)

        place_rec = Label(output_section, text=("[0,0]"))
        place_rec.grid(row=0,column=6)

        current_loc = Label(output_section, text=("[0,0]"))
        current_loc.grid(row=1,column=2)

        current_ori = Label(output_section, text=("[0]"))
        current_ori.grid(row=1,column=6)    
   
    root.after(500, lambda:dynamic_data(output_section, pick_position_x, pick_position_y, place_position_x, place_position_y, current_pose, curve_section, submit_input)) #run itself again after 100ms

    Output_section_sub_font = ("Arial",14,"roman")
    pick_rec.configure(font = Output_section_sub_font)
    place_rec.configure(font = Output_section_sub_font)
    current_loc.configure(font = Output_section_sub_font)
    current_ori.configure(font = Output_section_sub_font)

#Main part of program
pick_position_x, pick_position_y, place_position_x, place_position_y, submit_input = static_input()

#get current pos
current_pose = [0,0,0]


# Ashiq code reference example
ser = pop.__init__()         # you just got to call this once
 # you have to call this repeatedly 

curve_section = 1

static_output(pick_position_x, pick_position_y, place_position_x, place_position_y, current_pose, curve_section, submit_input)

root.mainloop()
