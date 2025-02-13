import tkinter as tk
from pyfirmata import Arduino, util
from PIL import Image, ImageTk  # Para redimensionar la imagen

# Configuración de Arduino
board = Arduino('COM13')  # Cambia 'COM4' por el puerto correcto
it = util.Iterator(board)
it.start()

# Configurar los pines del joystick
x_pin = board.get_pin('a:0:i')  # Eje X conectado al pin A0
y_pin = board.get_pin('a:1:i')  # Eje Y conectado al pin A1
x_pin.enable_reporting()
y_pin.enable_reporting()

# Configuración de la ventana
root = tk.Tk()
root.title("Joystick - Control de Ejes")
root.geometry("700x800")  # Aumentar el tamaño de la ventana
root.configure(bg="#dab6fc")

# Canvas para la cruz y el marcador
canvas = tk.Canvas(root, width=500, height=500, bg="#f3dafc", highlightthickness=0)  # Aumentar el tamaño del Canvas
canvas.pack(pady=20)

# Dibujar la cruz más grande
canvas.create_line(250, 0, 250, 500, fill="blue", width=4)  # Línea vertical más grande
canvas.create_line(0, 250, 500, 250, fill="blue", width=4)  # Línea horizontal más grande

# Cargar la imagen de Morty y mantener su tamaño
original_image = Image.open("C:/Users/diana/Pyton_microcontroladores/ImagenesInterfaces/morty.png")
resized_image = original_image.resize((50, 50))  # Mantener el tamaño original
morty_image = ImageTk.PhotoImage(resized_image)
marker = canvas.create_image(250, 250, image=morty_image)  # Centrar en el canvas más grande

# Etiquetas de los ejes más grandes
label_x = tk.Label(root, text="Eje X (Arriba/Abajo)", bg="#aad8e6", font=("Arial", 16))  # Fuente más grande
label_x.pack()

label_y = tk.Label(root, text="Eje Y (Izquierda/Derecha)", bg="#aad8e6", font=("Arial", 16))  # Fuente más grande
label_y.pack()

# Etiqueta para mostrar los valores más grande
position_label = tk.Label(root, text="Eje X: 0, Eje Y: 0", bg="#ffffff", font=("Arial", 16))
position_label.pack(pady=20)

# Función para actualizar la posición del marcador
def actualizar_marcador():
    x_val = x_pin.read()
    y_val = y_pin.read()
    
    if x_val is not None and y_val is not None:
        # Ajustar la posición del marcador (basado en tu lógica original)
        y_pos = 500 - int(x_val * 500)  # Eje X ajustado para arriba/abajo
        x_pos = int(y_val * 500)       # Eje Y ajustado para izquierda/derecha

        # Limitar los valores dentro del canvas
        y_pos = max(0, min(500, y_pos))
        x_pos = max(0, min(500, x_pos))

        # Actualizar la posición del marcador
        canvas.coords(marker, x_pos, y_pos)

        # Actualizar la etiqueta con los valores de X e Y
        position_label.config(text=f"Eje X: {int(x_val * 1023)}, Eje Y: {int(y_val * 1023)}")
    
    root.after(50, actualizar_marcador)  # Llamar a la función cada 50ms

# Botón para cerrar la aplicación más grande
def cerrar():
    board.exit()
    root.destroy()

btn_cerrar = tk.Button(root, text="Cerrar", font=("Arial", 16), bg="#aa2929", fg="white", width=12, height=2, command=cerrar)
btn_cerrar.pack(pady=20)

# Iniciar la actualización del marcador
actualizar_marcador()

# Ejecutar la interfaz gráfica
root.mainloop()

