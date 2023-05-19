from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from PIL import Image

app = Flask(__name__)

# Load the trained image tagging model
model = load_model('model/image_tagging_model.h5')

# Define the route for the image tagging API endpoint
@app.route('/api/image_tagging', methods=['POST'])
def image_tagging():
    # Check if the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']

    # Read and preprocess the image
    image = Image.open(image_file)
    image = image.convert('RGB')
    image = image.resize((224, 224))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = tf.expand_dims(image, axis=0)

    # Perform image tagging using the loaded model
    predictions = model.predict(image)
    tags = ['tag1', 'tag2', 'tag3', 'tag4']  # Replace with your own tags

    # Get the predicted tags
    predicted_tags = [tags[i] for i, prob in enumerate(predictions[0]) if prob > 0.5]

    # Return the predicted tags as the API response
    return jsonify({'tags': predicted_tags}), 200

if __name__ == '__main__':
    app.run()
