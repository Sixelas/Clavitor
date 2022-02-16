import tkinter, pynput
from tkinter import messagebox
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import sys

# /////// CONFIG ///////

root:object = tkinter.Tk()
app_title:str = "Clavitor"
app_size:tuple = (400, 500)
listener_stop:bool = False
backgroundColor = 'white'
foregroundColor = 'black'
ChartOptionList = ["camembert","histo"]
trigChart = "camembert"
stock_list = [[],[]] 

# Determine if it's clavitor.py or clavitor.exe
# Absolute path of the folder which contains this file
if getattr(sys, 'frozen', False):
    selfFolderPath = os.path.dirname(sys.executable) 
elif __file__:
    selfFolderPath = os.path.dirname(__file__)

# ///// END CONFIG /////


# Create graph files
def plot_Creator(listPlot, type):
    
    if(type == "camembert") :
        #explode = (0, 0.1, 0, 0)  #To elevate one part of the pie
        fig, ax = plt.subplots()
        ax.pie(listPlot[1], labels=listPlot[0],shadow=False, startangle=90)
        ax.axis('equal')

    elif(type == "histo") :
        fig = plt.figure()
        width = 0.5
        plt.bar(listPlot[0], listPlot[1], width )
    
    plt.savefig(selfFolderPath+'/chart.png')
    plt.close()

# Save content of stock_list[][] in data.txt
def saveFile() :
    fichier = open(selfFolderPath+"/data.txt", "a")
    for e in stock_list[0] :
        s = e + " "+ str(stock_list[1][stock_list[0].index(e)]) + "\n"
        fichier.write(s)
    fichier.close()

# Load content of data.txt in stock_list[][]
def loadFile() :
    if os.path.exists(selfFolderPath + '/data.txt'):
        fichier = open(selfFolderPath+"/data.txt", "r")
        for line in fichier :
            if "#" in line:
                continue
            data = line.split()
            stock_list[0].append(data[0])
            stock_list[1].append(int(data[1]))
        fichier.close()
        os.remove(selfFolderPath + '/data.txt')

# Add a key|mouse entry value to stock_list[][]
def add_to_stock(elem) :
    if elem in stock_list[0] :
        stock_list[1][stock_list[0].index(elem)] +=1
    else :
        stock_list[0].append(elem)
        stock_list[1].append(1)

# Return a list containing the 5 biggest (sorted).
def Top5():
    listTmp =[["","","","",""],[0,0,0,0,0]]
    for e in stock_list[0] :
        val  = stock_list[1][stock_list[0].index(e)]
        if(val > listTmp[1][0]) :
            listTmp[0].insert(0,e)
            listTmp[1].insert(0,val)
            listTmp[0].pop()
            listTmp[1].pop()
        elif(val > listTmp[1][1]) :
            listTmp[0].insert(1,e)
            listTmp[1].insert(1,val)
            listTmp[0].pop()
            listTmp[1].pop()
        elif(val > listTmp[1][2]) :
            listTmp[0].insert(2,e)
            listTmp[1].insert(2,val)
            listTmp[0].pop()
            listTmp[1].pop()
        elif(val > listTmp[1][3]) :
            listTmp[0].insert(3,e)
            listTmp[1].insert(3,val)
            listTmp[0].pop()
            listTmp[1].pop()
        elif(val > listTmp[1][4]) :
            listTmp[0].insert(4,e)
            listTmp[1].insert(4,val)
            listTmp[0].pop()
            listTmp[1].pop()
    plot_Creator(listTmp, trigChart)
    return listTmp

# Description in name 
def totalTouches() :
    ret = 0
    for e in stock_list[1] :
        ret = ret +e
    return ret


# Easy way to use pynput mouse + keyboard at the same time in Tkinter
# Inspired by https://stackoverflow.com/questions/61755350/using-pynput-for-key-events-instead-of-tkinter

# // Logics Keyboard
class Keyboard:

    # On button pressed
    @staticmethod
    def Pressed(key) -> bool:
        # If listener_stop is True then stop listening
        if listener_stop: print("Keyboard Events are stoped!"); return False
        # Else show pressed key
        else: 
            add_to_stock("{}".format(key))

    # Listen keybboard buttons
    @staticmethod
    def Listener() -> None:
        k_listen = pynput.keyboard.Listener(on_press=Keyboard.Pressed)
        k_listen.start()


# // Logics Mouse
class Mouse:
    
    # On click
    @staticmethod
    def Click(x, y, button, pressed) -> None:
        if pressed : 
            add_to_stock("{}".format(button))

    # Listen keybboard buttons
    @staticmethod
    def Listener() -> None:
        m_listen = pynput.mouse.Listener(on_click=Mouse.Click)
        m_listen.start()


