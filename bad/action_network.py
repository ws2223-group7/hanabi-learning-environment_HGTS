# pylint: disable=missing-module-docstring, wrong-import-position, unused-variable, unused-argument, not-callable, invalid-name, fixme, unreachable
import sys
import os
import numpy as np
import tensorflow as tf

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.encoding.observation import Observation
from bad.bayesian_action import BayesianAction

class ActionNetwork():
    ''' action network '''

    def __init__(self) -> None:
        self.model = None

    def build(self, observation: Observation, max_action: int) -> None:
        '''build'''
        if self.model is None:
            shape = observation.to_array().shape
            self.model = tf.keras.Sequential([
                tf.keras.Input(shape=shape, name="input"),
                tf.keras.layers.Dense(384, activation="relu", name="layer1"),
                tf.keras.layers.Dense(384, activation="relu", name="layer2"),
                tf.keras.layers.Dense(max_action, activation='softmax', name='Output_Layer')
            ])
            opt = tf.keras.optimizers.Adam(learning_rate=0.01)
            self.model.compile(loss='categorical_crossentropy', optimizer=opt)

    def print_summary(self):
        '''print summary'''
        self.model.summary()

    def get_model_input(self, observation: Observation):
        '''get model input'''
        network_input = observation.to_array()
        reshaped = tf.reshape(network_input, [1, network_input.shape[0]])
        return reshaped

    def get_action(self, observation: Observation) -> BayesianAction:
        '''get action'''

        result = self.model(self.get_model_input(observation))
        return BayesianAction(result.numpy()[0])

    def backpropagation(self, x, y):
        '''train step'''
        model = self.model
        optimizer = self.model.optimizer
        loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        train_acc_metric =  tf.keras.metrics.CategoricalAccuracy()

        tf_x = self.get_model_input(x)

        arr_y = np.zeros(21, dtype = int)
        arr_y = np.append(arr_y, int(y))
        tf_y = tf.reshape(arr_y, [1, arr_y.shape[0]])

        with tf.GradientTape() as tape:
            logits = model(tf_x, training=True)
            loss_value = loss_fn(tf_y, logits)
        grads = tape.gradient(loss_value, model.trainable_weights)
        optimizer.apply_gradients(zip(grads, model.trainable_weights))
        train_acc_metric.update_state(tf_y, logits)
