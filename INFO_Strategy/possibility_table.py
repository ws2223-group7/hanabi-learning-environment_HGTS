from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent

class Table(list):
    def __init__(self, observation):
        super().__init__(self.init_table(observation))

        self.colors = ['B', 'G', 'R', 'W', 'Y']
    
    def init_table(self, observation):

        num_players = observation['num_players']
        num_cards_per_hand = len(observation['observed_hands'][0])



        rep_color = [1,1,1,1,1]

        rep_hand =  {'B': rep_color.copy(),
                     'G': rep_color.copy(),
                     'R': rep_color.copy(),
                     'W': rep_color.copy(),
                     'Y': rep_color.copy(),}

        table = [[rep_hand]*num_cards_per_hand for i in range (num_players)]

        return table
    
    def get_card(self, card_table):
        """ Wenn die Karte bekannt ist 
        (ti=1) return Card sonst None"""

        # Prüfe ob Karte bekannt ist 
        if(self.table.get_ti(card_table) == 1):
            # Ermittel Karte von Table 
            pass 

    def get_ti(self, card_table)-> int:
        """ Bestimme ti (Anzahl von offene Möglichkeiten) 
        für eine bestimme Karte (player_idx, card_idx) """
        ti = 0
        
        # Iteriere über alle Farben im Table und summiere liste
        # P=1 und N=0 ti ist die Anzahl der P's 
        for color in self.colors: 
            ti += sum(card_table[color])
        
        return ti

    def get_card_table(self, player_idx, card_idx)-> list:
        """ Return card_table"""
        card_table = self[player_idx][card_idx] 
        return card_table

    def get_hand_table(self, player_idx:int)-> list:
        """ Return hand_table"""
        hand_table = self[player_idx]
        return hand_table


    
    
""" ----------- Ab Hier zu Test Zwecken ------------------------- """

def get_observation():

    AGENT_CLASSES = {'HTGSAgent' : RandomAgent}

    flags = {'players': 5, 'num_episodes': 100, 'agent_class': 'RandomAgent'}

    options, arguments = getopt.getopt(sys.argv[1:], '',
                                    ['players=',
                                    'num_episodes=',
                                    'agent_class='])
    if arguments:
        sys.exit('usage: rl_env_example.py [options]\n'
                '--players       number of players in the game.\n'
                '--num_episodes  number of game episodes to run.\n'
                '--agent_class   {}'.format(' or '.join(AGENT_CLASSES.keys())))

    for flag, value in options:
        flag = flag[2:]  # Strip leading --.
        flags[flag] = type(flags[flag])(value)
    
    environment = rl_env.make('Hanabi-Full', num_players=flags['players'])


    observations = environment.reset()
    observation = observations['player_observations'][0] 

    return observation



if __name__ == "__main__":


    import sys
    import getopt

    observation = get_observation()

    testtable = Table(observation)
    print()

 
  

