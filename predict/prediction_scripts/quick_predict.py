import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from datetime import datetime, timezone

MODEL_DIR = '../../Predictions/'
SCALAR_DIR = '../../Predictions/Model1/complements/'
IMG_DIR = 'media/prediction_model1'

# model = tf.keras.models.load_model(MODEL_DIR + 'final_model.h5')
# stat_scaler = pickle.load(open(SCALAR_DIR + 'stats_scaler.pickle', 'rb'))
# like_scaler = pickle.load(open(SCALAR_DIR + 'likes_scaler.pickle', 'rb'))
# view_scaler = pickle.load(open(SCALAR_DIR + 'views_scaler.pickle', 'rb'))

def quick_predict_script(stats, img_url):
    img = Image.open(img_url)
    img = img.resize((150, 150))
    thumb = np.array(img, dtype=np.float32)/255
    img_to_predict = np.expand_dims(thumb, axis=0)
    img.close()

    input_stat = np.expand_dims(stats, axis=0)
    input_stat = stat_scaler.transform(input_stat)
    # print(img_to_predict.shape, input_stat.shape)
    # print(input_stat)

    ans = model.predict([img_to_predict, input_stat])
    # print(ans)
    view = view_scaler.inverse_transform(ans[0])
    like = like_scaler.inverse_transform(ans[1])
    # print(view, like)
    return [view, like]

# Views = ans[0][0][0], Likes = ans[1][0][0]