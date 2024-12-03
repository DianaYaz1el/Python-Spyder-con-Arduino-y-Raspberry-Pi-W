import sys
import requests
import tkinter as tk
from PIL import Image, ImageTk
import os

# Dirección IP de la Raspberry Pi Pico W
pico_ip = '192.168.X.XXX'  # Reemplaza con la IP de tu Pico W

# Rutas de las imágenes
ruta_fondo_meme = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\sweating_hero.png"
ruta_imagen_verde = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_verde.png"
ruta_imagen_rojo = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_rojo.png"
ruta_imagen_azul = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_azul.png"
ruta_imagen_mano = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\mano.png"

# Verificar si las imágenes existen
imagenes = [ruta_fondo_meme, ruta_imagen_verde, ruta_imagen_rojo, ruta_imagen_azul, ruta_imagen_mano]
for imagen in imagenes:
    if not os.path.exists(imagen):
        print(f"Imagen no encontrada: {imagen}")
        sys.exit()

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Control de LEDs con Raspberry Pi Pico W")
root.geometry("800x700")  # Ajustar el tamaño de la ventana según sea necesario

# Determinar el filtro de redimensionamiento
resize_filter = Image.LANCZOS

# Cargar y mostrar la imagen de fondo
try:
    fondo_meme = Image.open(ruta_fondo_meme).resize((600, 300), resize_filter)
    fondo_meme_tk = ImageTk.PhotoImage(fondo_meme)
    label_fondo = tk.Label(root, image=fondo_meme_tk)
    label_fondo.image = fondo_meme_tk  # Mantener referencia
    label_fondo.place(x=0, y=-0, relwidth=1, relheight=0.6)
except Exception as e:
    print(f"Error al cargar fondo_meme: {e}")
    sys.exit()

# Agregar el título
titulo = tk.Label(
    root,
    text="Elige un botón",
    font=("Comic Sans MS", 24, "italic bold underline"),
    fg="#b4cfed",  # azul
    bg="#02131E",  # Gris claro
    justify="center",
    relief="groove",
    bd=3,
    width=30
)
titulo.place(x=100, y=10)  # Ajusta la posición según tu diseño

# Cargar y mostrar la imagen de la mano
try:
    imagen_mano = Image.open(ruta_imagen_mano).resize((600, 300), resize_filter)
    imagen_mano_tk = ImageTk.PhotoImage(imagen_mano)
    label_mano = tk.Label(root, image=imagen_mano_tk)
    label_mano.image = imagen_mano_tk  # Mantener referencia
    label_mano.place(x=96, y=350)  # Ajustar posición de la mano
except Exception as e:
    print(f"Error al cargar imagen_mano: {e}")
    sys.exit()

# Función para cargar imágenes de botones
def cargar_imagen(ruta):
    try:
        imagen = Image.open(ruta).resize((70, 70), resize_filter)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"Error al cargar {ruta}: {e}")
        sys.exit()

# Cargar imágenes de los botones
imagen_verde_tk = cargar_imagen(ruta_imagen_verde)
imagen_rojo_tk = cargar_imagen(ruta_imagen_rojo)
imagen_azul_tk = cargar_imagen(ruta_imagen_azul)

# Crear etiquetas para mostrar el estado de cada LED
estado_verde = tk.Label(root, text="Apagado", font=("Arial", 12), fg="#000000")  # Negro
estado_verde.place(x=200, y=480)

estado_rojo = tk.Label(root, text="Apagado", font=("Arial", 12), fg="#000000")  # Negro
estado_rojo.place(x=350, y=480)

estado_azul = tk.Label(root, text="Apagado", font=("Arial", 12), fg="#000000")  # Negro
estado_azul.place(x=500, y=480)

# Función genérica para controlar los LEDs con toggle y actualizar estado
def toggle_led(color, etiqueta_estado):
    try:
        url = f'http://{pico_ip}/{color}toggle'
        response = requests.get(url)
        if response.status_code == 200:
            estado = response.text.strip()  # Obtener el estado del LED desde el servidor
            print(f"Respuesta del servidor: '{estado}'")  # Para depuración
            if "encendido" in estado.lower():
                etiqueta_estado.config(text="Encendido", fg="#008000")  # Verde
            elif "apagado" in estado.lower():
                etiqueta_estado.config(text="Apagado", fg="#FF0000")  # Rojo
            else:
                etiqueta_estado.config(text=estado.capitalize(), fg="#000000")  # Negro
        else:
            print(f"Error al realizar la acción: {response.status_code}")
    except Exception as e:
        print(f"No se pudo conectar al servidor:\n{e}")

# Crear botones con imágenes
btn_verde = tk.Button(root, image=imagen_verde_tk, command=lambda: toggle_led("verde", estado_verde), bg="#FFFFFF", relief="flat")
btn_verde.image = imagen_verde_tk
btn_verde.place(x=200, y=400)

btn_rojo = tk.Button(root, image=imagen_rojo_tk, command=lambda: toggle_led("rojo", estado_rojo), bg="#FFFFFF", relief="flat")
btn_rojo.image = imagen_rojo_tk
btn_rojo.place(x=350, y=400)

btn_azul = tk.Button(root, image=imagen_azul_tk, command=lambda: toggle_led("azul", estado_azul), bg="#FFFFFF", relief="flat")
btn_azul.image = imagen_azul_tk
btn_azul.place(x=500, y=400)

# Ejecutar el ciclo principal de Tkinter
root.mainloop()
