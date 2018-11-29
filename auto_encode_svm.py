import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.layers import fully_connected
from sklearn import svm

mnist = input_data.read_data_sets("./Mnist_data/", one_hot=False)

num_input = 784
num_hid1 = 392
num_hid2 = 196
num_hid3 = num_hid1
num_output = num_input
lr = 0.01
actf = tf.nn.relu

X = tf.placeholder(tf.float32,shape=[None,num_input])
initializer = tf.variance_scaling_initializer()

w1 = tf.Variable(initializer([num_input,num_hid1]),dtype=tf.float32)
w2 = tf.Variable(initializer([num_hid1,num_hid2]),dtype=tf.float32)
w3 = tf.Variable(initializer([num_hid2,num_hid3]),dtype=tf.float32)
w4 = tf.Variable(initializer([num_hid3,num_output]),dtype=tf.float32)

b1=tf.Variable(tf.zeros(num_hid1))
b2=tf.Variable(tf.zeros(num_hid2))
b3=tf.Variable(tf.zeros(num_hid3))
b4=tf.Variable(tf.zeros(num_output))

hide_layer1 = actf(tf.matmul(X,w1) + b1)
hide_layer2 = actf(tf.matmul(hide_layer1,w2) + b2)
hide_layer3 = actf(tf.matmul(hide_layer2,w3) + b3)
output_layer = actf(tf.matmul(hide_layer3,w4) + b4)

loss = tf.reduce_mean(tf.square(output_layer-X))

optimizer = tf.train.AdamOptimizer(lr)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

num_epochs = 5
batch_size = 150
num_test_img = 10


weight_svm = []
labels_svm = []


with tf.Session() as sess:
    sess.run(init)

    for epoch in range(num_epochs):
        num_batch_train = mnist.train.num_examples // batch_size

        for iteration in range(num_batch_train):
            X_batch, y_batch = mnist.train.next_batch(batch_size)
            sess.run(train,feed_dict={X:X_batch})


        train_loss = loss.eval(feed_dict={X:X_batch})
        print("epoch {} loss {} ".format(epoch,train_loss))


    for iteration in range(num_batch_train):
        X_batch, y_batch = mnist.train.next_batch(batch_size)
        r = sess.run(hide_layer2,feed_dict={X:X_batch})
        weight_svm.append(r)
        labels_svm.append(y_batch)


clf = svm.SVC(gamma='scale', decision_function_shape='ovo')
print(labels_svm[0])
for i in range(len(labels_svm)):

    clf.fit(weight_svm[i],labels_svm[i])

