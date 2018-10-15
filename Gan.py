import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.gridspec as gridspec

mnist = input_data.read_data_sets('MNIST_data',one_hot=True)

def model_input(width,height,channel,z_dim):
    
    input_real = tf.placeholder(tf.float32,(None,width,height),name='input_real')

    input_z    = tf.placeholder(tf.float32,(None,z_dim),name="input_z")

    learning_rate = tf.placeholder(tf.float32,name='learning_rate')

    return input_real,input_z,learning_rate


def discriminator(images,reuse=False):

    with tf.variable_scope('discriminator',reuse=reuse):
        
        alpha = 0.2

        layer1 = tf.reshape(images,[-1,28,28,1])
        layer1 = tf.layers.conv2d(layer1,64,5,strides=2,padding='same')
        relu1  = tf.maximum(alpha*layer1,layer1)

        layer2 = tf.layers.conv2d(relu1,128,5,strides=1,padding='same')
        bn2    = tf.layers.batch_normalization(layer2,training=True)
        relu2  = tf.maximum(alpha*bn2,bn2)

        layer3 = tf.layers.conv2d(relu2, 256, 5, strides=2, padding='same')
        bn3    = tf.layers.batch_normalization(layer3,training=True)
        relu3  = tf.maximum(alpha*bn3,bn3)

        flat   = tf.reshape(relu3,(-1,7*7*256))
        logits = tf.layers.dense(flat,1)
        out    = tf.sigmoid(logits)


        return out, logits


def generator(z,channel_dim,is_train=True):
    with tf.variable_scope('generator',reuse= not is_train):
        alpha = 0.2

        layer1 = tf.layers.dense(z,7*7*256)


        layer1 = tf.reshape(layer1,(-1,7,7,256))
        layer1 = tf.layers.batch_normalization(layer1,training = is_train)
        layer1 = tf.maximum(alpha*layer1,layer1)

        layer2 = tf.layers.conv2d_transpose(layer1,128,5,strides=1,padding='same')
        layer2 = tf.layers.batch_normalization(layer2,training=is_train)
        layer2 = tf.maximum(alpha*layer2,layer2)

        layer3 = tf.layers.conv2d_transpose(layer2,64,5,strides=2,padding='same')
        layer3 = tf.layers.batch_normalization(layer3,training=is_train)
        layer3 = tf.maximum(alpha*layer3,layer3)

        logits = tf.layers.conv2d_transpose(layer3,channel_dim,5,strides=2,padding='same')

        out = tf.sigmoid(logits)

        return out


def model_loss(input_real,input_z,channel_dim):

    smooth = 0.1
    g_model = generator(input_z,channel_dim,is_train=True)
    d_model_real, d_logits_real = discriminator(input_real)
    d_model_fake, d_logits_fake = discriminator(g_model,reuse=True)

    d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_real,labels=tf.ones_like(d_model_real)*(1-smooth)))
    d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_fake,labels=tf.zeros_like(d_model_fake)))
    d_loss      = d_loss_real + d_loss_fake

    g_loss      = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=d_logits_fake,labels=tf.ones_like(d_model_fake)))

    return d_loss, g_loss

def model_opt(d_loss,g_loss,learning_rate,beta1):
    
    t_vars = tf.trainable_variables()
    d_vars = [var for var in t_vars if var.name.startswith('discriminator')]
    g_vars = [var for var in t_vars if var.name.startswith('generator')]


    with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):

        d_train_opt = tf.train.AdamOptimizer(learning_rate=learning_rate,beta1=beta1).minimize(d_loss)
        g_train_opt = tf.train.AdamOptimizer(learning_rate=learning_rate,beta1=beta1).minimize(g_loss)

        return d_train_opt, g_train_opt

def plote(samples):

    fig = plt.figure(figsize=(4,4))
    gs = gridspec.GridSpec(4,4)
    gs.update(wspace=0.05,hspace=0.05)
    samples = samples.reshape(16,784)
    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28,28),cmap='gray')
    
    return fig

def train(epoch_count,batch_size,z_dim,learning_rate,beta1):
        
        i = 0
        input_real, input_z, lr = model_input(28,28,1,z_dim)

        d_loss, g_loss = model_loss(input_real,input_z,1)

        d_train_opt, g_train_opt = model_opt(d_loss,g_loss,lr,beta1)

        d_loss_graph = []
        g_loss_graph = []

        with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                
                for e in range(epoch_count):

                        x_mb = batch = [np.reshape(b,[28,28]) for b in mnist.train.next_batch(batch_size=batch_size)[0]]
                        z_sample = np.random.uniform(-1,1,size=(batch_size,z_dim))


                        _ = sess.run(d_train_opt,feed_dict={input_real:x_mb,input_z:z_sample,lr:learning_rate})

                        _ = sess.run(g_train_opt,feed_dict={input_real:x_mb,input_z:z_sample,lr:learning_rate})


                        if e%10==0:
                                i+=1
                                
                                d_train_loss = d_loss.eval({input_real:x_mb,input_z:z_sample})
                                d_loss_graph.append(d_train_loss)
                                
                                g_train_loss = g_loss.eval({input_z:z_sample})
                                g_loss_graph.append(g_train_loss)
                                
                        if e%10==0:
                                z_dim = input_z.get_shape().as_list()[-1]
                                z_noise = np.random.uniform(-1,1,size=[16,z_dim])
                                samples = sess.run(generator(input_z,1,False),feed_dict={input_z:z_noise})
                                fig = plote(samples)
                                plt.savefig('{}.png'.format(str(e).zfill(3)),bbox_inches='tight')
                                i+=1
                                plt.close(fig)


if __name__=='__main__':
        batch_size = 32
        z_dim = 16
        learning_rate = 0.0002
        beta1 = 0.5
        n_images = 25
        epochs = 10000
        with tf.Graph().as_default():
                train(epochs,batch_size,z_dim,learning_rate,beta1)
