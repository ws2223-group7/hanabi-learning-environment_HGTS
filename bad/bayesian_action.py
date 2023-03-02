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

    def sample_action(self, legal_moves:np.ndarray) -> BayesianActionResult:
        '''returns a choice'''
        legal_actions_int = legal_moves.tolist()
        all_action_probs = self.actions.copy()

        if len(legal_actions_int) == len(all_action_probs):
            raise Exception('no legal moves left')

        all_action_probs_distribution = tfp.distributions.Categorical(probs=all_action_probs)
        done = False
        while not done:
            sampled_action:int = int(all_action_probs_distribution.sample().numpy())
            done: bool = legal_actions_int.count(sampled_action) > 0

        return BayesianActionResult(sampled_action)

    def get_action(self, legal_moves:np.ndarray) -> BayesianActionResult:
        '''returns a choice'''
        legal_actions_int = legal_moves.tolist()
        all_action_probs = self.actions.copy()

        if len(legal_actions_int) == len(all_action_probs):
            raise Exception('no legal moves left')

        policy = tfp.distributions.Categorical(probs=all_action_probs)
        policy_as_numpy = policy.probs.numpy()
        done = False
        while not done:
            sampled_action:int = int(np.argmax(policy_as_numpy, axis=0))
            done: bool = legal_actions_int.count(sampled_action) > 0
            if not done:
                policy_as_numpy[sampled_action] = -float('inf')

        return BayesianActionResult(sampled_action)
