from PIL import Image
import numpy as np
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('../model/distraction_meter_model.keras')

# Load and preprocess the saved screenshot
img = Image.open("last_monitor_frame.jpg").resize((224, 224)).convert('RGB')
img_array = np.array(img) / 255.0
input_tensor = np.expand_dims(img_array, axis=0)

# Predict using the model
pred = model.predict(input_tensor)[0][0]

# Interpret the prediction
print(f"Prediction confidence: {pred:.4f}")
if pred < 0.3:
    print("Class: non_short")
elif pred < 0.7:
    print("Class: reel")
else:
    print("Class: short")
