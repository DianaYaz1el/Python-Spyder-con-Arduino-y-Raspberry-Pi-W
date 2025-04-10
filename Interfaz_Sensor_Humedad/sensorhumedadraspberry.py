import tkinter as tk
from PIL import Image, ImageTk
import requests
import pandas as pd
from datetime import datetime
from tkinter import filedialog

# Dirección IP de la Raspberry Pi Pico W
pico_ip = "192.168.x.xxx"

# Variables globales
leyendo = True
lecturas = []  # Lista para guardar las lecturas

# Función para obtener datos
def obtener_datos():
    global leyendo, lecturas
    if leyendo:
        try:
            response = requests.get(f"http://{pico_ip}/sensor", timeout=2)
            if response.status_code == 200:
                datos = response.json()
                temperatura = datos["temp"]
                humedad = max(0, datos["hum"] - 5)  # Ajuste opcional

                # Mostrar en pantalla
                temp_label.config(text=f"{temperatura:.1f} °C", fg="red")
                hum_label.config(text=f"{humedad:.1f} %", fg="blue")
                error_label.config(text="")

                # Guardar lectura
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lecturas.append({
                    "Fecha y hora": timestamp,
                    "Temperatura (°C)": temperatura,
                    "Humedad (%)": humedad
                })

            else:
                error_label.config(text="Error al recibir datos", fg="orange")
        except Exception:
            error_label.config(text="Formato incorrecto o sin conexión", fg="orange")

        root.after(2000, obtener_datos)

# Botón: iniciar
def iniciar():
    global leyendo
    if not leyendo:
        leyendo = True
        error_label.config(text="Reanudando lectura...", fg="green")
        obtener_datos()

# Botón: detener
def detener():
    global leyendo
    leyendo = False
    error_label.config(text="Lectura detenida", fg="red")

# Botón: exportar a Excel
def exportar_excel():
    if not lecturas:
        error_label.config(text="No hay datos para exportar", fg="orange")
        return

    archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                           filetypes=[("Excel files", "*.xlsx")])
    if archivo:
        df = pd.DataFrame(lecturas)
        df.to_excel(archivo, index=False)
        error_label.config(text="Datos exportados correctamente", fg="green")

# Interfaz
root = tk.Tk()
root.title("Sensor DHT - Raspberry Pi Pico W")
root.geometry("400x650")
root.configure(bg="#DDF2FF")

# Título
tk.Label(root, text="Sensor DHT - Raspberry Pi Pico W", font=("Arial", 16, "bold"),
         bg="#DDF2FF", fg="#0B5ED7").pack(pady=10)

# Imagen decorativa
ruta_sensor = r"C:\Users\diana\Pyton_microcontroladores\ImagenesInterfaces\humed.gif"
imagen = Image.open(ruta_sensor).resize((200, 200))
imagen_tk = ImageTk.PhotoImage(imagen)
tk.Label(root, image=imagen_tk, bg="#DDF2FF").pack(pady=10)

# Temperatura
tk.Label(root, text="Temperatura:", font=("Arial", 14), bg="#DDF2FF").pack()
temp_label = tk.Label(root, text="- °C", font=("Arial", 20), bg="white", width=10)
temp_label.pack(pady=5)

# Humedad
tk.Label(root, text="Humedad:", font=("Arial", 14), bg="#DDF2FF").pack()
hum_label = tk.Label(root, text="- %", font=("Arial", 20), bg="white", width=10)
hum_label.pack(pady=5)

# Mensaje de estado
error_label = tk.Label(root, text="Lectura detenida", font=("Arial", 10),
                       bg="#DDF2FF", fg="red")
error_label.pack(pady=10)

# Botones
tk.Button(root, text="Iniciar", command=iniciar, bg="#0B5ED7", fg="white",
          font=("Arial", 14), width=15).pack(pady=5)

tk.Button(root, text="Detener", command=detener, bg="#DC3545", fg="white",
          font=("Arial", 14), width=15).pack(pady=5)

tk.Button(root, text="Exportar a Excel", command=exportar_excel, bg="#28A745", fg="white",
          font=("Arial", 14), width=15).pack(pady=10)

# Inicia automáticamente
obtener_datos()

# Ejecutar interfaz
root.mainloop()
