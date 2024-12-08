import tkinter as tk
from PIL import Image, ImageTk
import requests

# Dirección IP de la Raspberry Pi Pico W
pico_ip = "192.168.x.xxx"  # Cambia esta IP por la de tu Pico W

# Función para enviar comandos al servidor
def enviar_comando(comando):
    try:
        url = f"http://{pico_ip}/{comando}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Comando {comando} enviado con éxito")
        else:
            print(f"Error al enviar {comando}: {response.status_code}")
    except Exception as e:
        print(f"Error de conexión: {e}")

# Función para manejar las teclas presionadas
def manejar_tecla(event):
    if event.keysym == "Up":
        enviar_comando("adelante")
    elif event.keysym == "Down":
        enviar_comando("atras")
    elif event.keysym == "Right":
        enviar_comando("girar_derecha")
    elif event.keysym == "Left":
        enviar_comando("girar_izquierda")
    elif event.keysym == "space":
        enviar_comando("detener")

# Crear la interfaz
root = tk.Tk()
root.title("Control de Motores")
root.geometry("600x700")

# Rutas completas de las imágenes
ruta_flecha_arriba = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\up.png"
ruta_flecha_abajo = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\down.png"
ruta_flecha_derecha = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\right.png"
ruta_flecha_izquierda = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\left.png"
ruta_detener = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\stop.png"

# Cargar las imágenes de flechas y detener
flecha_arriba = ImageTk.PhotoImage(Image.open(ruta_flecha_arriba).resize((100, 100)))
flecha_abajo = ImageTk.PhotoImage(Image.open(ruta_flecha_abajo).resize((100, 100)))
flecha_derecha = ImageTk.PhotoImage(Image.open(ruta_flecha_derecha).resize((100, 100)))
flecha_izquierda = ImageTk.PhotoImage(Image.open(ruta_flecha_izquierda).resize((100, 100)))
imagen_detener = ImageTk.PhotoImage(Image.open(ruta_detener).resize((400, 100)))

# Botones con las imágenes
tk.Button(root, image=flecha_arriba, command=lambda: enviar_comando("adelante")).place(x=250, y=50)
tk.Button(root, image=flecha_abajo, command=lambda: enviar_comando("atras")).place(x=250, y=250)
tk.Button(root, image=flecha_derecha, command=lambda: enviar_comando("girar_derecha")).place(x=400, y=150)
tk.Button(root, image=flecha_izquierda, command=lambda: enviar_comando("girar_izquierda")).place(x=100, y=150)
tk.Button(root, image=imagen_detener, command=lambda: enviar_comando("detener")).place(x=90, y=400)

# Vincular las teclas del teclado
root.bind("<KeyPress>", manejar_tecla)

root.mainloop()
