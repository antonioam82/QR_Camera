from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox, filedialog
from pyzbar.pyzbar import decode
import cv2
import pyautogui
import numpy as np
from PIL import Image, ImageTk
import os

class App:
    def __init__(self):#,font_video=0):
        self.appName = 'QR Camera'
        self.ventana = Tk()
        self.ventana.title(self.appName)
        self.ventana['bg']='black'
        #self.font_video=font_video
        #self.vid=VideoCaptura(self.font_video)
        self.label=Label(self.ventana,text=self.appName,font=15,bg='blue',
                         fg='white').pack(side=TOP,fill=BOTH)
        self.display=scrolledtext.ScrolledText(self.ventana,width=86,background='snow3'
                                        ,height=4,padx=10, pady=10,font=('Arial', 10))
        self.display.pack(side=BOTTOM)
        
        self.canvas=Canvas(self.ventana,bg='black')#,width=self.vid.width,height=self.vid.height 600
        self.canvas.pack()
        self.btnLoad = Button(self.ventana,text="CARGAR ARCHIVO",width=29,bg='goldenrod2',
                    activebackground='red')
        self.btnLoad.pack(side=LEFT)
        self.btnCamera = Button(self.ventana,text="DETECTAR EN CAMARA",width=29,bg='goldenrod2',
                                activebackground='red',command=self.active_cam)
        self.btnCamera.pack(side=LEFT)
        self.btnScreen = Button(self.ventana,text="DETECTAR EN PANTALLA",width=30,bg='goldenrod2',
                                activebackground='red')
        self.btnScreen.pack(side=LEFT)

        #self.visor()
        self.ventana.mainloop()

    def active_cam(self):
        self.vid=cv2.VideoCapture(0)
        ret, frame = self.vid.read()

    def __del__(self):
        print("OK")

if __name__=="__main__":
    App()
           
