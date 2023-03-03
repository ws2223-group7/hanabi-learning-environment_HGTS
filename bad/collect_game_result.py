# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods
import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.game_buffer import GameBuffer


class CollectGameResult:
    '''collect episode data result'''
    def __init__(self, buffer: GameBuffer) -> None:
        ''''init'''
        self.buffer = buffer
