import unittest
import os
import sys

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)


from INFO_Strategy.htgs_info_agent import HTGSAgent

from hanabi_learning_environment import rl_env

class TestHTGSAgent(unittest.TestCase):        



    def set_observation(self):
        
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

        
        observation = {
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

        return observation
    
    def set_agent(self,observation):
        agent = HTGSAgent({'players': 5})
                                 
        
        agent.init_table(observation)
        agent.update_observation(observation)
        
        return agent
    
    def test_duplicate_card_in_hand(self):
        """1. Testcase: card_idx = 3 duplicate"""
        # Init 
        observation = self.set_observation()
        agent = self.set_agent(observation)

        
        
        # Von der eigenen Hand ist die dritte Karte bekannt
        # Es ist eine Gelbe mit Rank 2
        agent.table[0][3] = {'B': [0, 0, 0, 0, 0], 
                            'G': [0, 0, 0, 0, 0], 
                            'R': [0, 0, 0, 0, 0], 
                            'W': [0, 0, 0, 0, 0], 
                            'Y': [0, 0, 1, 0, 0]}

        agent.observation['observed_hands'][1][0] = {'color': 'Y', 'rank': 2} 
        poss_hand_table = agent.table[0]

        self.assertTrue(agent.duplicate_card_in_hand(poss_hand_table)
                        == 3)

    def test_update_mc_based_on_firework(self):
        """"""
        # Init 
        observation = self.set_observation()
        agent = self.set_agent(observation)

        
        observation['fireworks'] = {'R': 4, 'Y': 3, 'G': 2, 'W': 1, 'B': 0}
        agent.update_mc_based_on_firework()

        mc_R = agent.mc['R']
        mc_Y = agent.mc['Y']
        mc_G = agent.mc['G']
        mc_W = agent.mc['W']
        mc_B = agent.mc['B']

        mc_R_exp = [2,1,1,1,1]
        mc_Y_exp = [2,1,1,2,1]
        mc_G_exp = [2,1,2,2,1]
        mc_W_exp = [2,2,2,2,1]
        mc_B_exp = [3,2,2,2,1]

        self.assertTrue(mc_R == mc_R_exp)
        self.assertTrue(mc_Y == mc_Y_exp)
        self.assertTrue(mc_G == mc_G_exp)
        self.assertTrue(mc_W == mc_W_exp)
        self.assertTrue(mc_B == mc_B_exp)

    def test_update_tables(self):
        # Init 
        observation = self.set_observation()
        agent = self.set_agent(observation)

        agent.observation['observed_hands'][1] = [{'color': 'B', 'rank': 2},
                                                {'color': 'R', 'rank': 4}, 
                                                {'color': 'B', 'rank': 0}, 
                                                {'color': 'G', 'rank': 2}]

        agent.observation['observed_hands'][2] = [{'color': 'Y', 'rank': 2},
                                                {'color': 'R', 'rank': 3}, 
                                                {'color': 'W', 'rank': 1}, 
                                                {'color': 'Y', 'rank': 2}]

        agent.observation['observed_hands'][3] = [{'color': 'W', 'rank': 3},
                                                {'color': 'G', 'rank': 1}, 
                                                {'color': 'R', 'rank': 3}, 
                                                {'color': 'B', 'rank': 1}]

        agent.observation['observed_hands'][4] = [{'color': 'W', 'rank': 2},
                                                {'color': 'B', 'rank': 3}, 
                                                {'color': 'R', 'rank': 1}, 
                                                {'color': 'G', 'rank': 0}]

        action = {'action_type': 'REVEAL_RANK', 'rank': 2, 'target_offset': 4}

        player_hats = agent.player_hats(action)

        agent.update_tables(action)



        agent.observation['card_knowledge'][4] = [{'color': None, 'rank': 2},
                                                {'color': None, 'rank': None},
                                                {'color': None, 'rank': None},
                                                {'color': None, 'rank': None}]
        first_card_player1_rank = agent.observation['observed_hands'][2][0]['rank']
        first_card_player2_rank = agent.observation['observed_hands'][1][0]['rank']
        first_card_player3_rank = agent.observation['observed_hands'][3][0]['rank']
        first_card_player4_rank = agent.observation['observed_hands'][4][0]['rank']

        first_card_player1_color = agent.observation['observed_hands'][2][0]['color']
        first_card_player2_color = agent.observation['observed_hands'][1][0]['color']
        first_card_player3_color = agent.observation['observed_hands'][3][0]['color']
        first_card_player4_color = agent.observation['observed_hands'][4][0]['color']

        self.assertTrue(agent.table[1][0]\
                        [first_card_player1_color][first_card_player1_rank] == 1)

        self.assertTrue(agent.table[2][0]\
                        [first_card_player2_color][first_card_player2_rank] == 1)

        self.assertTrue(agent.table[3][0]\
                        [first_card_player3_color][first_card_player3_rank] == 1)

        self.assertTrue(agent.table[4][0]\
                        [first_card_player4_color][first_card_player4_rank] == 1)

    def test_cal_other_hat(self):

        observation = self.set_observation()
        agent = self.set_agent(observation)

        observation['discard_pile'] = [{'color': 'G', 'rank': 0}]
        observation['fireworks'] = {'R': 0, 'Y': 0, 'G': 1, 'W': 0, 'B': 0}

        agent.table[4][0] = {
                             'B': [0, 0, 0, 0, 0], 
                             'G': [0, 0, 0, 0, 0], 
                             'R': [0, 0, 1, 1, 0], 
                             'W': [0, 0, 0, 0, 0], 
                             'Y': [0, 0, 0, 0, 0]
                             }

                     
        agent.table[4][1] = {
                             'B': [0, 0, 0, 1, 0], 
                             'G': [0, 0, 1, 1, 0], 
                             'R': [0, 0, 1, 1, 0], 
                             'W': [0, 0, 1, 0, 0], 
                             'Y': [0, 0, 1, 0, 0]
                             }

                     
        agent.table[4][2] = {
                             'B': [1, 1, 1, 1, 1], 
                             'G': [1, 1, 1, 1, 1], 
                             'R': [1, 1, 1, 1, 1], 
                             'W': [1, 1, 1, 1, 1], 
                             'Y': [1, 1, 1, 1, 1]
                             }

                     
        agent.table[4][3] = {
                             'B': [1, 1, 1, 1, 1], 
                             'G': [1, 1, 1, 1, 1], 
                             'R': [1, 1, 1, 1, 1], 
                             'W': [1, 1, 1, 1, 1], 
                             'Y': [1, 1, 1, 1, 1]
                             }

        agent.observation['observed_hands'][4] = [{'color': 'Y', 'rank': 1}, {'color': 'W', 'rank': 3}, {'color': 'G', 'rank': 2}, {'color': 'B', 'rank': 1}]






if __name__ == "__main__":
    testClass = TestHTGSAgent()
    testClass.test_duplicate_card_in_hand()    
    testClass.test_cal_hat_player()    
    
