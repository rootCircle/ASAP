# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:14:14 2020

@author: compaq
"""

import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
app = tk.Tk()
app.geometry("200x400")
style = ThemedStyle(app)
style.set_theme("equilux")
#elegance
#Breeze
#Equilux
#Arc
#clearlooks
#scidmint
e =ttk.Entry(app)
e.pack()
ttk.Button(app, text="The button",command=lambda:style.set_theme(setth.get())).pack()
themes=style.theme_names()
print(len(themes))
setth=tk.StringVar(app,'scidmint')
Menu=ttk.OptionMenu(app,setth,*themes)
Menu.pack()
gender=tk.StringVar(app,"F")
GEN={"Male":"M","Female":"F","Not specified":"N"}
for (text,value) in GEN.items():
    ttk.Radiobutton(app,text=text,variable=gender,value=value).pack()
ttk.Label(app,text="Breeze,Equilux,Arc").pack()
recordMeet = False
ttk.Checkbutton(app, text='Record Meeting?', variable=recordMeet, onvalue=True, offvalue=False).pack()
app.mainloop()
