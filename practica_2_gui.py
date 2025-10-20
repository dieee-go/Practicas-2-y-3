import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from scipy import ndimage
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Configurar apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana principal
root = ctk.CTk()
root.title("Procesamiento de Imágenes - Práctica 2")
root.geometry("1100x700")

# Variables globales
img1 = None
img2 = None
panel_original = None
panel_resultado = None

# Funciones auxiliares
def cargar_imagen(num):
    global img1, img2
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp *.tiff")])
    if not ruta:
        return
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    if num == 1:
        img1 = imagen
        mostrar_imagen(imagen, panel_original)
    else:
        img2 = imagen
        mostrar_imagen(imagen, panel_resultado)

def mostrar_imagen(img, panel):
    """Convierte una imagen OpenCV a formato Tkinter y la muestra"""
    if img is None:
        return
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    im = Image.fromarray(img_rgb)
    im = im.resize((400, 300))
    imgtk = ImageTk.PhotoImage(im)
    panel.configure(image=imgtk)
    panel.image = imgtk

def ejecutar_operacion():
    global img1, img2
    if img1 is None:
        messagebox.showerror("Error", "Cargue al menos una imagen.")
        return

    opcion = combo_operacion.get()

    if opcion == "Aritméticas con escalar":
        try:
            x = int(entry_x.get())
            y = int(entry_y.get())
            z = int(entry_z.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
            return

        suma = cv2.add(img1, x)
        resta = cv2.subtract(img1, y)
        mult = cv2.multiply(img1, z)
        resultado = np.hstack((suma, resta, mult))
        mostrar_imagen(resultado, panel_resultado)

    elif opcion == "Aritméticas entre imágenes":
        if img2 is None:
            messagebox.showerror("Error", "Cargue la segunda imagen.")
            return
        img2_rz = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        suma = cv2.add(img1, img2_rz)
        resta = cv2.subtract(img1, img2_rz)
        mult = cv2.multiply(img1, img2_rz)
        resultado = np.hstack((suma, resta, mult))
        mostrar_imagen(resultado, panel_resultado)

    elif opcion == "Lógicas":
        if img2 is None:
            messagebox.showerror("Error", "Cargue la segunda imagen.")
            return
        _, bin1 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)
        _, bin2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)
        and_img = cv2.bitwise_and(bin1, bin2)
        or_img = cv2.bitwise_or(bin1, bin2)
        xor_img = cv2.bitwise_xor(bin1, bin2)
        resultado = np.hstack((and_img, or_img, xor_img))
        mostrar_imagen(resultado, panel_resultado)

    elif opcion == "Ruido Sal y Pimienta":
        try:
            porc = int(entry_x.get()) / 100
        except ValueError:
            messagebox.showerror("Error", "Ingrese un porcentaje válido.")
            return
        ruido = np.copy(img1)
        total_pix = img1.size
        pix_ruido = int(total_pix * porc)
        coords_sal = [np.random.randint(0, i - 1, pix_ruido // 2) for i in img1.shape]
        coords_pimienta = [np.random.randint(0, i - 1, pix_ruido // 2) for i in img1.shape]
        ruido[coords_sal[0], coords_sal[1]] = 255
        ruido[coords_pimienta[0], coords_pimienta[1]] = 0
        mostrar_imagen(ruido, panel_resultado)

    elif opcion == "Etiquetado de componentes":
        # Verificar si hay imagen cargada
        if img1 is None:
            messagebox.showerror("Error", "Cargue una imagen para etiquetar.")
            return

        # Convertir a binaria
        _, imagen_binaria = cv2.threshold(img1, 127, 1, cv2.THRESH_BINARY)

        # Definir vecindades
        vecindad_4 = np.array([
            [0,1,0],
            [1,1,1],
            [0,1,0]
        ], dtype=int)
        vecindad_8 = np.ones((3,3), dtype=int)

        # Etiquetado
        etiquetas_4, num_objetos_4 = ndimage.label(imagen_binaria, structure=vecindad_4)
        etiquetas_8, num_objetos_8 = ndimage.label(imagen_binaria, structure=vecindad_8)

        # Mostrar resultados con Matplotlib
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))

        axes[0].imshow(imagen_binaria, cmap='gray')
        axes[0].set_title("Imagen Binaria")
        axes[0].axis('off')

        axes[1].imshow(etiquetas_4, cmap='nipy_spectral')
        axes[1].set_title(f"Vecindad 4 - {num_objetos_4} objetos")
        axes[1].axis('off')

        axes[2].imshow(etiquetas_8, cmap='nipy_spectral')
        axes[2].set_title(f"Vecindad 8 - {num_objetos_8} objetos")
        axes[2].axis('off')

        plt.tight_layout()
        plt.show()


# Widgets principales
frame_izq = ctk.CTkFrame(root)
frame_izq.pack(side="left", fill="y", padx=10, pady=10)

label_op = ctk.CTkLabel(frame_izq, text="Seleccione operación:")
label_op.pack(pady=5)
combo_operacion = ctk.CTkComboBox(frame_izq, values=[
    "Aritméticas con escalar",
    "Aritméticas entre imágenes",
    "Lógicas",
    "Ruido Sal y Pimienta",
    "Etiquetado de componentes"
])
combo_operacion.pack(pady=5)

combo_operacion.set("Seleccionar...")

# ---- Entradas dinámicas según operación ----
label_x = ctk.CTkLabel(frame_izq, text="Parámetro X:")
entry_x = ctk.CTkEntry(frame_izq)
label_y = ctk.CTkLabel(frame_izq, text="Parámetro Y:")
entry_y = ctk.CTkEntry(frame_izq)
label_z = ctk.CTkLabel(frame_izq, text="Parámetro Z:")
entry_z = ctk.CTkEntry(frame_izq)

# ---- Botones de carga ----
btn_cargar1 = ctk.CTkButton(frame_izq, text="Cargar Imagen 1", command=lambda: cargar_imagen(1))
btn_cargar2 = ctk.CTkButton(frame_izq, text="Cargar Imagen 2", command=lambda: cargar_imagen(2))

# ---- Función para actualizar parámetros y botones ----
def actualizar_parametros(event=None):
    opcion = combo_operacion.get()

    # Ocultar todo primero
    for w in [label_x, entry_x, label_y, entry_y, label_z, entry_z, btn_cargar1, btn_cargar2]:
        w.pack_forget()

    # Reiniciar textos por defecto
    btn_cargar1.configure(text="Cargar Imagen 1")
    btn_cargar2.configure(text="Cargar Imagen 2")

    # Mostrar y configurar según la opción
    if opcion == "Aritméticas con escalar":
        label_x.configure(text="Escalar para Suma:")
        label_y.configure(text="Escalar para Resta:")
        label_z.configure(text="Escalar para Multiplicación:")

        label_x.pack(pady=3); entry_x.pack(pady=3)
        label_y.pack(pady=3); entry_y.pack(pady=3)
        label_z.pack(pady=3); entry_z.pack(pady=3)
        btn_cargar1.pack(pady=5)

    elif opcion == "Aritméticas entre imágenes":
        btn_cargar1.configure(text="Cargar Imagen 1 (A)")
        btn_cargar2.configure(text="Cargar Imagen 2 (B)")
        btn_cargar1.pack(pady=5)
        btn_cargar2.pack(pady=5)

    elif opcion == "Lógicas":
        btn_cargar1.configure(text="Cargar Imagen 1 (Binaria A)")
        btn_cargar2.configure(text="Cargar Imagen 2 (Binaria B)")
        btn_cargar1.pack(pady=5)
        btn_cargar2.pack(pady=5)

    elif opcion == "Ruido Sal y Pimienta":
        label_x.configure(text="Porcentaje de ruido (0–100):")
        label_x.pack(pady=3); entry_x.pack(pady=3)
        btn_cargar1.configure(text="Cargar Imagen")
        btn_cargar1.pack(pady=5)

    elif opcion == "Etiquetado de componentes":
        btn_cargar1.configure(text="Cargar Imagen para Etiquetar")
        btn_cargar1.pack(pady=5)

# Asociar el cambio del combo con la función
combo_operacion.configure(command=actualizar_parametros)

# Llamar una vez para iniciar sin mostrar nada
actualizar_parametros()

btn_cargar1 = ctk.CTkButton(frame_izq, text="Cargar Imagen 1", command=lambda: cargar_imagen(1))
btn_cargar1.pack(pady=5)

btn_cargar2 = ctk.CTkButton(frame_izq, text="Cargar Imagen 2", command=lambda: cargar_imagen(2))
btn_cargar2.pack(pady=5)

btn_ejecutar = ctk.CTkButton(frame_izq, text="Ejecutar", command=ejecutar_operacion)
btn_ejecutar.pack(pady=10)

# Paneles de visualización
frame_imgs = ctk.CTkFrame(root)
frame_imgs.pack(side="right", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(frame_imgs, text="Imagen / Resultado").pack()
panel_original = ctk.CTkLabel(frame_imgs, text="")
panel_original.pack(pady=5)
panel_resultado = ctk.CTkLabel(frame_imgs, text="")
panel_resultado.pack(pady=5)

root.mainloop()
