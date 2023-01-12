from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent

import unittest
import sys
import os
import getopt

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from INFO_Strategy.htgs_info_agent import HTGSAgent
from INFO_Strategy.possibility_table import Table

class TestHTGSAgent(unittest.TestCase):
    def __init__(self) -> None:
        self.observations = None
        self.agents = None 


    def set_observations(self):
           
        environment = rl_env.make('Hanabi-Full', num_players=5)
        observations = environment.reset()
         

        self.observations = observations
    
    def set_agents(self):
        self.agents = [HTGSAgent({'players': 5}) \
                                 for _ in range (5)] 
                                 
        for agent_idx, agent in enumerate (self.agents):
            agent.init_table(self.observations['player_observations'][agent_idx])
            agent.update_observation(self.observations['player_observations'][agent_idx])

    def set_table(self):
        self.table = Table(self.observation)    

    def test_duplicate_card_in_hand(self):
        """1. Testcase: card_idx = 3 duplicate"""
        # Init 
        self.set_observations()
        self.set_agents()
        agent = self.agents[0]
        
    

        # Von der eigenen Hand ist die vierte Karte bekannt
        # Es ist eine Gelbe mit Rank 2
        agent.table[0][3] = {'B': [0, 0, 0, 0, 0], 
                             'G': [0, 0, 0, 0, 0], 
                             'R': [0, 0, 0, 0, 0], 
                             'W': [0, 0, 0, 0, 0], 
                             'Y': [0, 0, 1, 0, 0]}

        agent.observation['observed_hands'][1][0] = {'color': 'Y', 'rank': 2} 
        poss_hand_table = agent.table[0]

        self.assertTrue(agent.duplicate_card_in_hand(poss_hand_table)
                        == {'color': 'Y', 'rank': 2})


if __name__ == "__main__":
    testClass = TestHTGSAgent()
    testClass.test_duplicate_card_in_hand()

                