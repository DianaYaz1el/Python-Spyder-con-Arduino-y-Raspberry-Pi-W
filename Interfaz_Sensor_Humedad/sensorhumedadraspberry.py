import tkinter as tk
from PIL import Image, ImageTk
import requests

# Dirección IP de la Raspberry Pi Pico W
pico_ip = "192.168.x.xxx"  #  Verifica que esta sea tu IP real

# Bandera de control
leyendo = True  # ← Se activa automáticamente

# Función para obtener datos del sensor
def obtener_datos():
    global leyendo
    if leyendo:
        try:
            response = requests.get(f"http://{pico_ip}/sensor", timeout=2)
            if response.status_code == 200:
                datos = response.json()
                temperatura = datos["temp"]
                humedad = datos["hum"] - 5  # ← Ajuste para corregir humedad alta
                if humedad < 0:
                    humedad = 0  # Evita valores negativos

                temp_label.config(text=f"{temperatura:.1f} °C", fg="red")
                hum_label.config(text=f"{humedad:.1f} %", fg="blue")
                error_label.config(text="")
            else:
                error_label.config(text="Error al recibir datos", fg="orange")
        except Exception as e:
            error_label.config(text="Formato incorrecto", fg="orange")
        root.after(2000, obtener_datos)

# Iniciar lectura manual (opcional)
def iniciar():
    global leyendo
    if not leyendo:
        leyendo = True
        error_label.config(text="Reanudando lectura...", fg="green")
        obtener_datos()

# Detener lectura
def detener():
    global leyendo
    leyendo = False
    error_label.config(text="Lectura detenida", fg="red")

# Crear ventana principal
root = tk.Tk()
root.title("Sensor DHT22 - Raspberry Pi Pico W")
root.geometry("400x550")
root.configure(bg="#DDF2FF")

# Título
tk.Label(root, text="Sensor DHT22 - Raspberry Pi Pico W", font=("Arial", 16, "bold"),
         bg="#DDF2FF", fg="#0B5ED7").pack(pady=10)

# Imagen decorativa
ruta_sensor = r"C:\Users\diana\Programas_Python\Imagenes\humedad.png"
imagen = Image.open(ruta_sensor).resize((200, 200))
imagen_tk = ImageTk.PhotoImage(imagen)
tk.Label(root, image=imagen_tk, bg="#DDF2FF").pack(pady=10)

# Etiquetas de lectura
tk.Label(root, text="Temperatura:", font=("Arial", 14), bg="#DDF2FF").pack()
temp_label = tk.Label(root, text="- °C", font=("Arial", 20), bg="white", width=10)
temp_label.pack(pady=5)

tk.Label(root, text="Humedad:", font=("Arial", 14), bg="#DDF2FF").pack()
hum_label = tk.Label(root, text="- %", font=("Arial", 20), bg="white", width=10)
hum_label.pack(pady=5)

# Estado / errores
error_label = tk.Label(root, text="", font=("Arial", 10), bg="#DDF2FF", fg="orange")
error_label.pack(pady=10)

# Botones de control manual (opcional)
tk.Button(root, text="Iniciar", command=iniciar, bg="#0B5ED7", fg="white",
          font=("Arial", 14), width=10).pack(pady=5)

tk.Button(root, text="Detener", command=detener, bg="#DC3545", fg="white",
          font=("Arial", 14), width=10).pack(pady=5)

# Inicia automáticamente la lectura
obtener_datos()

# Ejecuta la interfaz
root.mainloop()