from PIL import Image
import numpy as np
import os
from glob import glob
import tensorflow as tf

img_height = 100
img_width = 100

loaded_model = tf.keras.models.load_model('vgg_16.keras')

print(loaded_model.summary())

train_copy_path = r'C:\Users\andir\OneDrive\Documents\Fruit-Classification-Project\fruits-360_100x100\fruits-360\Training_copy'
train_classes = os.listdir(train_copy_path)
print(f"Classes in training data: {train_classes}")

className = glob(train_copy_path + '/*')
numberOfClass = len(className)
print("Number of Train Fruit Class: {}".format(numberOfClass))

def predict_fruit(image_path):
    try:
            # 1. Load the image
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(img_width, img_height))

            # 2. Convert the image to a numpy array
            img_array = tf.keras.preprocessing.image.img_to_array(img)

            # 3. Expand the dimensions to create a batch of size 1
            img_array = np.expand_dims(img_array, axis=0)

            # 4. Preprocess the image (important for models like VGG16)
            #img_array = tf.keras.applications.vgg16.preprocess_input(img_array)

            # 5. Make the prediction
            predictions = loaded_model.predict(img_array)

            # 6. Interpret the predictions
            # For a multi-class classification, the output is usually a probability distribution
            # across all classes. We find the index of the class with the highest probability.
            predicted_class_index = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class_index]
            predicted_class = train_classes[predicted_class_index]

            return predicted_class, confidence

    except Exception as e:
            return f"Error during prediction: {e}", None


if __name__ == '__main__':
    image_to_predict = r'C:\Users\andir\Downloads\s43_100.jpg'  # Replace with the path to the image you want to test
    predicted_fruit, confidence = predict_fruit(image_to_predict)

    if predicted_fruit:
        print(f"The predicted fruit is: {predicted_fruit} with a confidence of {confidence:.2f}")
    else:
        print(predicted_fruit) # Print the error message