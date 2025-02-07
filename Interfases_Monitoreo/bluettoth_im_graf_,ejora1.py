import sys
import serial
import threading
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Label, Button, filedialog, Frame, Canvas
from PIL import Image, ImageTk
from datetime import datetime

# Configuración del puerto COM del HC-06
puerto = "COM11"  # Cambia al puerto correcto
baudrate = 9600

# Variables globales
ser = None
datos_recolectados = []  # Lista para guardar los datos (voltaje, corriente, potencia)
recolectando = False  # Bandera para detener el hilo de recolección
voltajes = []
corrientes = []
potencias = []
tiempos = []
gif_frames_inicio = []
gif_frames_detencion = []


def cargar_gif(ruta_gif, resize_width=150, resize_height=150):
    """Cargar un GIF animado desde una ruta específica y redimensionarlo."""
    frames = []
    gif = Image.open(ruta_gif)
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.copy().resize((resize_width, resize_height), Image.Resampling.LANCZOS)
        frame_image = ImageTk.PhotoImage(frame_image)
        frames.append(frame_image)
    return frames


def iniciar_conexion():
    global ser, recolectando

    if recolectando:
        return  # Si ya está recolectando datos, no hace nada

    try:
        # Conectar al HC-06
        ser = serial.Serial(puerto, baudrate, timeout=1)
        status_label.config(text="Conectado al MPPT", fg="#1C6DD0")
        recolectando = True
        threading.Thread(target=recolectar_datos, daemon=True).start()  # Iniciar hilo
        actualizar_grafica()  # Iniciar actualización de la gráfica

        # Mostrar los GIFs de inicio
        gif_label_izquierda.place(x=10, y=20)
        gif_label_derecha.place(x=ventana.winfo_width() - 170, y=20)
        mostrar_gif(gif_frames_inicio, 0, gif_label_izquierda)
        mostrar_gif(gif_frames_inicio, 0, gif_label_derecha)

    except serial.SerialException as e:
        status_label.config(text=f"Error al conectar: {e}", fg="red")


def mostrar_gif(frames, frame, gif_label):
    """Reproducir un GIF animado frame por frame."""
    if recolectando and frames == gif_frames_inicio:
        gif_label.config(image=frames[frame])
        ventana.after(100, mostrar_gif, frames, (frame + 1) % len(frames), gif_label)
    elif not recolectando and frames == gif_frames_detencion:
        gif_label.config(image=frames[frame])
        ventana.after(100, mostrar_gif, frames, (frame + 1) % len(frames), gif_label)


def detener_conexion():
    global recolectando, ser

    if not recolectando:
        return  # Si ya está detenido, no hace nada

    recolectando = False
    if ser:
        ser.close()
    status_label.config(text="Conexión detenida.", fg="red")

    # Mostrar los GIFs de detención
    gif_label_izquierda.place(x=10, y=20)
    gif_label_derecha.place(x=ventana.winfo_width() - 170, y=20)
    mostrar_gif(gif_frames_detencion, 0, gif_label_izquierda)
    mostrar_gif(gif_frames_detencion, 0, gif_label_derecha)


def recolectar_datos():
    global ser, datos_recolectados, voltajes, corrientes, potencias, tiempos

    while recolectando:
        try:
            linea = ser.readline().decode("utf-8").strip()

            if linea:
                datos = linea.split(",")
                if len(datos) == 2:
                    try:
                        voltaje = float(datos[0])
                        corriente = float(datos[1])
                        potencia = voltaje * corriente

                        timestamp = datetime.now().strftime("%H:%M:%S")
                        datos_recolectados.append({"Fecha y Hora": timestamp, 
                                                   "Voltaje (V)": voltaje, 
                                                   "Corriente (A)": corriente, 
                                                   "Potencia (W)": potencia})

                        # Actualizar listas para graficar
                        voltajes.append(voltaje)
                        corrientes.append(corriente)
                        potencias.append(potencia)
                        tiempos.append(timestamp)

                        # Actualizar etiquetas
                        voltaje_label.config(text=f"{voltaje:.2f} V")
                        corriente_label.config(text=f"{corriente:.2f} A")
                        potencia_label.config(text=f"{potencia:.2f} W")
                    except ValueError:
                        status_label.config(text="Error al convertir datos.", fg="red")
        except Exception as e:
            status_label.config(text=f"Error durante la lectura: {e}", fg="red")


def guardar_excel():
    if datos_recolectados:
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel Files", "*.xlsx")])
        if archivo:
            df = pd.DataFrame(datos_recolectados)
            df.to_excel(archivo, index=False)
            status_label.config(text=f"Datos guardados en {archivo}", fg="#1C6DD0")
    else:
        status_label.config(text="No hay datos para guardar.", fg="red")


