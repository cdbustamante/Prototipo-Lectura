from flask import Flask, render_template
from deepface import DeepFace
import cv2
import os  
from cors_config import configure_cors  # Importa la función de configuración CORS

app = Flask(__name__)
configure_cors(app)

base_path = "./static/Imagenes"  # Cambiado el directorio base para que incluya "Imagenes"
image_extension = ['.jpg', '.jpeg', '.png']  # Extensiones de imagen compatibles

@app.route('/')
def index():
    acumulado = 0
    images_to_display = []

    # Contar el número total de imágenes en la carpeta
    num_images = len([f for f in os.listdir(base_path) if f.lower().endswith(tuple(image_extension))])

    for i in range(1, num_images + 1):
        image_path = f"imagen_{i}.jpg"  # Corregido aquí, eliminado "Imagenes/"
        pat = "Imagenes/"

        # Cargar la imagen utilizando OpenCV
        img = cv2.imread(os.path.join(base_path, image_path))

        # Analizar la emoción en la imagen
        emotion_result = DeepFace.analyze(img_path=os.path.join(base_path, image_path), actions=['emotion'])

        # Obtener la emoción dominante
        dominant_emotion = emotion_result[0]['dominant_emotion']

        punctuacion = 0

        if dominant_emotion == "sad":
            punctuacion = 1
            acumulado += punctuacion
            img_pth= pat + image_path
            images_to_display.append(img_pth)

    final = (acumulado * 6) / num_images
    resul = round(final)

    return render_template('./frontend/src/App.js', images_to_display=images_to_display, final_score=resul)

if __name__ == '__main__':
    app.run(debug=True)
