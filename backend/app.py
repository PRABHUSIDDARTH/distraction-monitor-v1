from flask import Flask, request, jsonify, send_from_directory
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import base64
import io
import mss
import threading
import time
from datetime import datetime

last_checked_time = "Never"

app = Flask(__name__, static_folder='../frontend')

# Load the trained model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/distraction_meter_model.keras'))
model = tf.keras.models.load_model(model_path)

# Globals
shorts_viewed = 0
threshold = 0
monitoring_active = False  # Start as paused
monitor_interval = 5  # seconds between checks



@app.route('/set_interval', methods=['POST'])
def set_interval():
    global monitor_interval
    interval = request.form.get('interval', type=int)
    if interval and interval >= 1:
        monitor_interval = interval
        return jsonify({'message': f'Interval set to {monitor_interval} seconds'}), 200
    return jsonify({'error': 'Invalid interval'}), 400

class_names = ['non_short', 'reel', 'short']


# ------------------ Utility Functions ------------------

def preprocess_image(image_data):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)


def monitor_loop():
    global monitoring_active, shorts_viewed
    global last_checked_time
    last_checked_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    while monitoring_active:
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary screen
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                img.save("last_monitor_frame.jpg")  # Optional debug

                # Preprocess
                img = img.resize((224, 224))
                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                preds = model.predict(img_array)[0]
                pred_class = np.argmax(preds)
                pred_label = class_names[pred_class]

                if pred_label in ['reel', 'short']:
                    shorts_viewed += 1
                    print(f"🔴 {pred_label} detected — Counter: {shorts_viewed}")
                else:
                    print("✅ Non-short content detected.")

        except Exception as e:
            print(f"❌ Monitoring error: {e}")

        time.sleep(monitor_interval)


# ------------------ Routes ------------------

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory(app.static_folder, 'style.css')

@app.route('/script.js')
def js():
    return send_from_directory(app.static_folder, 'script.js')


@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    global threshold, shorts_viewed, monitoring_active
    threshold = int(request.form.get('threshold', 0))
    shorts_viewed = 0
    monitoring_active = False
    return jsonify({'message': f'Threshold set to {threshold}'}), 200


@app.route('/start_monitoring', methods=['GET'])
def start_monitoring():
    global monitoring_active

    if monitoring_active:
        return jsonify({"message": "Already monitoring", "shorts_viewed": shorts_viewed}), 200

    monitoring_active = True
    threading.Thread(target=monitor_loop, daemon=True).start()

    return jsonify({
        "message": "✅ Monitoring started",
        "shorts_viewed": shorts_viewed
    }), 200


@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    return jsonify({'message': '🛑 Monitoring stopped'}), 200


@app.route('/reset', methods=['POST'])
def reset_all():
    global shorts_viewed, monitoring_active
    shorts_viewed = 0
    monitoring_active = False
    return jsonify({'message': '🔄 System reset'}), 200


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        image_data = base64.b64decode(data['image'])
        processed_image = preprocess_image(image_data)
        preds = model.predict(processed_image)[0]
        pred_class = np.argmax(preds)

        return jsonify({
            'prediction': class_names[pred_class],
            'confidence': float(preds[pred_class])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/shorts_count', methods=['GET'])
def get_shorts_count():
    global shorts_viewed
    return jsonify({'shorts_viewed': shorts_viewed}), 200



if __name__ == '__main__':
    app.run(debug=True)
