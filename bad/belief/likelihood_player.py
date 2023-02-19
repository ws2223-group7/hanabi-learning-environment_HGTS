# pylint: disable=missing-module-docstring, wrong-import-position, no-name-in-module, too-few-public-methods, too-many-instance-attributes, too-many-arguments

import sys
import os

from likelihood_hand_card import LikelihoodHandCard

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.action_network import ActionNetwork
from bad.encoding.observation import Observation


class LikelihoodPlayer(list):
    '''likelihoodplayer'''
    def __init__(self, constants, idx_ply: int, observation: Observation,
                  action_network: ActionNetwork, last_act, pub_belief, pre_hanabi_env):
        '''init'''
        self.idx_ply = idx_ply
        super().__init__(self.__init(constants, idx_ply, observation,
                                     action_network, last_act, pub_belief, pre_hanabi_env))

    def __init(self, constants, idx_ply, observation,
               action_network, last_act, pre_pub_belief, pre_hanabi_env) -> list:
        '''init'''
        likelihood_player = [LikelihoodHandCard(idx_ply, idx_card, constants, observation,
                              action_network, last_act, pre_pub_belief, pre_hanabi_env)
                              for idx_card in range(constants.num_cards) ]
        return likelihood_player
