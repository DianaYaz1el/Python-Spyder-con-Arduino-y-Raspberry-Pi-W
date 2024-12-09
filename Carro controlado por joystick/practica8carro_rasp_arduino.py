import tkinter as tk
import requests
from pyfirmata import Arduino, util

# Configuración de Arduino
arduino_port = "COM4"  # Cambia este puerto según tu configuración
board = Arduino(arduino_port)
it = util.Iterator(board)
it.start()

# Pines del joystick
x_pin = board.get_pin('a:3:i')  # Eje y conectado al pin A2 del Arduino
y_pin = board.get_pin('a:2:i')  # Eje x conectado al pin A3 del Arduino
# Si tienes botón SW, puedes leerlo también, pero no es obligatorio
x_pin.enable_reporting()
y_pin.enable_reporting()

# Dirección IP de la Raspberry Pi Pico W
pico_ip = "192.168.X.XXX"  # Cambia esta IP por la de tu Pico W

# Variables para evitar reenvío de comandos constantes
ultimo_comando = None

def enviar_comando(comando):
    global ultimo_comando
    if comando != ultimo_comando:
        try:
            url = f"http://{pico_ip}/{comando}"
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Comando {comando} enviado con éxito")
            else:
                print(f"Error al enviar {comando}: {response.status_code}")
        except Exception as e:
            print(f"Error de conexión: {e}")
        ultimo_comando = comando

# Ajustes de zona muerta y umbrales
zona_muerta = 0.3
umbral_mov = 0.7

def actualizar_joystick():
    x_val = x_pin.read()
    y_val = y_pin.read()

    if x_val is not None and y_val is not None:
        x = x_val * 2 - 1  # Rango -1 a 1
        y = y_val * 2 - 1

        # Mover el marcador según x,y en el canvas
        desplazamiento = 100
        marcador_x = centro_x + x * desplazamiento
        marcador_y = centro_y - y * desplazamiento
        canvas.coords(marcador, marcador_x - 5, marcador_y - 5, marcador_x + 5, marcador_y + 5)

        # Lógica para el movimiento del carrito usando umbrales
        # Primero, la zona muerta
        if abs(x) < zona_muerta and abs(y) < zona_muerta:
            enviar_comando("detener")
        else:
            # Determinar comando según eje dominante
            # Si |y| > |x|, priorizamos adelante/atrás
            # Si |x| >= |y|, priorizamos giro
            if abs(y) > abs(x):
                if y > umbral_mov:
                    enviar_comando("adelante")
                elif y < -umbral_mov:
                    enviar_comando("atras")
                else:
                    # Si no llega al umbral, detenemos
                    enviar_comando("detener")
            else:
                if x > umbral_mov:
                    enviar_comando("girar_derecha")
                elif x < -umbral_mov:
                    enviar_comando("girar_izquierda")
                else:
                    enviar_comando("detener")

    root.after(100, actualizar_joystick)  # Actualizar cada 100ms

def cerrar():
    board.exit()
    root.destroy()

root = tk.Tk()
root.title("Control del Carrito con Joystick")
root.geometry("600x700")
root.configure(bg="#f0f0f0")  # gris claro

titulo = tk.Label(
    root,
    text="Control del Carrito con Joystick",
    font=("Comic Sans MS", 24, "italic bold underline"),
    fg="#800080",  # Púrpura
    bg="#D3D3D3",  # Gris claro
    justify="center",
    relief="groove",
    bd=3,
    width=30
)
titulo.pack(pady=10)

canvas = tk.Canvas(root, width=400, height=400, bg="#FFFFFF", highlightthickness=0)
canvas.pack()

centro_x, centro_y = 200, 200
# Dibujar la cruz
canvas.create_line(0, centro_y, 400, centro_y, fill="#000000", width=2)
canvas.create_line(centro_x, 0, centro_x, 400, fill="#000000", width=2)

# Marcador del joystick
marcador = canvas.create_oval(centro_x - 5, centro_y - 5, centro_x + 5, centro_y + 5, fill="#1b2bf5")

# Ya no mostramos ángulo, así que removemos cualquier label de ángulo
# Etiqueta del ángulo eliminada

btn_cerrar = tk.Button(root, text="Cerrar", font=("Arial", 14), command=cerrar, bg="#aa2929", fg="#FFFFFF")
btn_cerrar.pack(pady=10)

actualizar_joystick()

root.mainloop()
