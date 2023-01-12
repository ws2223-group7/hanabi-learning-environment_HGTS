import unittest
import os
import sys

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)


from INFO_Strategy.htgs_info_agent import HTGSAgent

from hanabi_learning_environment import rl_env

class TestHTGSAgent(unittest.TestCase):        

    def setUp(self) -> None:
        self.observation = self.set_observations()
        self.agent = self.set_agent() 

    def set_observations(self):
        
        observed_hand_0 = [{'color': None, 'rank': -1}, 
                           {'color': None, 'rank': -1}, 
                           {'color': None, 'rank': -1}, 
                           {'color': None, 'rank': -1}]

        observed_hand_1 = [{'color': 'R', 'rank': 1}, 
                           {'color': 'G', 'rank': 1}, 
                           {'color': 'G', 'rank': 1}, 
                           {'color': 'Y', 'rank': 2}]

        observed_hand_2 = [{'color': 'G', 'rank': 2}, 
                           {'color': 'W', 'rank': 3}, 
                           {'color': 'Y', 'rank': 0}, 
                           {'color': 'B', 'rank': 2}]

        observed_hand_3 = [{'color': 'R', 'rank': 3},
                           {'color': 'Y', 'rank': 1},
                           {'color': 'G', 'rank': 0},
                           {'color': 'B', 'rank': 3}]

        observed_hand_4 = [{'color': 'Y', 'rank': 1},
                           {'color': 'B', 'rank': 0},
                           {'color': 'B', 'rank': 0},
                           {'color': 'R', 'rank': 4}] 
        
        card_knowledge_hand = [{'color': None, 'rank': None}, 
                               {'color': None, 'rank': None}, 
                               {'color': None, 'rank': None}, 
                               {'color': None, 'rank': None}]

        
        observations = {
                        'current_player': 0, 
                        'current_player_offset': 0, 
                        'life_tokens': 3, 
                        'information_tokens': 8, 
                        'num_players': 5, 
                        'deck_size': 30, 
                        'fireworks': {'R': 0, 'Y': 0, 'G': 0, 'W': 0, 'B': 0}, 
                        'legal_moves': [], 
                        'legal_moves_as_int': [], 
                        'observed_hands': [observed_hand_0, 
                                           observed_hand_1, 
                                           observed_hand_2, 
                                           observed_hand_3, 
                                           observed_hand_4], 
                        'discard_pile': [], 
                        'card_knowledge': [card_knowledge_hand.copy(), 
                                           card_knowledge_hand.copy(), 
                                           card_knowledge_hand.copy(), 
                                           card_knowledge_hand.copy(), 
                                           card_knowledge_hand.copy()], 
                        }

        return observations
    
    def set_agent(self):
        agent = HTGSAgent({'players': 5})
                                 
        
        agent.init_table(self.observation)
        agent.update_observation(self.observation)
        
        return agent
    
    def test_duplicate_card_in_hand(self):
        """1. Testcase: card_idx = 3 duplicate"""
        # Init 

        
        
        # Von der eigenen Hand ist die vierte Karte bekannt
        # Es ist eine Gelbe mit Rank 2
        self.agent.table[0][3] = {'B': [0, 0, 0, 0, 0], 
                            'G': [0, 0, 0, 0, 0], 
                            'R': [0, 0, 0, 0, 0], 
                            'W': [0, 0, 0, 0, 0], 
                            'Y': [0, 0, 1, 0, 0]}

        self.agent.observation['observed_hands'][1][0] = {'color': 'Y', 'rank': 2} 
        poss_hand_table = self.agent.table[0]

        self.assertTrue(self.agent.duplicate_card_in_hand(poss_hand_table)
                        == {'color': 'Y', 'rank': 2})

        
    
