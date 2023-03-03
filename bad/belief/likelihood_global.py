# pylint: disable=missing-module-docstring, wrong-import-position, wrong-import-order, ungrouped-imports, too-few-public-methods, line-too-long, too-many-arguments

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.action_network import ActionNetwork
from bad.encoding.observation import Observation
from bad.belief.likelihood_player import LikelihoodPlayer

class Likelihood(list):
    '''likely hood'''
    def __init__(self, constants, action_network: ActionNetwork, pre_hanabi_env,
                pre_observation: Observation, last_act, pub_belief)-> None:
        """Initialize / Update the likelihood based on the last_action, observation and last_action network
        By initializing the likelihood, the first time last_act,old_likelihood and last_act are None
        

        Args:
            constants (HanabiEnv): Hanabi environment 
            act_network (ActionNetwork): Network that predicts the last_action
            last_act (int, None): the last action taken by the agent
            pre_observation (Observation): Observation from the previous step
            pub_belief (Likelihood, None): current public_belief
            pre_hint_matrix (HintMatrix, None): Hint matrix from the previous step
        Returns:
            likelihood (Likelihood): Likelihood of the current step
        """
        super().__init__(self.__init(constants, pre_observation,
                                     action_network, last_act, pub_belief, pre_hanabi_env))


    def __init(self, constants, observation: Observation,
                     action_network: ActionNetwork, last_act,
                     pub_belief, pre_hanabi_env) -> list:

        players_hands = [LikelihoodPlayer(constants, idx_ply, observation,
                         action_network, last_act, pub_belief, pre_hanabi_env)
                         for idx_ply in range(constants.num_ply)]

        return players_hands
