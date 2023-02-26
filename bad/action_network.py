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

    def __init__(self, path) -> None:
        self.model = None
        self.path = path
        self.optimizer = tf.keras.optimizers.Adam()

    def load(self, ) -> None:
        """load"""
        self.model = tf.keras.models.load_model(self.path)

    def save(self):
        """save"""
        self.model.save(self.path)

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
            self.model.compile(loss='categorical_crossentropy', optimizer=self.optimizer)

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

    def backpropagation(self, observation: Observation, rewards_to_go: float, loss):
        '''train step'''
        model = self.model

        with tf.GradientTape() as tape:
            logits = model(self.get_model_input(observation))
            log_probs = tf.nn.log_softmax(logits, -1)
            loss = -(tf.reduce_mean(log_probs * rewards_to_go))
            print(f'current loss {loss}')

        grads = tape.gradient(loss, model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, model.trainable_variables))
