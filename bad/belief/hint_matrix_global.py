# pylint: disable=missing-module-docstring, wrong-import-position, wrong-import-order, ungrouped-imports, too-few-public-methods, line-too-long, too-many-arguments, unused-variable, no-value-for-parameter

import os
import sys


currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.belief.hint_matrix_player import HintMatrixPlayer
from bad.belief.ftpubvec import RemaingCards
from bad.belief.build_hanabi_env import get_hanabi_env



class HintMatrix(list):
    '''hint matrix'''
    def __init__(self, constants, rem_cards: RemaingCards):
        '''init'''
        super().__init__(self.__init(constants, rem_cards))


    def __init(self, constants, rem_cards: RemaingCards) -> list:
        '''init'''
        players_hands = [HintMatrixPlayer(constants, idx_ply,
                         rem_cards) for idx_ply in range(constants.num_ply)]

        return players_hands

def main():
    '''main'''
    hanabi_env = get_hanabi_env()
    observation = hanabi_env['player_observations']
    rem_cards = RemaingCards(hanabi_env)
    hint_matrix = HintMatrix(observation, rem_cards)
    print()

if __name__ == "__main__":
    main()
