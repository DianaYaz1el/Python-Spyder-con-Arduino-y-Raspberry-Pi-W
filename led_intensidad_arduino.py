from pyfirmata import Arduino, PWM
import tkinter as tk
from PIL import Image, ImageTk
import os

# Configuración de Arduino
board = Arduino('COM13')  # Cambia 'COM4' por el puerto correspondiente
led_pin = board.get_pin('d:9:p')  # Pin 9 configurado como PWM

# Rutas de las imágenes
ruta_led_apagado = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_apagado.png"
ruta_led_bajo = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_bajo.png"
ruta_led_medio = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_medio.png"
ruta_led_alto = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\led_alto.png"

# Verificar que las imágenes existan
imagenes = [ruta_led_apagado, ruta_led_bajo, ruta_led_medio, ruta_led_alto]
for imagen in imagenes:
    if not os.path.exists(imagen):
        print(f"Imagen no encontrada: {imagen}")
        exit()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Control de Intensidad del LED")
root.geometry("500x500")

# Determinar el filtro de redimensionamiento
resize_filter = Image.LANCZOS

# Cargar imágenes del LED
imagen_apagado = Image.open(ruta_led_apagado).resize((200, 200), resize_filter)
imagen_bajo = Image.open(ruta_led_bajo).resize((200, 200), resize_filter)
imagen_medio = Image.open(ruta_led_medio).resize((200, 200), resize_filter)
imagen_alto = Image.open(ruta_led_alto).resize((200, 200), resize_filter)

imagenes_led = {
    "apagado": ImageTk.PhotoImage(imagen_apagado),
    "bajo": ImageTk.PhotoImage(imagen_bajo),
    "medio": ImageTk.PhotoImage(imagen_medio),
    "alto": ImageTk.PhotoImage(imagen_alto),
}

# Etiqueta para mostrar la imagen del LED
label_led = tk.Label(root, image=imagenes_led["apagado"])
label_led.pack(pady=20)

# Función para actualizar la intensidad del LED y la imagen

def actualizar_led(valor):
    intensidad = int(valor) / 100  # Convertir el valor del slider (0-100) a PWM (0-1)
    led_pin.write(intensidad)  # Enviar valor PWM al pin del LED

    # Cambiar la imagen del LED según la intensidad
    if intensidad == 0:
        label_led.config(image=imagenes_led["apagado"])
    elif 0 < intensidad <= 0.3:
        label_led.config(image=imagenes_led["bajo"])
    elif 0.3 < intensidad <= 0.7:
        label_led.config(image=imagenes_led["medio"])
    else:
        label_led.config(image=imagenes_led["alto"])

# Crear un deslizador para controlar la intensidad
slider = tk.Scale(root, from_=0, to=100, orient="horizontal", command=actualizar_led,
                  label="Intensidad del LED (%)", length=300)
slider.pack(pady=20)

# Iniciar la interfaz gráfica
try:
    root.mainloop()
finally:
    # Apagar el LED y cerrar la conexión con Arduino al salir
    led_pin.write(0)
    board.exit()
