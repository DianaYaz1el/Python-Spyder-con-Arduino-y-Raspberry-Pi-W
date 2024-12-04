import tkinter as tk
import requests

# Dirección IP de la Raspberry Pi Pico W
pico_ip = "192.168.0.xxx"  # Cambia según la IP de tu Pico W

# Función para enviar el ángulo al servidor
def mover_servo():
    angulo = entry_angulo.get()
    try:
        url = f"http://{pico_ip}/mover?angulo={angulo}"
        response = requests.get(url)
        if response.status_code == 200:
            resultado.set(f"Servo movido a {angulo}°")
        else:
            resultado.set(f"Error: {response.status_code}")
    except Exception as e:
        resultado.set(f"Error de conexión: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Servomotor - Raspberry Pi Pico W")
root.geometry("400x300")

# Título
titulo = tk.Label(root, text="Control de Servomotor", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

# Entrada de ángulo
frame = tk.Frame(root)
frame.pack(pady=20)
label_angulo = tk.Label(frame, text="Ángulo (0-180):", font=("Arial", 12))
label_angulo.pack(side=tk.LEFT)
entry_angulo = tk.Entry(frame, font=("Arial", 12), width=5)
entry_angulo.pack(side=tk.LEFT, padx=10)

# Botón para mover el servo
btn_mover = tk.Button(root, text="Mover Servo", font=("Arial", 14), command=mover_servo, bg="#008000", fg="white")
btn_mover.pack(pady=10)

# Resultado
resultado = tk.StringVar()
resultado_label = tk.Label(root, textvariable=resultado, font=("Arial", 12), fg="blue")
resultado_label.pack(pady=10)

# Ejecutar la interfaz
root.mainloop()
