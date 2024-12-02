import requests
import tkinter as tk
from tkinter import messagebox

# Dirección IP de la Raspberry Pi Pico W
# Cambia 'DIRECCION_PUBLICA_DEL_MODEM' por la dirección pública del módem de tu Raspberry Pi
pico_ip = '192.168.0.101'

# Función para encender el LED
def encender_led():
    try:
        url = f'http://{pico_ip}/ledon'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "LED encendido correctamente")
        else:
            messagebox.showerror("Error", f"Error al encender el LED: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor:\n{e}")

# Función para apagar el LED
def apagar_led():
    try:
        url = f'http://{pico_ip}/ledoff'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "LED apagado correctamente")
        else:
            messagebox.showerror("Error", f"Error al apagar el LED: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor:\n{e}")

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Control de LED con Raspberry Pi Pico W")

# Etiqueta principal
label = tk.Label(root, text="Control de LED", font=("Arial", 16))
label.pack(pady=10)

# Botón para encender el LED
btn_encender = tk.Button(root, text="Encender LED", command=encender_led, bg="green", fg="white", width=20)
btn_encender.pack(pady=5)

# Botón para apagar el LED
btn_apagar = tk.Button(root, text="Apagar LED", command=apagar_led, bg="red", fg="white", width=20)
btn_apagar.pack(pady=5)

# Ejecutar el ciclo principal de Tkinter
root.mainloop()
