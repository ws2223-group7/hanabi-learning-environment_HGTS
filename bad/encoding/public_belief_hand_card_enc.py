# pylint: disable=missing-module-docstring, wrong-import-position, unused-variable, unused-argument, not-callable, invalid-name, too-few-public-methods

import sys
import os
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.belief.public_belief_hand_card import PublicBelfHandCard
from bad.encoding.card_probabilitiy import CardProbabilitiy

class PublicBeliefHandCardEnc():
    '''PublicBeliefHandCardEnc'''
    def __init__(self, public_belf_hand_card: PublicBelfHandCard):
        '''init'''
        colors = ['B', 'G', 'R', 'W', 'Y']
        max_rank = 5

        self.pro_hand_card = np.empty(0,int)

        for color in colors:
            for rank in range(max_rank):
                num_rem_cards: int = public_belf_hand_card[color][rank]
                self.pro_hand_card = np.append(self.pro_hand_card,
                    CardProbabilitiy([color],[num_rem_cards]))
