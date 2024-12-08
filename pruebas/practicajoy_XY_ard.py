import tkinter as tk
import pyfirmata

# Configurar el Arduino
board = pyfirmata.Arduino('COM4')  # Cambia 'COM4' por el puerto correcto

# Iniciar el iterador
it = pyfirmata.util.Iterator(board)
it.start()

# Configurar los pines del joystick
x_pin = board.get_pin('a:0:i')  # Eje X conectado al pin A0
y_pin = board.get_pin('a:1:i')  # Eje Y conectado al pin A1
sw_pin = board.get_pin('d:2:i')  # Botón SW conectado al pin D2

# Activar lectura en los pines
x_pin.enable_reporting()
y_pin.enable_reporting()
sw_pin.enable_reporting()

# Crear la ventana principal
root = tk.Tk()
root.title("Joystick - Control de Ejes")
root.geometry("400x500")
root.configure(bg="#daace0")  # Fondo gris claro

# Crear el canvas para la cruz y los ejes
canvas = tk.Canvas(root, width=300, height=300, bg="#ffffff", highlightthickness=0)
canvas.pack(pady=20)

# Dibujar la cruz central
cruz_x = canvas.create_line(150, 0, 150, 300, fill="#007ACC", width=2)  # Azul
cruz_y = canvas.create_line(0, 150, 300, 150, fill="#007ACC", width=2)  # Azul

# Etiquetas de los ejes
label_x = tk.Label(root, text="Eje X (Arriba/Abajo)", font=("Arial", 12), bg="#ececec", fg="#007ACC")
label_x.pack()

label_y = tk.Label(root, text="Eje Y (Izquierda/Derecha)", font=("Arial", 12), bg="#ececec", fg="#007ACC")
label_y.pack()

# Etiqueta para mostrar los valores de X e Y
label_valores = tk.Label(root, text="Eje X: 0, Eje Y: 0", font=("Arial", 12), bg="#ececec", fg="#FF5733")
label_valores.pack(pady=10)

# Crear el marcador para el joystick
marcador = canvas.create_oval(145, 145, 155, 155, fill="#FF5733")  # Naranja

# Función para actualizar la posición del marcador
def actualizar_marcador():
    x_val = x_pin.read()
    y_val = y_pin.read()
    
    if x_val is not None and y_val is not None:
        # Escalar los valores a un rango de 0 a 300
        y_pos = 300 - int(x_val * 300)  # Eje X ajustado para arriba/abajo
        x_pos = int(y_val * 300)       # Eje Y ajustado para izquierda/derecha

        # Limitar los valores dentro del canvas
        y_pos = max(0, min(300, y_pos))
        x_pos = max(0, min(300, x_pos))

        # Actualizar la posición del marcador
        canvas.coords(marcador, x_pos - 5, y_pos - 5, x_pos + 5, y_pos + 5)

        # Actualizar la etiqueta con los valores de X e Y
        label_valores.config(text=f"Eje X: {int(x_val * 1023)}, Eje Y: {int(y_val * 1023)}")
    
    root.after(50, actualizar_marcador)  # Llamar a la función cada 50ms

# Botón para cerrar la aplicación
def cerrar():
    board.exit()
    root.destroy()

btn_cerrar = tk.Button(root, text="Cerrar", font=("Arial", 12), bg="#C0392B", fg="white", width=10, command=cerrar)
btn_cerrar.pack(pady=10)

# Iniciar la actualización del marcador
actualizar_marcador()

# Ejecutar la interfaz gráfica
root.mainloop()

