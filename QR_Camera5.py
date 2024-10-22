#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox, filedialog
import cv2
import pyperclip
import pyautogui
import numpy as np
import threading
from PIL import Image, ImageTk, ImageGrab
import os
 
class App:
    def __init__(self, font_video=0):
        self.active_camera = False
        self.info = []
        self.codelist = []
        self.appName = 'QR Code Reader'
        self.ventana = tk.Tk()
        self.ventana.title(self.appName)
        self.ventana.resizable(height=tk.FALSE, width=tk.FALSE)
        self.ventana['bg'] = 'black'
        self.currentDir = tk.StringVar()
        self.currentDir.set(os.getcwd())
        self.font_video = font_video
        tk.Entry(self.ventana, textvariable=self.currentDir, width=107).pack(side=tk.TOP)
        tk.Label(self.ventana, text=self.appName, font=15, bg='blue',
                 fg='white').pack(side=tk.TOP, fill=tk.BOTH)
        bt_canvas = tk.Canvas(self.ventana)
        bt_canvas.pack(side=tk.BOTTOM)
        tk.Button(bt_canvas, text="GUARDAR", width=10, bg='light blue', command=self.guardar).pack(side=tk.LEFT)
        tk.Button(bt_canvas, text="COPIAR", width=10, bg='light blue', command=self.copy_info).pack(side=tk.LEFT)

        self.display = scrolledtext.ScrolledText(self.ventana, width=86, background='snow3',
                                                 height=4, padx=10, pady=10, font=('Arial', 10))
        self.display.pack(side=tk.BOTTOM)

        self.canvas = tk.Canvas(self.ventana, bg='black', width=640, height=0)
        self.canvas.pack()
        tk.Button(self.ventana, text="CARGAR ARCHIVO", width=29, bg='goldenrod2', activebackground='red',
                  command=self.abrir).pack(side=tk.LEFT)
        self.btnCamera = tk.Button(self.ventana, text="INICIAR LECTURA POR CAMARA", width=30, bg='goldenrod2',
                                   activebackground='red', command=self.active_cam)
        self.btnCamera.pack(side=tk.LEFT)
        tk.Button(self.ventana, text="DETECTAR EN PANTALLA", width=29, bg='goldenrod2', activebackground='red',
                  command=self.screen_shot).pack(side=tk.RIGHT)

        self.ventana.mainloop()

    def guardar(self):
        if len(self.display.get('1.0', tk.END)) > 1:
            documento = filedialog.asksaveasfilename(initialdir="/",
                                                     title="Guardar en", defaultextension='.txt')
            if documento != "":
                with open(documento, "w", encoding="utf-8") as archivo_guardar:
                    archivo_guardar.write(self.display.get('1.0', tk.END))
                messagebox.showinfo("GUARDADO", "INFORMACIÓN GUARDADA EN \'{}\'".format(documento))

    def copy_info(self):
        try:
            if len(self.display.get('1.0', tk.END)) > 1:
                pyperclip.copy(self.display.get('1.0', tk.END))
                messagebox.showinfo("COPIADO", "Copiado en el portapapeles.")
        except Exception as e:
            messagebox.showwarning("UNEXPECTED ERROR", str(e))

    def abrir(self):
        ruta = filedialog.askopenfilename(initialdir="/", title="SELECCIONAR ARCHIVO",
                                          filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
        if ruta != "":
            archivo = cv2.imread(ruta)
            qrCode = cv2.QRCodeDetector()
            retval, decoded_info, points, _ = qrCode.detectAndDecodeMulti(archivo)
            if retval:
                self.display.delete('1.0', tk.END)
                for info in decoded_info:
                    self.display.insert(tk.END, info + '\n')
            else:
                messagebox.showwarning("ARCHIVO NO VÁLIDO", "NO SE DETECTÓ CÓDIGO QR.")

    def screen_shot(self):
        screenshot = ImageGrab.grab()  # captura pantalla
        screenshot = np.array(screenshot)  # arreglo numpy

        qrCode = cv2.QRCodeDetector()
        retval, decoded_info, points, _ = qrCode.detectAndDecodeMulti(screenshot)
        if retval:
            self.display.delete('1.0', tk.END)
            for info in decoded_info:
                self.display.insert(tk.END, info + '\n')
        else:
            messagebox.showwarning("QR NO ENCONTRADO", "NO SE DETECTÓ CÓDIGO")

    def visor(self):
        ret, frame = self.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.ventana.after(15, self.visor)

    def active_cam(self):
        if not self.active_camera:
            self.active_camera = True
            self.VideoCaptura()
            self.visor()
        else:
            self.active_camera = False
            self.codelist = []
            self.btnCamera.configure(text="INICIAR LECTURA POR CAMARA")
            self.vid.release()
            self.canvas.delete('all')
            self.canvas.configure(height=0)

    def capta(self, frm):
        qrCode = cv2.QRCodeDetector()
        retval, decoded_info, points, _ = qrCode.detectAndDecodeMulti(frm)
        cv2.putText(frm, "Muestre el codigo delante de la camara para su lectura", (84, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if retval:
            self.display.delete('1.0', tk.END)
            for info in decoded_info:
                if info not in self.codelist:
                    self.codelist.append(info)
                    self.display.insert(tk.END, info + '\n')
                self.draw_rectangle(frm, points)
        else:
            if len(self.codelist) > 0:
                self.display.delete('1.0', tk.END)
                for e in set(self.codelist):
                    self.display.insert(tk.END, e + '\n')

    def get_frame(self):
        if self.vid.isOpened():
            verif, frame = self.vid.read()
            if verif:
                self.btnCamera.configure(text="CERRAR CAMARA")
                self.capta(frame)
                return verif, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                messagebox.showwarning("CAMARA NO DISPONIBLE", """La cámara está siendo utilizada por otra aplicación.
                Cierrela e intentelo de nuevo.""")
                self.active_cam()
                return verif, None
        else:
            return False, None

    def draw_rectangle(self, frm, points):
        if points is not None:
            for point in points:
                points_int = point.astype(int)
                frm = cv2.polylines(frm, [points_int], True, (255, 0, 0), 6)

    def VideoCaptura(self):
        self.vid = cv2.VideoCapture(self.font_video)
        if self.vid.isOpened():
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.canvas.configure(width=self.width, height=self.height)
        else:
            messagebox.showwarning("CAMARA NO DISPONIBLE", "El dispositivo está desactivado o no disponible")
            self.display.delete('1.0', tk.END)
            self.active_camera = False

    def __del__(self):
        if self.active_camera:
            self.vid.release()

if __name__ == "__main__":
    App()
