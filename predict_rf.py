import traceback
import numpy as np
import scipy as sp
import tensorflow as tf
import time
import picamera
from AMSpi import AMSpi

image_height = 240 // 10
image_width = 320 // 10
image_channels = 3
pixel_depth = 255

MODEL_META_FILE = 'model_1layernn_1024.ckpt.meta'
classes = ['F', 'L', 'R']

def extract_params(sess):
    W1 = sess.graph.get_tensor_by_name("weights1:0")
    b1 = sess.graph.get_tensor_by_name("bias1:0")
    W2 = sess.graph.get_tensor_by_name("weights2:0")
    b2 = sess.graph.get_tensor_by_name("bias2:0")
    return (W1, b1, W2, b2)

def predict(sess, x, W1, b1, W2, b2):
    index = sess.run(tf.nn.softmax(tf.matmul(tf.nn.relu(tf.matmul(x, W1) + b1), W2) + b2)).argmax()
    return classes[index]

def preprocess(imgage):
    return ((sp.misc.imresize(image, (image_height,image_width)) - pixel_depth / 2) / pixel_depth).astype(np.float32).reshape(1, -1)

if __name__ == '__main__':
    saver = tf.train.import_meta_graph(MODEL_META_FILE)
    with AMSpi() as amspi, tf.Session() as sess, picamera.PiCamera() as camera:
        amspi.set_74HC595_pins(21, 20, 16)
        amspi.set_L293D_pins(5, 6, 13, 19)

        saver.restore(sess, tf.train.latest_checkpoint('./'))
        W1, b1, W2, b2 = extract_params(sess)

        camera.resolution = (320, 240)
        camera.framerate = 10

        while True:
            try:
                image = np.empty((320, 240, image_channels), dtype=np.uint8)
                camera.capture(image, 'rgb')

                image = preprocess(image)
                cmd = predict(sess, image, W1, b1, W2, b2)
                
                if cmd == 'F':
                    # FORWARD
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=False)
                    time.sleep(.1)
                elif cmd == 'B':
                    # BACKWARD
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=True)
                elif cmd == 'L':
                    # LEFT
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=False)
                elif cmd == 'R':
                    # RIGHT
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=True)
                time.sleep(.1)
            except:
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                print(traceback.format_exc())
                break