def actualizar_grafica():
    if recolectando:
        ax.clear()
        ax.plot(tiempos, voltajes, label="Voltaje (V)", color="#1C6DD0")
        ax.plot(tiempos, corrientes, label="Corriente (A)", color="#FF5733")
        ax.plot(tiempos, potencias, label="Potencia (W)", color="#2ECC71")
        ax.legend()
        ax.set_title("Gráfica en Tiempo Real")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Mediciones")
        canvas.draw()
        ventana.after(1000, actualizar_grafica)


# Configuración de la ventana de Tkinter
ventana = Tk()
ventana.title("Sistema de Monitoreo del MPPT")
ventana.geometry("1200x800")
ventana.configure(bg="#EAF6FF")

# Rutas de los GIFs
ruta_gif_inicio = r"C:\\Users\\diana\\Pyton_microcontroladores\\ImagenesInterfaces\\psan.gif"
ruta_gif_detencion = r"C:\\Users\\diana\\Pyton_microcontroladores\\ImagenesInterfaces\\psan27.gif"

# Cargar los GIFs y redimensionarlos
gif_frames_inicio = cargar_gif(ruta_gif_inicio, resize_width=150, resize_height=150)
gif_frames_detencion = cargar_gif(ruta_gif_detencion, resize_width=150, resize_height=150)

# Título principal
Label(ventana, text="Sistema de Monitoreo del MPPT", font=("Arial Rounded MT Bold", 24), bg="#EAF6FF", fg="#1C6DD0").pack(pady=10)

# Estado
status_label = Label(ventana, text="Estado: Desconectado", fg="red", font=("Arial", 14), bg="#EAF6FF")
status_label.pack(pady=10)

# Rectángulo detrás de los datos
canvas_rect = Canvas(ventana, width=800, height=150, bg="#EAF6FF", highlightthickness=0)
canvas_rect.pack(pady=10)
canvas_rect.create_rectangle(20, 20, 780, 130, fill="#D6EAF8", outline="#1C6DD0", width=2)

# Contenedor de datos dentro del rectángulo
frame_datos = Frame(canvas_rect, bg="#D6EAF8")
frame_datos.place(x=250, y=30)  # Ajustar posición para centrar

# Cuadro de voltaje
voltaje_frame = Label(frame_datos, text="Voltaje:", font=("Arial", 20), bg="#FFFFFF", width=15, height=2, relief="ridge")
voltaje_frame.grid(row=0, column=0, padx=20, pady=10)
voltaje_label = Label(voltaje_frame, text="-", font=("Arial", 20), bg="#FFFFFF")
voltaje_label.pack()
voltaje_text = Label(frame_datos, text="Voltaje (V)", font=("Arial", 12), bg="#D6EAF8", fg="#1C6DD0")
voltaje_text.grid(row=1, column=0, pady=(0, 10))  # Etiqueta debajo del cuadro

# Cuadro de corriente
corriente_frame = Label(frame_datos, text="Corriente:", font=("Arial", 20), bg="#FFFFFF", width=15, height=2, relief="ridge")
corriente_frame.grid(row=0, column=1, padx=20, pady=10)
corriente_label = Label(corriente_frame, text="-", font=("Arial", 20), bg="#FFFFFF")
corriente_label.pack()
corriente_text = Label(frame_datos, text="Corriente (A)", font=("Arial", 12), bg="#D6EAF8", fg="#1C6DD0")
corriente_text.grid(row=1, column=1, pady=(0, 10))  # Etiqueta debajo del cuadro

# Cuadro de potencia
potencia_frame = Label(frame_datos, text="Potencia:", font=("Arial", 20), bg="#FFFFFF", width=15, height=2, relief="ridge")
potencia_frame.grid(row=0, column=2, padx=20, pady=10)
potencia_label = Label(potencia_frame, text="-", font=("Arial", 20), bg="#FFFFFF")
potencia_label.pack()
potencia_text = Label(frame_datos, text="Potencia (W)", font=("Arial", 12), bg="#D6EAF8", fg="#1C6DD0")
potencia_text.grid(row=1, column=2, pady=(0, 10))  # Etiqueta debajo del cuadro

# Botones
Button(ventana, text="Iniciar Monitoreo", command=iniciar_conexion, bg="#1C6DD0", fg="#FFFFFF", font=("Arial", 14), width=20).pack(pady=10)
Button(ventana, text="Detener Monitoreo", command=detener_conexion, bg="#FF5733", fg="#FFFFFF", font=("Arial", 14), width=20).pack(pady=10)
Button(ventana, text="Exportar Datos a Excel", command=guardar_excel, bg="#2ECC71", fg="#FFFFFF", font=("Arial", 14), width=20).pack(pady=10)

# Gráfica
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(pady=20)

# Labels para mostrar los GIFs
gif_label_izquierda = Label(ventana, bg="#EAF6FF")
gif_label_derecha = Label(ventana, bg="#EAF6FF")

# Iniciar loop de la interfaz
ventana.mainloop()
