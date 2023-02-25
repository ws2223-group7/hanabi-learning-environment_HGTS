# pylint: disable=missing-module-docstring too-few-public-methods, pointless-string-statement,wrong-import-position, fixme, broad-exception-raised
import sys
import os

import numpy as np
import tensorflow_probability as tfp

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.bayesian_action_result import BayesianActionResult


class BayesianAction:
    '''Bayesian Action'''
    def __init__(self, actions: np.ndarray) -> None:
        self.actions = actions

    def decode_action(self) -> BayesianActionResult:
        '''returns a choice'''
        all_action_probs = self.actions.copy()

        policy = tfp.distributions.Categorical(probs=all_action_probs)
        sampled_action:int = int(policy.sample().numpy())

        return BayesianActionResult(sampled_action, policy)
