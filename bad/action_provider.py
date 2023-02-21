# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, line-too-long, too-many-arguments, unused-variable, pointless-string-statement
from abc import ABC

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.bayesian_action import BayesianAction
from bad.encoding.observation import Observation
from bad.encoding.public_belief_global_enc import PublicBeliefGlobalEnc


class ActionProvider(ABC):
    """action provider"""
    def get_action(self, observation: Observation, \
                   public_belief: PublicBeliefGlobalEnc = None) -> BayesianAction:
        """get action"""
        raise NotImplementedError("Please Implement this method")
