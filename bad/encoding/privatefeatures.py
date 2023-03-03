# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods
import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.encoding.hands import Hands

class PrivateFeatures:
    '''private features'''
    def __init__(self, observation: dict) -> None:
        '''init'''
        self.observation = observation
        self.hands = self.convert_hands()

    def convert_hands(self) -> Hands:
        '''returns hands'''
        return Hands(self.observation)
