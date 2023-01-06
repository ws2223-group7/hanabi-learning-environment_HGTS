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
        if(self.get_ti(card_table) == 1):
            # Ermittel Karte von Table 
            for color in self.colors:
                for rank, value in enumerate(card_table[color]):
                    if value == 1:
                        card = {'color': color, 'rank': rank}
                        return card

        return None

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
    
    def get_part_table(self, observation, card_table):
        """Return den partition table zu einem hand_table"""
        
        # Ermittle alle toten Karten im Spiel 
        dead_cards_dict = self.get_dead_card_in_game(observation)

        # Ermittle Anzahl der Singleton set 
        single_hint_sets, seven_hint_sets = self.get_size_hint_sets(card_table, dead_cards_dict)

        # Erzeuge neuen table der als partion table dient (wie Fig.6 Cox)
        part_table = Table(observation)

        # Setze alle Deadcards auf 0 
        part_table = self.set_dead_hint_set(part_table, dead_cards_dict)

        # Setze die single hint sets 
        part_table = self.set_singleton_hint_sets(part_table, single_hint_sets)

        # Setze zusätzliche (sieberer) hint sets
        part_table = self.set_seven_hint_sets(part_table, seven_hint_sets) 


    def get_deads_card_dict(self, observation)->dict:
        """Return dict zu toten Karten im Spiel
        Es wird der max. Rank der toten Karten übergeben"""

        # Erzeuge Liste mit allen Karten 
        max_rank = 4
        all_cards = [{'color': color, 'rank':rank} for color in self.colors 
                                                   for rank in range(max_rank+1)]

        # Prüfe jede Karte ob Sie tot ist 
        dead_cards = []
        for card in all_cards:
            if (self.dead_card(card, observation)):
                dead_cards.append(card)
        
        return dead_cards
                

    def dead_card(self, card, observation):
        """Return True wenn Karte tot sonst False"""

        firework = observation['fireworks']
        if (card['rank'] < firework[card['color']]):
            return True
        
        # Max Karten pro Rank die abgeworfen sein dürfen 
        max_card_per_rank = [3,2,2,2]

        cards_in_dsc_pile = [0,0,0,0]
        
        for card_dsc_pile in observation['discard_pile']:
        
            # Prüfe alle Karten im dsc_pile mit der selben Farbe und
            # einem geringen Rank 
            if (card_dsc_pile['color'] == card['color'] 
                and card_dsc_pile['rank'] < card['rank']):
                cards_in_dsc_pile[card_dsc_pile['rank']] += 1    

            # Wenn alle Karten eines rankes einer Farbe abgewurfen worden
            # dann return True (Karte ist ToT)
            for idx,elem in enumerate(cards_in_dsc_pile):
                if elem >= max_card_per_rank[idx]:
                    return True

        return False
    
    def get_size_hint_sets(self, card_table, dead_cards_dict):
        """Return die Anzahl an single hint sets  
        und die Anzahl der hint sets mit größe sieben"""
        
        num_dead_card = len(dead_cards_dict)

        # Die max singleton_size hängt davon ob
        # ob eine Partition von Dead Cards belegt wird 
        max_single_hint_set = 7 if num_dead_card < 0 else 8

        # Es können alle verbleiben Karten (ti - num_dead_card)
        # als singleton realisiert werden wenn es nicht zu viele sind
        single_hint_set = self.get_ti(card_table) - num_dead_card 

        # Anzahl der zusätzlichen 7 hint sets 
        seven_hint_sets = 0  
        
        # Solange es zu viele singleton gibt ziehe ein block der größe 7 ab 
        while (single_hint_set > max_single_hint_set):
            single_hint_set -= 7
            seven_hint_sets += 1

            # Jedes zusätzliche Set reduziert
            max_single_hint_set -= 1

        return single_hint_set, seven_hint_sets


    def set_dead_hint_set(self, part_table, dead_cards_dict):
        """Return part_table mit gesetzer Partition für alle 
        dead cards"""
        pass        

    def set_singleton_hint_sets(part_table, single_hint_sets):
        """Return part_table mit gesetzen Partitionen 
        für single hint set"""
        pass    

        




    
    
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

 
  

