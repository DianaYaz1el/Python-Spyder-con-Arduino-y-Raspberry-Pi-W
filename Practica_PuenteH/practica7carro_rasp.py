# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 21:24:10 2025

@author: diana
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# --- Config inicial ---
TIMEOUT = 1.5  # segundos para las peticiones HTTP

# --- Comprobación de conexión ---
def http_alive(ip, timeout=TIMEOUT):
    """Intenta /ping y luego / como fallback."""
    for path in ("/ping", "/"):
        try:
            r = requests.get(f"http://{ip}{path}", timeout=timeout)
            if r.status_code < 500:
                return True
        except requests.exceptions.RequestException:
            pass
    return False

# --- Envío de comandos ---
def enviar_comando(comando):
    if not estado["conectado"]:
        return
    ip = ent_ip.get().strip()
    try:
        url = f"http://{ip}/{comando}"
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            print(f"Comando {comando} enviado con éxito")
        else:
            print(f"Error al enviar {comando}: {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        on_desconectado("Conexión perdida durante el envío.")

# --- Teclado ---
def manejar_tecla(event):
    if not estado["conectado"]:
        return
    k = event.keysym
    if   k == "Up":    enviar_comando("adelante")
    elif k == "Down":  enviar_comando("atras")
    elif k == "Right": enviar_comando("girar_derecha")
    elif k == "Left":  enviar_comando("girar_izquierda")
    elif k == "space": enviar_comando("detener")

# --- UI helpers ---
def set_controles(habilitar: bool):
    st = ("normal" if habilitar else "disabled")
    for b in botones_mov:
        b.config(state=st)

def on_conectado():
    estado["conectado"] = True
    lbl_estado.config(text=f"Estado: Conectado a {ent_ip.get().strip()}", fg="green")
    btn_conectar.config(text="Reconectar", state="normal")
    set_controles(True)
    root.bind("<KeyPress>", manejar_tecla)

def on_desconectado(msg="No se pudo contactar el dispositivo."):
    estado["conectado"] = False
    lbl_estado.config(text=f"Estado: Desconectado. {msg}", fg="red")
    btn_conectar.config(text="Conectar", state="normal")
    set_controles(False)
    root.unbind("<KeyPress>")

def verificar_conexion():
    ip = ent_ip.get().strip()
    if not ip:
        messagebox.showwarning("IP faltante", "Ingresa la dirección IP del Pico W.")
        return
    lbl_estado.config(text="Estado: Verificando conexión...", fg="orange")
    btn_conectar.config(state="disabled")
    root.after(50, lambda: _hacer_verificacion(ip))

def _hacer_verificacion(ip):
    if http_alive(ip):
        on_conectado()
    else:
        on_desconectado(f"No responde en {ip}. Verifica Wi-Fi/energía/servidor HTTP.")

# --- Ventana principal ---
root = tk.Tk()
root.title("Control de Motores")
root.geometry("600x760")

estado = {"conectado": False}

# --- Encabezado conexión ---
frm_top = tk.Frame(root, padx=10, pady=10)
frm_top.pack(fill="x")

tk.Label(frm_top, text="IP del Pico W:").grid(row=0, column=0, sticky="w")
ent_ip = tk.Entry(frm_top, width=18)
ent_ip.grid(row=0, column=1, padx=(6,10))
ent_ip.insert(0, "192.168.0.xxx")  # Cambia si quieres otra por defecto

btn_conectar = tk.Button(frm_top, text="Conectar", command=verificar_conexion)
btn_conectar.grid(row=0, column=2, padx=(0,10))

lbl_estado = tk.Label(frm_top, text="Estado: Desconectado", fg="red")
lbl_estado.grid(row=1, column=0, columnspan=3, sticky="w", pady=(8,0))

tk.Label(frm_top, text="Usa las flechas (↑ ↓ ← →) y barra espaciadora para detener.").grid(
    row=2, column=0, columnspan=3, sticky="w", pady=(6,0)
)

# --- Carga de imágenes ---
ruta_flecha_arriba    = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\up.png"
ruta_flecha_abajo     = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\down.png"
ruta_flecha_derecha   = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\right.png"
ruta_flecha_izquierda = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\left.png"
ruta_detener          = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\stop.png"

flecha_arriba     = ImageTk.PhotoImage(Image.open(ruta_flecha_arriba).resize((100, 100)))
flecha_abajo      = ImageTk.PhotoImage(Image.open(ruta_flecha_abajo).resize((100, 100)))
flecha_derecha    = ImageTk.PhotoImage(Image.open(ruta_flecha_derecha).resize((100, 100)))
flecha_izquierda  = ImageTk.PhotoImage(Image.open(ruta_flecha_izquierda).resize((100, 100)))
imagen_detener    = ImageTk.PhotoImage(Image.open(ruta_detener).resize((400, 100)))

# --- Zona de control ---
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

btn_up    = tk.Button(root, image=flecha_arriba,    command=lambda: enviar_comando("adelante"),       state="disabled")
btn_down  = tk.Button(root, image=flecha_abajo,     command=lambda: enviar_comando("atras"),          state="disabled")
btn_right = tk.Button(root, image=flecha_derecha,   command=lambda: enviar_comando("girar_derecha"),  state="disabled")
btn_left  = tk.Button(root, image=flecha_izquierda, command=lambda: enviar_comando("girar_izquierda"),state="disabled")
btn_stop  = tk.Button(root, image=imagen_detener,   command=lambda: enviar_comando("detener"),        state="disabled")

# Ubicación similar a la tuya
btn_up.place(x=250, y=120)
btn_down.place(x=250, y=320)
btn_right.place(x=400, y=220)
btn_left.place(x=100, y=220)
btn_stop.place(x=90, y=470)

botones_mov = [btn_up, btn_down, btn_right, btn_left, btn_stop]
set_controles(False)  # arrancan deshabilitados

# Nota: el bind del teclado se activa al conectar
root.mainloop()
