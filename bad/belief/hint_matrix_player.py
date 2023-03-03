# pylint: disable=missing-module-docstring, wrong-import-position, wrong-import-order, ungrouped-imports, too-few-public-methods, line-too-long, too-many-arguments, no-value-for-parameter

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.belief.ftpubvec import RemaingCards
from bad.belief.hint_matrix_hand_card import HintMatrixHandCard


class HintMatrixPlayer(list):
    '''hint matrix player'''
    def __init__(self, constants, idx_ply: int, rem_cards: RemaingCards):
        self.idx_ply = idx_ply
        super().__init__(self.__init(constants, rem_cards))

    def __init(self, constants, rem_cards: RemaingCards) -> list:
        hint_matrix_player = [HintMatrixHandCard(constants, idx_card, rem_cards)
                              for idx_card in range(constants.num_ply)]
        return hint_matrix_player
