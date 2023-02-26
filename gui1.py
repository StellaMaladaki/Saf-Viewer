import customtkinter as ctk
import netCDF4 as nc
import numpy as np
import pandas as pd
from matplotlib.pyplot import * 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


def readNC():
      
      global keys,data, check_new
   
      path=entry1.get()
      path=path.replace('"',' ')
      data = nc.Dataset(path)
      keys=data.variables.keys()
      print("opened: ", path)
      
      if check_new == False: 
        global checkBoxes
        checkBoxes = []
        for key in keys: 
          print(data.variables[key])
          if key == 'ny':
               break
          checkBox=ctk.CTkCheckBox(master=frame,text=key)
          checkBox.pack(pady=12,padx=10)
          checkBoxes.append(checkBox)
          
        button2=ctk.CTkButton(master=frame,text="Create")
        button2.bind("<Button-1>", Get_Data)
        button2.pack(pady=5,padx=50)
        
      else:
        indx = 0
        for key in keys: 
            if key == 'ny':
                break
            checkBoxes[indx].configure(text=key)
            indx+=1
  
      check_new = True
      
def Get_Data(*args,**kwargs):
    unswer=[]
    global Buttonia
    for list in checkBoxes:    
        unswer.append(list.get())
    j=0
    for key in keys:
        if key == 'ny':
            break
        if unswer[j]==1:
            plot_data.append(key)
        j=j+1
    
    
    if Buttonia==False:
        button3.pack(pady=5,padx=60)
        button4.pack(pady=5,padx=60)
        Buttonia=True
      
def create_txt(plot_data):
    #fd = open(f'temp.txt', "w")
    for key in plot_data:
      values = data.variables[key][:]

      df = pd.DataFrame(values)  
      df=df.fillna(5)   
      print(df)
      df.to_csv('temp.csv', index=False)

    print('Done')

    
def Plot(*args, **kwards):

    data_to_plot=np.genfromtxt('temp.csv', delimiter=',')
        
    
    canvas.draw()
    canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
    button5.pack(pady=5,padx=60)
    ax.spines[['right', 'top','left','bottom']].set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.imshow(data_to_plot, cmap='gray', vmin=0, vmax=3)
       

def Save(fig):
    fig.savefig('Figure.jpeg')

if __name__ == '__main__':

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root=ctk.CTk()
    root.geometry("1024x800")

    check_new = False
    Buttonia=False

    plot_data = []
    
    frame=ctk.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill="both",expand=True)

    frame2=ctk.CTkFrame(master=frame)
    frame2.pack(side=ctk.RIGHT, pady=20,padx=60,fill="both",expand=True)
    

    fig = matplotlib.pyplot.Figure(figsize=(5, 4), dpi=100)
    
    ax = fig.add_subplot(1,1,1)
    

    canvas = FigureCanvasTkAgg(fig, master=frame2)  # A tk.DrawingArea.
    
    label=ctk.CTkLabel(master=frame,text="Open Netcdf File")
    label.pack(pady=12,padx=5)

    #entry path
    entry1=ctk.CTkEntry(master=frame,placeholder_text = "File Path ")
    entry1.pack(pady=12,padx=10)

    button=ctk.CTkButton(master=frame,text="Open",command=readNC)
    button.pack(pady=20,padx=20)

    button3=ctk.CTkButton(master=frame,text="Get Data")
    button3.bind("<Button-1>",lambda event ,p=plot_data: create_txt(p))    #downloading csv
                                       
    button4=ctk.CTkButton(master=frame,text="Plot")
    button4.bind("<Button-1>", lambda event, ax=ax, canvas=canvas:Plot(ax, canvas)) 
    
    button5=ctk.CTkButton(master=frame,text="Download Jpeg")
    button5.bind("<Button-1>", lambda event, fig=fig :Save(fig)) 
    root.mainloop()


