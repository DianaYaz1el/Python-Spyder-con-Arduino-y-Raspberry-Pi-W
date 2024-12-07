import tkinter as tk
import math
import requests
from pyfirmata import Arduino, util

# Configuración de Arduino
arduino_port = "COM4"  # Cambia este puerto según tu configuración
board = Arduino(arduino_port)
it = util.Iterator(board)
it.start()

# Configurar los pines del joystick
x_pin = board.get_pin('a:0:i')  # Eje X conectado al pin A0 del Arduino
y_pin = board.get_pin('a:1:i')  # Eje Y conectado al pin A1 del Arduino
x_pin.enable_reporting()
y_pin.enable_reporting()

# Configuración de la Raspberry Pi Pico W
pico_ip = "192.168.x.xxx"  # Cambia esta IP según tu configuración

# Parámetros de la zona muerta
zona_muerta = 5  # ±5 grados alrededor de 90°

# Función para enviar el ángulo al servidor de la Raspberry Pi Pico W
def mover_servo(angulo):
    # Asegurar que el ángulo esté dentro de 0-180
    angulo = max(0, min(180, angulo))
    try:
        url = f"http://{pico_ip}/mover?angulo={int(angulo)}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Servo movido a {int(angulo)}°")
        else:
            print(f"Error al mover el servo: {response.status_code}")
    except Exception as e:
        print(f"Error de conexión: {e}")

# Función para leer los valores del joystick y calcular el ángulo
def actualizar_joystick():
    x_val = x_pin.read()
    y_val = y_pin.read()

    if x_val is not None and y_val is not None:
        # Escalar valores a rango de -1 a 1
        x = x_val * 2 - 1
        y = y_val * 2 - 1

        # Si el joystick está casi en el centro (ej. ±0.05 alrededor de x=0,y=0),
        # consideramos que está en reposo y forzamos el ángulo a 90°
        if abs(x) < 0.05 and abs(y) < 0.05:
            # Joystick en reposo, servo en 90°
            mover_servo(90)
            brazo_x = centro_x
            brazo_y = centro_y - (radio - 50)
            canvas.coords(brazo, centro_x, centro_y, brazo_x, brazo_y)
            label_angulo.config(text="Ángulo: 90°")
        else:
            # Calcular el ángulo del joystick en grados
            # Primero obtenemos el ángulo usando atan2
            angulo = math.degrees(math.atan2(-y, x))

            # Normalizar el ángulo para que esté entre 0 y 360
            if angulo < 0:
                angulo += 360

            # Ajustar rango a 0-180: Si >180, lo limitamos a 180
            if angulo > 180:
                angulo = 180

            # Calcular diferencia respecto a 90°
            diferencia = abs(angulo - 90)

            # Si la diferencia es mayor a 4°, mover el servo al ángulo calculado
            if diferencia > zona_muerta:
                mover_servo(angulo)
                # Actualizar el brazo indicador en el canvas
                brazo_x = centro_x + (radio - 50) * math.cos(math.radians(angulo))
                brazo_y = centro_y - (radio - 50) * math.sin(math.radians(angulo))
                canvas.coords(brazo, centro_x, centro_y, brazo_x, brazo_y)
                label_angulo.config(text=f"Ángulo: {int(angulo)}°")
            else:
                # Si la diferencia es menor o igual a 4°, mantener/volver a 90°
                mover_servo(90)
                brazo_x = centro_x
                brazo_y = centro_y - (radio - 50)
                canvas.coords(brazo, centro_x, centro_y, brazo_x, brazo_y)
                label_angulo.config(text="Ángulo: 90°")

    root.after(50, actualizar_joystick)  # Actualizar cada 50ms

# Función para cerrar la aplicación
def cerrar():
    board.exit()
    root.destroy()

# Crear ventana principal
root = tk.Tk()
root.title("Control de Servo con Joystick")
root.geometry("600x700")
root.configure(bg="#f0f0f0")  # Gris claro

# Agregar el título (con códigos hexadecimales)
titulo = tk.Label(
    root,
    text="Oprime cerrar para salir",
    font=("Courier New", 24, "italic bold underline"),
    fg="#032655",   # azul
    bg="#87cfe6",   # Gris claro
    justify="center",
    relief="groove",
    bd=3,
    width=30
)
titulo.pack(pady=10)

# Canvas para representar el joystick
canvas = tk.Canvas(root, width=400, height=400, bg="#FFFFFF", highlightthickness=0)  # Fondo blanco
canvas.pack()

# Dibujar círculo del slider
centro_x, centro_y = 200, 200
radio = 150
canvas.create_oval(centro_x - radio, centro_y - radio, centro_x + radio, centro_y + radio, outline="#000000", width=2)  # Negro

# Dibujar brazo del servo (verde #008000)
brazo = canvas.create_line(centro_x, centro_y, centro_x, centro_y - (radio - 50), width=3, fill="#1b2bf5")

# Etiqueta para mostrar el ángulo (azul #0000FF)
label_angulo = tk.Label(root, text="Ángulo: 90°", font=("Arial", 14), bg="#f0f0f0", fg="#0000FF")
label_angulo.pack(pady=10)

# Botón para cerrar la aplicación (rojo #aa2929 con texto blanco #FFFFFF)
btn_cerrar = tk.Button(root, text="Cerrar", font=("Ubuntu Mono", 20), command=cerrar, bg="#5a7ef0", fg="#000000")
btn_cerrar.pack(pady=10)

# Iniciar la lectura del joystick
actualizar_joystick()

# Ejecutar la interfaz
root.mainloop()
