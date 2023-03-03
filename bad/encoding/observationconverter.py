# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods
import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)

from bad.encoding.observation import Observation

class ObservationConverter:
    ''' converting hanabi observation to vector observation '''

    def convert(self, observation: dict) -> Observation:
        ''' one hot encoding '''
        return Observation(observation)
