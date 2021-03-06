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
    def __init__(self,font_video=0):
        self.info = []
        self.appName = "QR Camera"
        self.ventana = Tk()
        self.ventana.title(self.appName)
        self.ventana['bg']='black'
        self.font_video=font_video
        self.vid=VideoCaptura(self.font_video)
        self.label=Label(self.ventana,text=self.appName,font=15,bg='blue',
                         fg='white').pack(side=TOP,fill=BOTH)
        self.btnSave = Button(self.ventana,text="GUARDAR INFO",bg='light blue',command=self.guardar)
        self.btnSave.pack(side=BOTTOM)        
        self.display=scrolledtext.ScrolledText(self.ventana,width=86,background='snow3'
                                        ,height=4,padx=10, pady=10,font=('Arial', 10))
        self.display.pack(side=BOTTOM)
        
        self.canvas=Canvas(self.ventana,bg='red',width=self.vid.width,height=self.vid.height)
        self.canvas.pack()
        
        self.btnCamera = Button(self.ventana,text="DETECTAR EN CAMARA",width=29,bg='goldenrod2',
                                activebackground='red',command=self.captura)
        self.btnCamera.pack(side=TOP,fill=X)

        self.visor()
        self.ventana.mainloop()
    
        
    def guardar(self):
        if self.info != []:
            documento=open('QR_info.txt',"w",encoding="utf-8")
            linea=""
            for c in str(self.info[0][0]):
                linea=linea+c
            documento.write(linea)
            documento.close()
            messagebox.showinfo("GUARDADO","INFORMACIÓN GUARDADA EN \'QR_info.txt\'")
    def captura(self):
        ver,frame=self.vid.get_frame()
        if ver:
            image="cameraCapt.jpg"
            cv2.imwrite(image,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            self.leer()
            
    def visor(self):
        ret, frame=self.vid.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor=NW)#0,0
            self.ventana.after(15,self.visor)
        else:
            messagebox.showwarning("CAMARA NO DISPONIBLE","""La cámara está siendo utilizada por otra aplicación.
               Cierrela e intentelo de nuevo.""")

    def leer(self):
        archivo = cv2.imread("cameraCapt.jpg")
        self.info = decode(archivo)
        if self.info != []:
            self.display.delete('1.0',END)
            self.display.insert(END,self.info[0][0])
        else:
            messagebox.showwarning("QR NO ENCONTRADO","NO SE DETECTÓ CÓDIGO")
        os.remove("cameraCapt.jpg")

class VideoCaptura:
    def __init__(self,font_video=0):
        self.vid = cv2.VideoCapture(font_video)
        if not self.vid.isOpened():
            raise ValueError("No se puede usar esta camara")
        self.width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    def get_frame(self):
        if self.vid.isOpened():
            verif,frame=self.vid.read()
            if verif:
                return(verif,cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return(verif,None)
        else:
            return(verif,None)
        
    def __del__(self):
        print("OK")
        #if self.vid.isOpened():
            #self.vid.release()
                
if __name__=="__main__":
    App()
