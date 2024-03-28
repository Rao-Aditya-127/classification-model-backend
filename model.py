import tensorflow as tf
import json
import numpy as np
import sys

# Assuming you have already loaded your model and set img_height and img_width
model = tf.keras.models.load_model('D:\CODE\Fastapi\V_1_model.h5')
img_height, img_width = 256, 256  # Adjust according to your model's input size

new_path = sys.argv[1]
# Path to the image
# new_path = 'D:\\CODE\\Fastapi\\image\\9.png'

# Load and preprocess the image without resizing
img = tf.keras.utils.load_img(new_path, target_size=(img_height, img_width))
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create a batch

# Make predictions
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

# Display the top prediction
class_names = ['Chausa', 'Dasheri', 'Kesar', 'Langra', 'alphonso', 'totapuri']  # Replace with your actual class names
predicted_class = class_names[tf.argmax(score)]
confidence = 100 * tf.reduce_max(score)

print(f"Predicted class: {predicted_class}")
print(f"Confidence: {confidence:.2f}%")

result = {"prediction": predicted_class,
           "Confidence" : confidence.numpy().tolist(),
           "path" : new_path
        }
print(json.dumps(result))

