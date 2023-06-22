import tensorflow as tf
from tensorflow import keras
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import os


def formatarImagem(image):
    image = cv2.resize(image, (170, 170))
    image = image.reshape((1, 170, 170, 3,))
    image = tf.cast(image/255. ,tf.float32)

    return image


def prediction(imagem):
    request = requests.get(imagem)

    image = Image.open(fp=BytesIO(request.content))
    image = image.convert('RGB')

    arr_image = np.array(image)

    image = formatarImagem(arr_image)

    # Carregar modelo
    model = tf.keras.saving.load_model("modelpizzaornotpizza.h5")

    prediction = model.predict([image])
    if prediction[0].max() == prediction[0][1]:
        return "Isso é uma pizza"
    elif prediction[0].max() == prediction[0][0]:
        return "Isso não é uma pizza"