# // GUI
class MainApp:

    def __init__(self, master):
        self.master = master

        self.X = (self.master.winfo_screenwidth() - app_size[0]) // 2
        self.Y = (self.master.winfo_screenheight() - app_size[1]) // 2
        self.master.wm_title(app_title)
        self.master.wm_geometry(f"{app_size[0]}x{app_size[1]}+{self.X}+{self.Y}")
        self.master.configure(bg=backgroundColor)
        self.master.option_add('*Background', backgroundColor)

        self.Screen(self.master)
        self.InputEvents()
        self.updateImage()

    # Define Screen Informations
    def Screen(self, root) -> None:

        # Global counter
        self.valMax = tkinter.Label(root)
        self.valMax.pack(side=tkinter.TOP)

        #Old option
        '''
        self.val1 = tkinter.Label(root, pady=10)
        self.val1.pack()
        self.val2 = tkinter.Label(root, pady=10)
        self.val2.pack()
        self.val3 = tkinter.Label(root, pady=10)
        self.val3.pack()
        self.val4 = tkinter.Label(root, pady=10)
        self.val4.pack()
        self.val5 = tkinter.Label(root, pady=10)
        self.val5.pack()
        '''

        # OptionMenu for choosing the statistic to be displayed
        self.chartName = ChartOptionList[0]
        options = tkinter.StringVar(root)
        options.set(self.chartName)
        self.optm = tkinter.OptionMenu(root, options, *ChartOptionList, command=self.userInput).pack(side=tkinter.TOP)
        
        #TODO : Button for generate a specific complete graph.
        '''
        self.Button_Generate=tkinter.Button(root, pady=10)
        self.Button_Generate["bg"] = "#AED4FD"
        ft = tkFont.Font(family='Times',size=10)
        self.Button_Generate["font"] = ft
        self.Button_Generate["fg"] = "#000000"
        self.Button_Generate["justify"] = "center"
        self.Button_Generate["text"] = "Générer Key"
        self.Button_Generate["relief"] = "raised"
        self.Button_Generate["state"] = "normal"
        #self.Button_Generate.place(x=100,y=80,width=75,height=30)
        self.Button_Generate["command"] = self.Button_Generate_command
        self.Button_Generate.pack()
        '''

        self.canvas = tkinter.Canvas(root)
        self.canvas.pack(fill="both", expand=1)

    # Input events
    def InputEvents(self) -> None:
        Keyboard.Listener()
        Mouse.Listener()
    
    #TODO Button for generate a specific complete graph.
    def Button_Generate_command(self):
        plot_Creator(stock_list, trigChart)
    
    
    # Call updateImageOnce and setup a new update in TTL seconds
    def updateImage(self):

        #plot_Creator()
        Top5()
        self.qrImage = Image.open(selfFolderPath + '/chart.png')
        textMax = "Nombre total de touches : " + str(totalTouches())
        self.valMax.config(text=textMax)

        #Old option
        '''
        if(len(stock_list[0]) > 4) :
            top5 = Top5()
            Textval1 = '1 : '+ top5[0][0] +' : '+ str(top5[1][0])
            Textval2 = '2 : '+ top5[0][1] +' : '+ str(top5[1][1])
            Textval3 = '3 : '+ top5[0][2] +' : '+ str(top5[1][2])
            Textval4 = '4 : '+ top5[0][3] +' : '+ str(top5[1][3])
            Textval5 = '5 : '+ top5[0][4] +' : '+ str(top5[1][4])

            self.val1.config(text=Textval1)
            self.val2.config(text=Textval2)
            self.val3.config(text=Textval3)
            self.val4.config(text=Textval4)
            self.val5.config(text=Textval5)
        '''
        # Set a new timer for the next refresh time (in ms)
        self.canvas.after(int(1000), self.updateImage)
        self.displayImage()

    def displayImage(self):

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        size = min(width, height)

        # Adapt the size of the image with the size of the viewport
        self.qrImageResized = self.qrImage.resize((size, size))
        self.qrImageResized = ImageTk.PhotoImage(self.qrImageResized)
        self.canvas.create_image(width / 2,
                                 height / 2,
                                 anchor='center',
                                 image=self.qrImageResized)

    # Event handler when the OptionMenu selected option is changed
    def userInput(self, selectedElement=None):
        global trigChart
        if selectedElement:
            self.chartName = selectedElement
            trigChart = selectedElement

        self.canvas.after_cancel(self.updateImage)
        self.updateImage()

    # Safe Quit
    def SafeQuit(self, master:object = root) -> None:
        global listener_stop

        if messagebox.askokcancel(f"{app_title} Quit", f"Quitter {app_title}?"):
            if listener_stop == False:
                listener_stop = True
            master.destroy()
            saveFile()

# Start
if __name__ == "__main__":
    loadFile()
    app:object = MainApp(root)
    root.protocol("WM_DELETE_WINDOW", app.SafeQuit)
    root.mainloop()