import tkinter as tk
import math
import requests

# Dirección IP de la Raspberry Pi Pico W
pico_ip = "192.168.x.xxx"  # Cambia esta IP según tu configuración

# Función para enviar el ángulo al servidor
def mover_servo(angulo):
    try:
        url = f"http://{pico_ip}/mover?angulo={int(angulo)}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Servo movido a {int(angulo)}°")
        else:
            print(f"Error al mover el servo: {response.status_code}")
    except Exception as e:
        print(f"Error de conexión: {e}")

# Función para actualizar el ángulo con el slider circular
def actualizar_angulo(event):
    x, y = event.x - centro_x, centro_y - event.y
    angulo = math.degrees(math.atan2(y, x))
    if angulo < 0:
        angulo += 360

    if 0 <= angulo <= 180:
        marcador_x = centro_x + radio * math.cos(math.radians(angulo))
        marcador_y = centro_y - radio * math.sin(math.radians(angulo))
        canvas.coords(
            marcador,
            marcador_x - radio_marcador, marcador_y - radio_marcador,
            marcador_x + radio_marcador, marcador_y + radio_marcador
        )
        brazo_x = centro_x + (radio - 50) * math.cos(math.radians(angulo))
        brazo_y = centro_y - (radio - 50) * math.sin(math.radians(angulo))
        canvas.coords(brazo, centro_x, centro_y, brazo_x, brazo_y)
        label_angulo.config(text=f"Ángulo: {int(angulo)}°")
        mover_servo(angulo)

# Función para resetear el ángulo
def resetear_angulo():
    mover_servo(90)
    marcador_x = centro_x
    marcador_y = centro_y - radio
    canvas.coords(
        marcador,
        marcador_x - radio_marcador, marcador_y - radio_marcador,
        marcador_x + radio_marcador, marcador_y + radio_marcador
    )
    brazo_x = centro_x
    brazo_y = centro_y - (radio - 50)
    canvas.coords(brazo, centro_x, centro_y, brazo_x, brazo_y)
    label_angulo.config(text="Ángulo: 90°")

# Crear ventana principal
root = tk.Tk()
root.title("Slider Circular - Control de Servo")
root.geometry("400x500")
root.configure(bg="#daace0")  # Color de fondo

# Crear el canvas para el slider circular
canvas = tk.Canvas(root, width=400, height=400, bg="#ecd7e8", highlightthickness=0)
canvas.pack()

# Dibujar el círculo
centro_x, centro_y = 200, 200
radio = 150
canvas.create_oval(centro_x - radio, centro_y - radio, centro_x + radio, centro_y + radio, outline="#ae00ea", width=2)

# Ajustar tamaño del marcador
radio_marcador = 10  # Tamaño del marcador (original era 5)
marcador = canvas.create_oval(
    centro_x - radio_marcador, centro_y - radio - radio_marcador,
    centro_x + radio_marcador, centro_y - radio + radio_marcador,
    fill="#9500ea"
)

# Dibujar el brazo indicador del servo
brazo = canvas.create_line(centro_x, centro_y, centro_x, centro_y - (radio - 50), width=3, fill="#230535")

# Texto para mostrar el ángulo
label_angulo = tk.Label(root, text="Ángulo: 90°", font=("Arial", 14), bg="#f0f0f0")
label_angulo.pack(pady=10)

# Botón para resetear el ángulo
btn_reset = tk.Button(root, text="Resetear Ángulo", font=("Arial", 14), command=resetear_angulo, bg="#ea008a", fg="white")
btn_reset.pack(pady=10)

# Configurar eventos para arrastrar el marcador
canvas.bind("<B1-Motion>", actualizar_angulo)

# Ejecutar la aplicación
root.mainloop()
