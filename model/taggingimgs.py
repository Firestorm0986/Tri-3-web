import os
import certifi
import requests
from io import BytesIO
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def fetch_image_data_from_api():
    # Make a request to the backend API to fetch image data
    response = requests.get('http://your-backend-api.com/images')

    # Assuming the API response contains a list of image URLs
    image_urls = response.json()['image_urls']

    # Fetch the images and return as a list of PIL Image objects
    images = []
    for image_url in image_urls:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        images.append(image)

    return images

def train_image_tagging_model():
    # Fetch images from the backend API
    images = fetch_image_data_from_api()

    # Set the tags for image labeling
    tags = ['tag1', 'tag2', 'tag3', 'tag4']  # Replace with your own tags

    # Define the parameters for training the model
    image_size = (224, 224)
    batch_size = 32
    num_epochs = 10

    # Create a data generator for training
    data_generator = ImageDataGenerator(rescale=1.0/255.0, validation_split=0.2)

    # Generate dummy labels since the backend API may not provide them
    labels = [0] * len(images)

    # Split the data into training and validation sets
    train_size = int(0.8 * len(images))
    train_images = images[:train_size]
    train_labels = labels[:train_size]
    validation_images = images[train_size:]
    validation_labels = labels[train_size:]

    # Convert the lists of images and labels to numpy arrays
    train_images = np.array(train_images)
    train_labels = np.array(train_labels)
    validation_images = np.array(validation_images)
    validation_labels = np.array(validation_labels)

    # Prepare the data generators using the image and label arrays
    train_generator = data_generator.flow(train_images, train_labels, target_size=image_size, batch_size=batch_size, subset='training')
    validation_generator = data_generator.flow(validation_images, validation_labels, target_size=image_size, batch_size=batch_size, subset='validation')

    # Set the SSL certificate file environment variable
    os.environ['SSL_CERT_FILE'] = certifi.where()

    # Load the pre-trained VGG16 model without the top classification layer
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(image_size[0], image_size[1], 3))

    # Add a global average pooling layer and a dense layer for classification
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(len(tags), activation='softmax')(x)

    # Create the model with the VGG16 base and the classification layers
    model = Model(inputs=base_model.input, outputs=predictions)

    # Freeze the weights of the pre-trained layers
    for layer in base_model.layers:
        layer.trainable = False

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(train_generator, epochs=num_epochs, validation_data=validation_generator)

    # Save the trained model
    model.save('model/image_tagging_model.h5')

def initTagging():
# Call the function to train the image tagging model when this file is executed
    train_image_tagging_model()
