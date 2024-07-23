import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests

# URL del modelo implementado en Azure
URL_MODELO = 'https://casopayles-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/b1bac1aa-52c1-4f02-ab07-801486c16a2a/classify/iterations/Custom%20vision%20Payles/image'
CLAVE_PREDICCION = '7c619906a4c04dab85133f2153e51acf'

def clasificar_imagen(ruta_imagen):
    with open(ruta_imagen, 'rb') as archivo_img:
        datos_img = archivo_img.read()
    headers = {
        'Prediction-Key': CLAVE_PREDICCION,
        'Content-Type': 'application/octet-stream'
    }
    try:
        respuesta = requests.post(URL_MODELO, headers=headers, data=datos_img)
        respuesta.raise_for_status()  # Esto lanzará una excepción si la solicitud no tuvo éxito
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar la imagen: {e}")
        return None


def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename()
    if ruta_archivo:
        resultado = clasificar_imagen(ruta_archivo)
        if resultado:
            # Procesar el resultado JSON
            predicciones = resultado.get('predictions', [])
            if predicciones:
                # Obtener la predicción con mayor probabilidad
                mejor_prediccion = max(predicciones, key=lambda x: x['probability'])
                texto_resultado = f"Predicción: {mejor_prediccion['tagName']} ({mejor_prediccion['probability']*100:.2f}%)"
            else:
                texto_resultado = "No se encontraron predicciones."
            etiqueta_resultado.config(text=texto_resultado, fg="blue", font=("Helvetica", 14, "bold"))
            
            # Mostrar la imagen cargada
            img = Image.open(ruta_archivo)
            img.thumbnail((250, 250))
            img = ImageTk.PhotoImage(img)
            etiqueta_imagen.config(image=img)
            etiqueta_imagen.image = img
        else:
            etiqueta_resultado.config(text="Error al clasificar la imagen.", fg="red", font=("Helvetica", 14, "bold"))

# Configuración de la ventana principal
root = tk.Tk()
root.title("Clasificación de Calzado - Payles")
root.geometry("500x700")
root.config(bg="#f0f0f0")

# Estilo para el botón
estilo_boton = {
    "bg": "#4CAF50",
    "fg": "white",
    "font": ("Helvetica", 12, "bold"),
    "relief": tk.RAISED,
    "bd": 3,
    "padx": 10,
    "pady": 5
}

# Título de la aplicación
titulo_app = tk.Label(root, text="Clasificación de Calzado - Payles", bg="#f0f0f0", font=("Helvetica", 16, "bold"))
titulo_app.pack(pady=10)

# Título para el botón de cargar imagen
titulo_cargar = tk.Label(root, text="Paso 1: Cargar Imagen", bg="#f0f0f0", font=("Helvetica", 14, "bold"))
titulo_cargar.pack(pady=10)

# Botón para cargar imagen
boton_cargar = tk.Button(root, text="Cargar Imagen", command=abrir_archivo, **estilo_boton)
boton_cargar.pack(pady=10)

# Etiqueta para mostrar la imagen cargada
etiqueta_imagen = tk.Label(root, bg="#f0f0f0")
etiqueta_imagen.pack(pady=20)

# Título para el resultado
titulo_resultado = tk.Label(root, text="Resultado de la Clasificación", bg="#f0f0f0", font=("Helvetica", 14, "bold"))
titulo_resultado.pack(pady=10)

# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(root, text="", bg="#f0f0f0", font=("Helvetica", 12))
etiqueta_resultado.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()






