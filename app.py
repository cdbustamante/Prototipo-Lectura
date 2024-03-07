from flask import Flask, render_template, Response, redirect, url_for, send_from_directory
from deepface import DeepFace
import cv2
import threading
import os
from flask_cors import CORS # Importa la función de configuración CORS
from flask import jsonify
import shutil

app = Flask(__name__)
CORS(app)

base_path = "./static/Imagenes"  # Cambiado el directorio base para que incluya "Imagenes"
image_extension = ['.jpg', '.jpeg', '.png']  # Extensiones de imagen compatibles
output_folder = "static/imagenes"
recording = False
video_capture = None

def record_video():
    global video_capture, recording
    recording = True
    video_writer = None
    frame_count = 0
    imagen_count = 1

    while recording:
        ret, frame = video_capture.read()

        if ret:
            frame_count += 1

            if frame_count % 12 == 0:
                if video_writer is None:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    output_filename = f"{output_folder}/output.mp4"
                    video_writer = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

                video_writer.write(frame)

                img_filename = f"{output_folder}/imagen_{imagen_count}.jpg"
                cv2.imwrite(img_filename, frame)
                imagen_count += 1

    recording = False
    if video_writer is not None:
        video_writer.release()

def generate_frames():
    global video_capture, recording

    while True:
        if video_capture is not None:
            ret, frame = video_capture.read()

            if ret:
                if recording:
                    cv2.putText(frame, "Grabando...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    ret, buffer = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    frame = buffer.tobytes()

                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                else:
                    break

@app.route('/run_deep_face_script', methods=['POST'])
def run_deep_face_script_route():
    global recording
    recording = False  # Detener la grabación antes de analizar las emociones

    # Analizar las emociones en las imágenes capturadas
    acumulado = 0
    images_to_display = []

    # Contar el número total de imágenes en la carpeta
    num_images = len([f for f in os.listdir(base_path) if f.lower().endswith(tuple(image_extension))])

    for i in range(1, num_images + 1):
        image_path = f"imagen_{i}.jpg"
        pat = "Imagenes/"

        # Cargar la imagen utilizando OpenCV
        img = cv2.imread(os.path.join(base_path, image_path))

        # Analizar la emoción en la imagen
        try:
            emotion_result = DeepFace.analyze(img_path=os.path.join(base_path, image_path), actions=['emotion'], enforce_detection=False)
            dominant_emotion = emotion_result[0]['dominant_emotion']
        except:
            dominant_emotion = None

        punctuacion = 0

        if dominant_emotion == "sad":
            punctuacion = 1
            img_pth = pat + image_path
            images_to_display.append(img_pth)
            
        acumulado += punctuacion   

    final = (acumulado * 6) / num_images
    resul = round(final) 

    return jsonify(images_to_display=images_to_display, final_score=resul)


@app.route('/')
def index():
    return render_template('./frontend/src/App.js')

def start_capture():
    global video_capture
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FPS, 20)

def stop_capture():
    global video_capture
    video_capture.release()

@app.route('/start_recording', methods=['POST'])
def start_recording():
    clean_output_folder()
    clean_template_images_folder()
    if not recording:
        capture_thread = threading.Thread(target=record_video)
        capture_thread.start()
    return "Recording started"

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording
    copy_images_to_template_folder()
    recording = False

    return "Recording stopped"

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('./static/', path)

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def clean_output_folder():
    folder_path = os.path.join(os.getcwd(), output_folder)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"No se pudo borrar {file_path}. Razón: {e}")

def clean_template_images_folder():
    destination_folder = os.path.join(os.getcwd(), 'templates/Imagenes')

    try:
        if os.path.exists(destination_folder):
            for file_name in os.listdir(destination_folder):
                file_path = os.path.join(destination_folder, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"No se pudo borrar {file_path}. Razón: {e}")

            print(f'Todos los archivos eliminados de {destination_folder}')
    except Exception as e:
        print(f'Error al eliminar archivos: {e}')

def copy_images_to_template_folder():
    source_folder = os.path.join(os.getcwd(), output_folder)
    destination_folder = os.path.join(os.getcwd(), 'templates/Imagenes')

    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file_name in os.listdir(source_folder):
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            shutil.copy2(source_file_path, destination_file_path)

        print(f'Todas las imágenes copiadas de {source_folder} a {destination_folder}')
    except Exception as e:
        print(f'Error al copiar imágenes: {e}')



if __name__ == '__main__':
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    start_capture()
    app.run(host='0.0.0.0', debug=True, threaded=True)

    # Detener la captura cuando la aplicación Flask se cierra
    stop_capture()
