import imageio
import numpy as np
import scipy as sp
import tensorflow as tf

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

def read_image(image_file_path):
	return imageio.imread(image_file_path)

if __name__ == '__main__':
	saver = tf.train.import_meta_graph(MODEL_META_FILE)
	with tf.Session() as sess:
		saver.restore(sess, tf.train.latest_checkpoint('./'))
		W1, b1, W2, b2 = extract_params(sess)
		image = read_image("testdata/R/018a6f1a1f4844359aca0ed92337fd87.jpg")
		image = preprocess(image)
		print(predict(sess, image, W1, b1, W2, b2))
