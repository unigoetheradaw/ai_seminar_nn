"""Data-Types: This file contains the code for the new data-types.
These will be used to create the neural network later on.

How to:
In the main function, first, the data from test_data.txt is retrived,
and the input as well as the output is put into np ndarray form
Afterwards you can construct a nn using the explanation provided.
with network_robert a constructor is called which builds the nn.
In the following for loop the input data is put in and that output is
compared to the target output. at the end the overall costs of this nn is shown.

to do:
apply sgd
apply backprob
celebrate

Please note, that in the console printed version the weight and bias
values are rounded by default. Internally they are stored as 16bit float.
we can certainly expand to 32 or 64 bit or even 128.
"""

__author__ = "Niels #1, Niels #2"
__copyright__ = "Copyright 2017/2018 – EPR-Goethe-Uni"
__credits__ = "If you would like to thank somebody \
              i.e. an other student for her code or leave it out"
__email__ = ""

import numpy as np
import network_class
import random
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
import skimage.measure
import time
import datetime
import threading


class Main():
    def __init__(self):
        self.time_stamp = str(datetime.datetime.now()).replace(' ', '_').replace(':', '')[:-7]
        self.training_images = []
        self.training_labels = []
        self.main()



    def main(self):
        mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


# ----- MAX POOLING OF IMAGES (2,2) ------
        for img in mnist.train.images:
            self.training_images.append(np.matrix(skimage.measure.block_reduce(np.matrix(img).reshape((28,28)), (2,2), np.max)).flatten().transpose())

        for lab in mnist.train.labels:
            self.training_labels.append(np.matrix(lab).transpose())

# # ----- SHOW IMAGES OF NUMBERS ------
#
#         test1 = np.array(mnist.train.images[986]).reshape((28,28))
#         test1_down = self.training_images[986].reshape(14, 14)
#
#         print(self.training_labels[986])
#         img = plt.imshow(test1)
#         plt.show()
#         img = plt.imshow(test1_down)
#         plt.show()

        self.params = self.read_params('start_weights_for_test.txt')

# ------ Starting Threads ----------
#         t1 = threading.Thread(target=self.training_single)
#         t2 = threading.Thread(target=self.training_batch)
#         t3 = threading.Thread(target=self.training_rand)
#
#         t1.start()
#         t2.start()
#         t3.start()

        test_images = []
        test_labels = []

        parameters = self.read_params('weigths_after_test_2_2018-07-06_030533.txt')

        for img in mnist.test.images:
            test_images.append(np.matrix(skimage.measure.block_reduce(np.matrix(img).reshape((28,28)), (2,2), np.max)).flatten().transpose())

        for lab in mnist.test.labels:
            test_labels.append(np.matrix(lab).transpose())


        mnist_net = network_class.Network([(196), (150), (10)],  weights=parameters[1], bias=parameters[2], activation_function="sigmoid", initilizer="predefined", dropout=0.0)


        error1 = 0
        error2 = 0
        for i in range(10000):
            x = mnist_net.test(test_images[i])
            first = np.argmax(x)
            seccond = np.argmax(np.delete(x, first))
            if seccond >= first:
                seccond += 1
            y = np.argmax(test_labels[i])

            if first != y:
                error1 += 1
                if seccond != y:
                    error2 += 1
                    print("Error")
                    print(x)
                    print(first, seccond)
                    print(y)
                    img = plt.imshow(test_images[i].reshape(14, 14))
                    plt.show()


        print(error1/10000)
        print(error2/10000)


    def read_params(self, file_name):
        with open(file_name, 'r') as params:
            rows = params.read().split('\n')
            layer_infos = eval(rows[0])
            wei = []
            bia = []
            for i in range(len(layer_infos) - 1):
                wei.append(np.matrix(eval(str(rows[i + 1]))))
            for i in range(len(layer_infos) - 1):
                bia.append(np.matrix(eval(str(rows[i + len(layer_infos)]))))

            return (layer_infos, wei, bia)

    def write_time(self, start, end, start_time):
        title = 'times_for_mnist_net_' + self.time_stamp + '.txt'
        with open(title, 'a') as f:
            f.write('Time Differrence: ' + str(end - start) + '\n')
            f.write('TIME of Start' + str(start_time).replace(' ', '_').replace(':', '')[:-7] + '\n')

    def training_batch(self):
        start1 = datetime.datetime.now()
        start_time = datetime.datetime.now()

        mnist_net_batch = network_class.Network([(196), (150), (10)],  weights=self.params[1], bias=self.params[2], activation_function="sigmoid", initilizer="predefined", dropout=0.0)

        for i in range(1000):
            sample = random.sample(range(len(self.training_images)), 60)
            images = []
            labels = []
            for m in range(len(sample)):
                x = self.training_images[sample[m]]
                y = self.training_labels[sample[m]]
                images.append(x)
                labels.append(y)
            mnist_net_batch.train_batch(images, labels)

        mnist_net_batch.save_params('weigths_after_test_2')

        end1 = datetime.datetime.now()
        self.write_time(start1, end1, start_time)

    def training_rand(self):
        start2 = time.time()
        start_time = datetime.datetime.now()

        mnist_net_rand = network_class.Network([(196), (150), (10)],  weights=self.params[1], bias=self.params[2], activation_function="sigmoid", initilizer="predefined", dropout=0.0)

        for i in range(80000):
            ind = random.randint(0, len(self.training_images))
            x = self.training_images[ind]
            y = self.training_labels[ind]
            mnist_net_rand.test_train_single(x, y)

        mnist_net_rand.save_params('weigths_after_test_3')

        end2 = time.time()
        self.write_time(start2, end2, start_time)

    def training_single(self):
        start3 = datetime.datetime.now()
        start_time = datetime.datetime.now()

        mnist_net_single = network_class.Network([(196), (150), (10)],  weights=self.params[1], bias=self.params[2], activation_function="sigmoid", initilizer="predefined", dropout=0.0)

        for ind in range(len(self.training_images)):
            x = self.training_images[ind]
            y = self.training_labels[ind]
            mnist_net_single.test_train_single(x, y)

        mnist_net_single.save_params('weights_after_test_1')

        end3 = datetime.datetime.now()
        self.write_time(start3, end3, start_time)




if __name__ == "__main__":
    Main()
