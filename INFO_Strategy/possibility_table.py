from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent

import math

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
        dead_cards_in_game = self.get_deads_card(observation)

        # Ermittle Anzahl der Singleton set 
        single_hint_sets, seven_hint_sets = self.get_size_hint_sets(card_table,dead_cards_in_game)

        # Erzeuge neuen table der als partion table dient (wie Fig.6 Cox)
        part_table = self.init_part_table(card_table)

        # Setze alle Deadcards auf 0 
        part_table = self.set_dead_hint_set(part_table,dead_cards_in_game)

        # Setze die single hint sets 
        part_table = self.set_singleton_hint_sets(part_table, single_hint_sets)

        # Setze zusätzliche (sieberer) hint sets
        part_table = self.set_seven_hint_sets(part_table, single_hint_sets)

        return part_table
    

    def get_deads_card(self, observation)->dict:
        """Return alle toten Karten im Spiel"""

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
    
    def get_size_hint_sets(self, card_table,dead_cards_in_game):
        """Return die Anzahl an single hint sets  
        und die Anzahl der hint sets mit größe sieben"""

        ti = self.get_ti(card_table)

        # Max Anzahl der Toten Karten in der Hand 
        pos_dead_card = self.get_possible_dead_cards(card_table, dead_cards_in_game)

        # Die max singleton_size hängt davon ob
        # ob eine Partition von Dead Cards belegt wird 
        single_hint_set = 7 if pos_dead_card > 0 else 8


        num_seven_hint_sets = 0 
        
        # Idee [2,1,1,1,5,7,7]
        # Max Anzahl der Karten in Singlehint + seven_hints + dead_set muss >= ti sein
        while (ti > (pos_dead_card + single_hint_set + num_seven_hint_sets*7)):
            single_hint_set -= 1
            num_seven_hint_sets += 1

        return single_hint_set, num_seven_hint_sets        

    def get_possible_dead_cards(self, card_table, dead_cards_in_game): 
        """Return die Anzahl der max. toten Karten in der Hand"""
        max_rank = 4
        num_pos_dead_cards = 0

        for dead_card in dead_cards_in_game:
            if (card_table[dead_card['color']][dead_card['rank']] == 1):
                num_pos_dead_cards += 1

        return num_pos_dead_cards

    def init_part_table(self, card_table):
        part_table = {}

        
        for color, rank_list in card_table.items():
            # Jedes P (also jede 1) wird zur -2 
            # Jeder N (also jede 0) wird zur -1
            idx_shifted_list =  [-2 if x==1 else -1 for x in rank_list]
            part_table[color] = idx_shifted_list

        
        return part_table

    def set_dead_hint_set(self, part_table, dead_cards_in_game):
        """Return part_table mit gesetzer Partition für alle 
        dead cards"""
        for dead_card in dead_cards_in_game:
            if (part_table[dead_card['color']][dead_card['rank']] == -2):
                part_table[dead_card['color']][dead_card['rank']] = 0

        return part_table        

    def set_singleton_hint_sets(self, part_table, single_hint_sets):
        """Return part_table mit gesetzen Partitionen 
        für single hint set"""
        
        max_rank = 4
        part_idx_single_hint = 1
        
        # Iteriere über jeden Rank und jede Farbe
        for rank in range(max_rank + 1):
            for color in self.colors:

                # Überprüfe ob noch ein single hint set gesetzt wird
                if (part_idx_single_hint > single_hint_sets):
                    return part_table

                # Wenn es sich nicht um eine freie Karte handlet 
                # (keine dead Kart), dann setze neue Partion
                # für die Karte die ein eigenes Singleton set ist
                 
                if (part_table[color][rank] == -2):
                    part_table[color][rank] = part_idx_single_hint
                    
                    part_idx_single_hint += 1

        
        return part_table

                    


        

    def set_seven_hint_sets(self, part_table, single_hint_set):
        
        max_rank = 4
        set_idx = single_hint_set + 1
        number_in_set = 0

        # Iteriere über jeden Rank und jede Farbe
        for rank in range(max_rank + 1):
            for color in self.colors:

                # # Wenn es sich nicht um eine freie Karte handlet 
                # (keine dead Kart oder singletonset), dann setze
                # neue Karte in sevenhint set 
                if (part_table[color][rank] == -2):
                    part_table[color][rank] = set_idx

                    number_in_set += 1

                    # Bei sieben Karten im Set
                    # mache neues Set  
                    if (number_in_set == 7):
                        number_in_set = 0
                        set_idx += 1
        
        return part_table


        




    
    
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

    dead_cards_in_game = testtable.get_deads_card(observation)

    card_table = testtable.get_card_table(0,0)
    
    part_table = testtable.get_part_table(observation, card_table)
    
    print()
  

