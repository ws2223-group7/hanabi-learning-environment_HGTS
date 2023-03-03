# pylint: disable=missing-module-docstring, wrong-import-position, line-too-long, arguments-differ, unused-argument
import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.rl_env import Agent, HanabiEnv
from bad.bad_agent_acting_result import BadAgentActingResult
from bad.policy import Policy
from bad.encoding.observationconverter import ObservationConverter

class BadAgent(Agent):
    ''' bad agent '''
    def __init__(self, policy: Policy, hanabi_environment: HanabiEnv) -> None:
        self.policy = policy
        self.hanabi_environment = hanabi_environment
        self.observation_converter: ObservationConverter = ObservationConverter()

    def act(self, observation, public_belief=None) -> BadAgentActingResult:
        '''act'''
        legal_moves_as_int = self.hanabi_environment.state.legal_moves_int()
        bad = self.policy.get_action(self.observation_converter.convert(observation), legal_moves_as_int)
        action_result = bad.get_action(self.hanabi_environment.state.legal_moves_int())
        observation_after_step, reward, done, _ = self.hanabi_environment.step(action_result.sampled_action)
        return BadAgentActingResult(observation_after_step, done, int(reward))

    def reset(self, config):
        print('reset')
