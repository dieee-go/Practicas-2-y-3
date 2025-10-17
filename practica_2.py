import os
import cv2
import numpy as np

#--------- Entradas ---------
def seleccionar_imagen(x):
	nom_img2 = None
	image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg')

	# Obtener archivos
	image_files = [f for f in os.listdir('.') if f.lower().endswith(image_extensions)]
	# print(image_files)
	for i, filename in enumerate(image_files):
		print(f"{i+1}. {filename}")
		
	nom_img1 = int(input("Selecciona una imagen: ")) - 1
	if x > 0:
		nom_img2 = int(input("Selecciona otra imagen: ")) - 1

	# Leer imágenes en escala de grises
	img1 = cv2.imread(image_files[nom_img1], cv2.IMREAD_GRAYSCALE)
	if nom_img2 is not None:
		img2 = cv2.imread(image_files[nom_img2], cv2.IMREAD_GRAYSCALE)
		return img1, img2

	return img1

#--------- Tratamiento ---------

def tratamiento(img1, img2):
	# Asegurar que ambas imágenes tengan el mismo tamaño
	img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

	# Umbralización simple
	_, img_bin1 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)
	_, img_bin2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)

	return img2, img_bin1, img_bin2

#--------- Operaciones ---------

# Operaciones con un escalar
def aritmeticas_escalar (img, x, y, z):
	suma_escalar = cv2.add(img, x)           # Suma con escalar
	resta_escalar = cv2.subtract(img, y)     # Resta con escalar
	mult_escalar = cv2.multiply(img, z)       # Multiplicación con escalar

	return suma_escalar, resta_escalar, mult_escalar

# Operaciones entre imágenes
def aritmeticas_img (img1, img2):
	suma = cv2.add(img1, img2)
	resta = cv2.subtract(img1, img2)
	mult = cv2.multiply(img1, img2)
	return suma, resta, mult

# Operaciones lógicas
def logicas (img_bin1, img_bin2):
	and_img = cv2.bitwise_and(img_bin1, img_bin2)
	or_img = cv2.bitwise_or(img_bin1, img_bin2)
	not_img = cv2.bitwise_not(img_bin1)
	xor_img = cv2.bitwise_xor(img_bin1, img_bin2)
	return and_img, or_img, not_img, xor_img




opc = int(input("Operación? \n1. Aritméticas con escalar \n2. Aritméticas entre imágenes \n3. Lógicas \n4. Añadir ruido \n\nRespuesta: "))

match opc:
	case 1:
		img1 = seleccionar_imagen(0)
		x = int(input("Escalar para la suma: "))
		y = int(input("Escalar para la resta: "))
		z = int(input("Escalar para la multiplicación: "))
		suma_escalar, resta_escalar, mult_escalar = aritmeticas_escalar(img1, x, y, z) 
		_, img_bin1 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)

		cv2.imshow('Original', img1)
		cv2.imshow('Umbralizada', img_bin1)
		cv2.imshow('Suma', suma_escalar)
		cv2.imshow('Resta', resta_escalar)
		cv2.imshow('Multiplicacion', mult_escalar)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	case 2:
		img1, img2 = seleccionar_imagen (1)
		img2, img_bin1, img_bin2 = tratamiento(img1, img2)
		suma, resta, mult = aritmeticas_img (img1, img2)

		cv2.imshow('Original 1', img1)
		cv2.imshow('Original 2', img2)
		cv2.imshow('Umbralizada 1', img_bin1)
		cv2.imshow('Umbralizada 2', img_bin2)
		cv2.imshow('Suma', suma)
		cv2.imshow('Resta', resta)
		cv2.imshow('Multiplicacion', mult)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	case 3:
		img1, img2 = seleccionar_imagen (1)
		_, img_bin1, img_bin2 = tratamiento(img1, img2)
		and_img, or_img, not_img, xor_img = logicas (img_bin1, img_bin2)

		cv2.imshow('Original 1', img1)
		cv2.imshow('Original 2', img2)
		cv2.imshow('Umbralizada 1', img_bin1)
		cv2.imshow('Umbralizada 2', img_bin2)
		cv2.imshow('AND', and_img)
		cv2.imshow('OR', or_img)
		cv2.imshow('NOT', not_img)
		cv2.imshow('XOR', xor_img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	case 4:
		#--------- Ruido ---------
		img1 = seleccionar_imagen(0)
		porcentaje_ruido = (int(input("Porcentaje de ruido? [0 - 100] ")))/100			# Parámetro: porcentaje de ruido (entre 0 y 1)

		ruido = np.copy(img1)			# Crear una copia de la imagen

		total_pixeles = img1.size		# Número total de píxeles
		pix_ruido = int(total_pixeles * porcentaje_ruido)

		# Agregar ruido sal
		coords_sal = [np.random.randint(0, i - 1, pix_ruido // 2) for i in img1.shape]
		ruido[coords_sal[0], coords_sal[1]] = 255

		# Agregar ruido pimienta
		coords_pimienta = [np.random.randint(0, i - 1, pix_ruido // 2) for i in img1.shape]
		ruido[coords_pimienta[0], coords_pimienta[1]] = 0

		# Mostrar resultados
		cv2.imshow('Original', img1)
		cv2.imshow('Con ruido Sal y Pimienta', ruido)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	case _:
		print("Opción no válida")