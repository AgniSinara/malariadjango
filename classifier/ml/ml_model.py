import numpy as np
import os
import matplotlib.pyplot as plt
import malaria.settings as settings
from skimage.transform import resize

import requests
from io import BytesIO
import urllib.request
import urllib3


import tensorflow.keras as keras



# MODEL_PATH = os.path.join(settings.BASE_DIR, 'classifier/ml/malaria.h5')
# classes = ['Parasitized', 'Uninfected']
#
# # Load your trained model
# malaria_model = keras.models.load_model(MODEL_PATH)
# print(MODEL_PATH)
# malaria_model._make_predict_function()
#
#
# def model_predict(img_path):
#     # img = image.load_img(img_path, target_size=(64, 64))
#     img = plt.imread(img_path)
#     img = resize(img, (64, 64, 3))
#     img = img[np.newaxis, :]
#
#     # Preprocessing the image
#     # x = image.img_to_array(img)
#     # x = np.true_divide(x, 255)
#     # x = np.expand_dims(x, axis=0)
#
#     # Be careful how your trained model deals with the input
#     # otherwise, it won't make correct prediction!
#     # x = preprocess_input(x, mode='caffe')
#
#     preds = malaria_model.predict(img)
#     # preds = 1
#     print(preds)
#     return preds


# h = model_predict(os.path.join(settings.BASE_DIR, 'media/uploads/aryka.jpg'))
# print(h)

def model_predict(img_url):
    with urllib.request.urlopen(img_url) as response:
        img_raw = response
        img = plt.imread(img_raw)
        img = resize(img, (64, 64, 3))
        img = img[np.newaxis, :]
        # preds = malaria_model.predict(img)



def img_dl(img_url):
    response = requests.get(img_url)
    print(response.content)
    fp = BytesIO()

    fp.write(response.content)

    return fp
