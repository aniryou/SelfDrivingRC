import time
import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from sklearn.externals import joblib as jbl

image_height = 240 // 10
image_width = 320 // 10
pixel_depth = 255.

classes = ['F', 'L', 'R']

def preprocess(image):
    img_gray = np.dot(image, [0.299, 0.587, 0.114])
    img_small = sp.misc.imresize(img_gray, (image_height, image_width))
    img_norm = (img_small - pixel_depth/2) / pixel_depth
    img_ravel = img_norm.reshape(1, -1)
    plt.imsave("pred_images/img_{0}.jpeg".format(time.time()), img_ravel.reshape(24, 32))
    return img_ravel


model = jbl.load('models/model_pca_rf.jbl')


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

client_socket = server_socket.accept()[0]
connection = client_socket.makefile('rb')

try:
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        image = Image.open(image_stream)
        image = preprocess(image)
        pred = model.predict(image)
        client_socket.send(classes[pred])
finally:
    connection.close()
    server_socket.close()