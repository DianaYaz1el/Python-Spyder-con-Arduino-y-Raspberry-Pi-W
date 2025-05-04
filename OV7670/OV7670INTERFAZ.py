import os
import cv2
import time
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import tkinter as tk
from PIL import Image, ImageTk

# ------------------------------------
# 1) Depuración: listar archivos en Cel1 y Cel2
# ------------------------------------
ruta_frames = r"C:\Users\diana\OneDrive\Documentos\arduino-1.8.18\frames"

for clase in ["Cel1", "Cel2"]:
    carpeta = os.path.join(ruta_frames, clase)
    print(f"\n--- Clase {clase} ---")
    if os.path.exists(carpeta):
        archivos = [f for f in os.listdir(carpeta)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"Ruta encontrada: {carpeta}")
        print(f"Número de imágenes detectadas: {len(archivos)}")
        for nombre in archivos:
            print("  ", nombre)
    else:
        print(f"¡ERROR! No existe la carpeta: {carpeta}")

# ------------------------------------
# 2) Cargar, entrenar y evaluar el modelo
# ------------------------------------
clases = ["Cel1", "Cel2"]
X, y = [], []

for idx, clase in enumerate(clases):
    carpeta = os.path.join(ruta_frames, clase)
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(carpeta, archivo)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (64, 64))
            X.append(img.flatten())
            y.append(idx)

X = np.array(X)
y = np.array(y)
X, y = shuffle(X, y, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print("\n🔍 Reporte de clasificación:\n")
print(classification_report(y_test, y_pred, target_names=clases))

# ------------------------------------
# 3) Interfaz con Tkinter para cámara en vivo (con colores)
# ------------------------------------
def launch_live_classifier(model, classes):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️ No se pudo abrir la cámara.")
        return

    root = tk.Tk()
    root.title("Clasificador en Vivo")
    root.geometry("560x560")
    root.configure(bg="#e3f2fd")  # Fondo azul pastel claro
    root.resizable(False, False)

    # Video display
    video_label = tk.Label(root, bg="#e3f2fd")
    video_label.pack(pady=5)

    # Instrucciones/resultados
    info_label = tk.Label(
        root,
        text="📸 Presiona 'Capturar' (c)\n❌ Salir: 'Salir' (q)",
        font=("Helvetica", 11, "bold"),
        bg="#e3f2fd",
        fg="#0d47a1",
        justify="center"
    )
    info_label.pack(pady=10)

    # Botones
    btn_frame = tk.Frame(root, bg="#e3f2fd")
    btn_frame.pack(pady=5)

    def capture():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(gray, (64, 64))
            flat = small.flatten().reshape(1, -1)
            pred = model.predict(flat)[0]
            info_label.config(text=f"🧠 Clasificación: {classes[pred]}")

    def quit_app():
        cap.release()
        root.destroy()

    tk.Button(
        btn_frame, text="🎯 Capturar (c)", font=("Helvetica", 10, "bold"),
        bg="#64b5f6", fg="white", activebackground="#42a5f5",
        command=capture
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        btn_frame, text="🚪 Salir (q)", font=("Helvetica", 10, "bold"),
        bg="#ef5350", fg="white", activebackground="#e53935",
        command=quit_app
    ).grid(row=0, column=1, padx=10)

    root.bind('c', lambda e: capture())
    root.bind('q', lambda e: quit_app())

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame_small = cv2.resize(frame, (520, 440))
            cv2image = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)
        root.after(30, update_frame)

    update_frame()
    root.mainloop()

# Ejecutar la interfaz
launch_live_classifier(modelo, clases)

