# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, no-method-argument, unnecessary-pass, consider-using-enumerate, too-many-function-args, too-many-arguments

import os
import sys

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)


from bad.belief.public_belief_hand_card import PublicBelfHandCard
from bad.belief.ftpubvec import RemaingCards
from bad.belief.hint_matrix_player import HintMatrixPlayer
from bad.belief.likelihood_player import LikelihoodPlayer


class PublicBeliefPlayer(list):
    '''public belief'''
    def __init__(self, constants, idx_ply: int, rem_cards: RemaingCards,
                 hint_matrix_ply: HintMatrixPlayer, likelihood_ply: LikelihoodPlayer):
        '''init'''
        self.idx_ply = idx_ply
        super().__init__(self.init(constants, rem_cards,
                                   hint_matrix_ply, likelihood_ply))

    def init(self, constants, rem_cards: RemaingCards,
             hint_matrix_ply: HintMatrixPlayer,
             likelihood_ply: LikelihoodPlayer) -> list:
        '''init'''

        public_belief_hand_cards = [PublicBelfHandCard(constants, self.idx_ply, idx_card,
                                rem_cards, hint_matrix_ply[idx_card],
                                likelihood_ply[idx_card])
                                for idx_card in range(constants.num_ply)]
        return public_belief_hand_cards
        