

class Table(list):
    def __init__(self, observation):
        super().__init__(self.init_table(observation))
    
    def init_table(self, observation):

        num_players = observation['num_players']
        num_cards_per_hand = len(observation['observed_hands'][0])



        rep_color = [1,1,1,1,1]

        rep_hand =  {'BLUE': rep_color.copy(),
                     'GREEN': rep_color.copy(),
                     'RED': rep_color.copy(),
                     'WHITE': rep_color.copy(),
                     'YELLOW': rep_color.copy(),}

        table = [[rep_hand]*num_cards_per_hand for i in range (num_players)]

        return table




    
    
""" ----------- Ab Hier zu Test Zwecken ------------------------- """

def get_observation():

    AGENT_CLASSES = {'HTGSAgent' : HTGSAgent}

    flags = {'players': 5, 'num_episodes': 100, 'agent_class': 'HTGSAgent'}

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
    from hanabi_learning_environment import rl_env
    from htgs_info_agent import HTGSAgent

    import sys
    import getopt

    observation = get_observation()

    testtable = Table(observation)
    print()

 
  

