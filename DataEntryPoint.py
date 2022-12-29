import subprocess
import json
import tkinter as tk
from tkinter.ttk import *
from tkinter import simpledialog
import customtkinter


#Default values
method = [2,2]
starting_point=[0,0]
runs = [6,6]
probability1 = [
            "0.5", "0.45", "0.4", "0.35", "0.3", "0.3*", "0.3", "0.3135", "0.3135", "0.3135",
            "0.3*",
        ]
probability2 = ["0.5", "0.45","0.99h", "0.4016T","0.987h", "0.3546T", "0.986h","0.30425T","0.979h", "0.3064", "0.979h", "0.3064T", "0.979h","0.3046T", "0.972h","0.3086T","0.972h", "0.3086T",
            "0.93h","0.3226"]
moneytree1 = [
            0.0045, 0.00563, 0.00698, 0.00853, 0.01028, 0.0318, 0.03746, 0.04371, 0.05517, 0.06337,
            0.07952,
        ]
moneytree2 = [0.0045, 0.00563, 0.0, 0.00698, 0.0, 0.00853, 0.0, 0.01028, 0.0, 0.0318, 0.0, 0.03746,0.0,  0.04371,0.0, 0.05517,0.0, 0.06337,0.0,
            0.07952]
falsecap = [5,5]
trials = 1000


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("1650x700")
app.title("Bob")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)
# app.withdraw()
# the input dialog
# USER_INP = simpledialog.askstring(title="Test",
#                                   prompt="What's your Name?:")

# # check it out
# print("Hello", USER_INP)

