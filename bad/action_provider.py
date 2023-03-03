# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, line-too-long, too-many-arguments, unused-variable, pointless-string-statement
from abc import ABC

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.bayesian_action import BayesianAction
from bad.encoding.observation import Observation


class ActionProvider(ABC):
    """action provider"""
    def get_action(self, observation: Observation, legal_moves_as_int: list, \
                   public_belief = None) -> BayesianAction:
        """get action"""
        raise NotImplementedError("Please Implement this method")
