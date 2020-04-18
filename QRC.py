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
        self.active_camera = False
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
                    activebackground='red',command=self.abrir)
        self.btnLoad.pack(side=LEFT)
        self.btnCamera = Button(self.ventana,text="INICIAR CAMARA",width=29,bg='goldenrod2',
                                activebackground='red',command=self.active_cam)
        self.btnCamera.pack(side=LEFT)
        self.btnScreen = Button(self.ventana,text="DETECTAR EN PANTALLA",width=30,bg='goldenrod2',
                                activebackground='red',command=self.screen_shot)
        self.btnScreen.pack(side=LEFT)

        #self.visor()
        self.ventana.mainloop()
        
    def abrir(self):
        global info
        ruta = filedialog.askopenfilename(initialdir="/",title="SELECCIONAR ARCHIVO",
                    filetypes =(("png files","*.png") ,("jpg files","*.jpg")))
        if ruta != "":
            archivo = cv2.imread(ruta)
            info = decode(archivo)
            if info != []:
                self.display.delete('1.0',END)
                self.display.insert(END,info[0][0])
            else:
                messagebox.showwarning("ERROR","NO SE DETECTÓ CÓDIGO")
        
    def screen_shot(self):
        pyautogui.screenshot("QRsearch_screenshoot.jpg")
        archivo = cv2.imread("QRsearch_screenshoot.jpg")
        info = decode(archivo)
        if info != []:
            self.display.delete('1.0',END)
            self.display.insert(END,info[0][0])
        else:
            messagebox.showwarning("QR NO ENCONTRADO","NO SE DETECTÓ CÓDIGO")
        os.remove("QRsearch_screenshoot.jpg")
                    
    def active_cam(self):
        if self.active_camera == False:
            self.active_camera = True
            self.btnCamera.configure(text="CERRAR CAMARA")
            self.vid=cv2.VideoCapture(0)
            ret, frame = self.vid.read()
        else:
            self.active_camera = False
            self.btnCamera.configure(text="INICIAR CAMARA")
            self.vid.release()

    def __del__(self):
        print("OK")

if __name__=="__main__":
    App()
          

         