# def infodump(info, methodology):
#     #methodology is going to be the type of data entry we are considering
#     # we want to generalise data collection and allocation to different variables
#     if methodology == 1:
#         return (method := int(info))
#     elif methodology == 2:
#     else: return None




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Rusty Simulator.py ")
        self.geometry(f"{1650}x{800}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0,7),weight=1)
        self.grid_columnconfigure((1,2,3,4,5,6), weight=7)
        # self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1,2,5,6), weight=1)
        self.grid_rowconfigure((3,4), weight=4)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=20, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, columnspan = 1,rowspan=7, sticky="nsew")
        # self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Advanced Trial Simulator", font=("CF Spaceship", 45))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text = "Simulate" ,command=self.simulate,height=200, width = 400,hover_color="black", font=("Microsoft Yi Baiti", 60), corner_radius=20) # Microsoft Yi Baiti,OCR A Extended, Prestige Elite Std
        self.sidebar_button_1.grid(row=4, column=0, rowspan = 3, padx=20, pady=100)

        self.sidebar_trialentry = customtkinter.CTkEntry(self.sidebar_frame,placeholder_text = "     No of Trials" ,font=("OCR A Extended", 25), corner_radius=5, width=350, height= 100) # Microsoft Yi Baiti,OCR A Extended, Prestige Elite Std
        self.sidebar_trialentry.grid(row=1, column=0, rowspan = 2, padx=0, pady=100)        
        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        #Appearance mode 
        # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="center", font=("Microsoft Yi Baiti", 20))
        # self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(0, 0))
        # self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
        #                                                                command=self.change_appearance_mode_event,font=("Microsoft Yi Baiti", 16))
        # self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # # self.scaling_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #Simulation 1

        self.sim1 = customtkinter.CTkLabel(self, text="Simulation 1", font=("OCR A Extended", 25))
        self.sim1.grid(row=0, column=2, pady=(20,0))
        
        self.sim2 = customtkinter.CTkLabel(self, text="Simulation 2", font=("OCR A Extended", 25))
        self.sim2.grid(row=0, column=5, pady=(20,0))

        self.entry = customtkinter.CTkEntry(self, placeholder_text= "Method", font=("Microsoft Yi Baiti", 16), fg_color=("gray78", "gray28"),justify = "center")  #text inside typing spot
        self.entry.grid(row=1, column=2, columnspan=1, padx=(40, 20), pady=(20, 20), sticky="nsew") 
        # self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.button1)
        # self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Number of runs ", font=("Microsoft Yi Baiti", 16), justify = "center")  #text inside typing spot
        self.entry2.grid(row=2, column=2, columnspan=1, padx=(40, 20), pady=(20, 20), sticky="nsew") 

        self.entry3 = customtkinter.CTkEntry(self, placeholder_text="Probability Structure", font=("Microsoft Yi Baiti", 16),justify = "center")
        self.entry3.grid(row=3, column=1, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")         

        self.entry4 = customtkinter.CTkEntry(self, placeholder_text="Monetary Scheme", font=("Microsoft Yi Baiti", 16),justify = "center") 
        self.entry4.grid(row=4, column=1, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")        

        self.entry5 = customtkinter.CTkEntry(self, placeholder_text="Starting point", font=("Microsoft Yi Baiti", 16),justify = "center") 
        self.entry5.grid(row=5, column=2, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")                

        self.entry6 = customtkinter.CTkEntry(self, placeholder_text="Falsecap parameter", font=("Microsoft Yi Baiti", 16),justify = "center")
        self.entry6.grid(row=6, column=2, columnspan=1, padx=(40, 20), pady=(20, 20), sticky="nsew")                





    #simulation 2
        self.entry21 = customtkinter.CTkEntry(self, placeholder_text="Method", font=("Microsoft Yi Baiti", 16),justify = "center")
        self.entry21.grid(row=1, column=5, columnspan=1, padx=(0,20), pady=(20, 20), sticky="nsew")  
        # self.main_button_2= customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.button2)
        # self.main_button_2.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")        

        self.entry22 = customtkinter.CTkEntry(self, placeholder_text="Number of runs ", font=("Microsoft Yi Baiti", 16),justify = "center")  
        self.entry22.grid(row=2, column=5, columnspan=1, padx=(0,20), pady=(20, 20), sticky="nsew") 


        self.entry23 = customtkinter.CTkEntry(self, placeholder_text="Probability Structure",font=("Microsoft Yi Baiti", 16),justify = "center")  
        self.entry23.grid(row=3, column=4, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")   

        self.entry24 = customtkinter.CTkEntry(self, placeholder_text="Monetary Scheme",font=("Microsoft Yi Baiti", 16),justify = "center")  
        self.entry24.grid(row=4, column=4, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")      

        self.entry25 = customtkinter.CTkEntry(self, placeholder_text="Starting point",font=("Microsoft Yi Baiti", 16),justify = "center")  
        self.entry25.grid(row=5, column=5, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")     

        self.entry26 = customtkinter.CTkEntry(self, placeholder_text="Falsecap parameter",font=("Microsoft Yi Baiti", 16),justify = "center")  
        self.entry26.grid(row=6, column=5, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")                 


        
        

        #Close 


        #Another side bar on right
        # self.sidebar_frame = customtkinter.CTkFrame(self, width=50, corner_radius=0)
        # self.sidebar_frame.grid(row=0, column=7, columnspan = 2,rowspan=5, sticky="nsew")        
        # close_button = Button(title_bar, text='X', command=root.destroy,bg="#2e2e2e",padx=2,pady=2,activebackground='red',bd=0,font="bold",fg='white',highlightthickness=0)        

        # # create textbox
        # self.textbox = customtkinter.CTkTextbox(self, width=100)
        # self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # # create tabview
        # self.tabview = customtkinter.CTkTabview(self, width=250)
        # self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.tabview.add("CTkTabview")
        # self.tabview.add("Tab 2")
        # self.tabview.add("Tab 3")
        # self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
        #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
        #                                             values=["Value 1", "Value 2", "Value Long....."])
        # self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        # self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                    command=self.open_input_dialog_event)
        # self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

    def button1(self):
        print(f"Sir, you have entered {self.entry.get()} into the dialog box, haven't you?")

    def button2(self):
        print(f"Sir, you have entered {self.entry2.get()} into the dialog box, haven't you?")       

    def simulate(self):
        global method 
        global runs 
        global probability1
        global probability2
        global moneytree1
        global moneytree2
        global falsecap
        global trials
        global starting_point
        try:method = [max(int(self.entry.get()),0),max(int(self.entry21.get()),0)]
        except:pass
        print(f"Method vector is now {method[0]} by {method[1]}")
        #falsecap
        try:falsecap = [max(int(self.entry6.get()),0),max(int(self.entry26.get()),0)]
        except:pass        
        print(f"falsecap vector is {falsecap[0]} by {falsecap[1]}")
        try:starting_point = [max(int(self.entry5.get()),0),max(int(self.entry25.get()),0)]
        except:pass        
        print(f"Starting point for each of the simulations is {starting_point[0]} by {starting_point[1]}")        
        try:runs = [max(int(self.entry2.get()),0),max(int(self.entry22.get()),0)]
        except:pass
        print(f"runs vector is now {runs[0]} by {runs[1]}")
        try:
            #Strings can be overwritten here with ""s if user does not type anything inside. Let us maintain the integrity of the default prob values
            if len(self.entry3.get())>0  and len(self.entry4.get())>0 :
                probability1 = [x.replace(" ","") for x in self.entry3.get().split(",")]
                moneytree1 = [float(x.replace(" ","")) for x in self.entry4.get().split(",")]
            if len(self.entry23.get())>0 and len(self.entry24.get())>0:
                probability2 = [x.replace(" ","") for x in self.entry23.get().split(",")]
                moneytree2 = [float(x.replace(" ","")) for x in self.entry24.get().split(",")]
        except:pass 
        print(f"Prob vector is now {probability1} by {probability2}")
        print(f"Money vector 1 is now {moneytree1} by {moneytree2}")        
        #edit trials
        try:trials = int(self.sidebar_trialentry.get())
        except:pass
        print(f"Number of trials set to {trials}")
        outputjson = {"simulation1":{
            "method":method[0],"runs":runs[0], "starting_point":starting_point[0],"probability":probability1,"moneytree":moneytree1, "falsecap":falsecap[0]
        },
        "simulation2":{
            "method":method[1],"runs":runs[1],"starting_point":starting_point[1], "probability":probability2,"moneytree":moneytree2, "falsecap":falsecap[1]
        },
        "trials":trials
        }
        with open("E:/RustCalc/output.json", "w") as outfile:
            json.dump(outputjson, outfile)       
        # app.destroy()
        subprocess.Popen("cargo run | py plot.py", shell=True) 
        # p_status = p.wait()
        # os.system("cargo run | py plot.py")
        # return None

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    # def change_appearance_mode_event(self, new_appearance_mode: str):
    #     customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()