from hanabi_learning_environment.rl_env import Agent
from possibility_table import Table

class HTGSAgent(Agent):
    def __init__(self, config, *args, **kwargs):
        self.config = config

        self.mc = self.init_mc()
        self.observation = None
        self.table = None
    
    def init_table(self, observation):
        self.table = Table(observation)

    def init_mc(self):
        rep_color = [3,2,2,2,1]

        mc = {'B': rep_color.copy(),
              'G': rep_color.copy(),
              'R': rep_color.copy(),
              'W': rep_color.copy(),
              'Y': rep_color.copy(),}
        
        return mc

    def act(self):
        
        hand_table = self.table.get_hand_table(0) 

        # Rule 1.
        playable_card_idx = self.playable_card_in_hand(hand_table)
        if (playable_card_idx is not None):
            act = {'action_type': 'PLAY','card_index': playable_card_idx}
            return act

        # Rule 2.
        dead_card_idx = self.dead_card_in_hand(hand_table)
        if (len(self.observation['discard_pile']) < 5 and dead_card_idx is not None):
            act = {'action_type': 'DISCARD','card_index': playable_card_idx}
            return act
        
        # Rule 3.
        if (self.observation['information_tokens'] > 0):
            return self.give_hint()
        
        # Rule 4. 
        if (dead_card_idx is not None):
            act = {'action_type': 'DISCARD','card_index': playable_card_idx}
            return act
        
        # Rule 5.
        duplicate_card_idx = self.duplicate_card_in_hand(hand_table) 
        if (dead_card_idx is not None):
            act = {'action_type': 'DISCARD','card_index': duplicate_card_idx}
            return act
        
        # Rule 6.
        dispensable_card_idx = self.duplicate_card_in_hand(hand_table) 
        if (dispensable_card_idx is not None):
            act = {'action_type': 'DISCARD','card_index': dispensable_card_idx}
            return act

        # Rule 7
        else:
            act = {'action_type': 'DISCARD', 'card_index': 0}
            return act
        

    def playable_card_in_hand(self):
        """ Return Index der ersten spielbaren Karte
        wenn keine Karte spielbare return None"""
        hand_table = self.table.get_hand_table(0)
        
        
        for card_idx, card_table in enumerate(hand_table):

            #Prüfe ob eine Karte eindeutig identifizier bar ist
            if (self.table.getTi(card_table) == 1):
                card = self.table.get_card(card_table)

                # Prüfe ob diese Karte spielebar ist 
                if (self.card_is_playable(card) is True):
                    return card_idx

        return None 

    def playable_card(self, card)-> bool:
        """Return True wenn Karte spielbar sonst False"""
        
        fireworks = self.observation['fireworks']
        return card['rank'] == fireworks[card['color']]
    


    def dead_card_in_hand(self, hand_table)->int:
        """ Return index der ersten dead Kart
        wenn keine dead Kart vorhanden return None"""
        
         
        for card_idx, card_table in enumerate(hand_table):
            # Prüfe ob Karte bekannt ist
            if (self.table.get_ti(card_table) == 1):
    
                # Ermittele Karte  
                card = self.table.get_card(card_table)

                # Prüfe ob Karte tot 
                if self.dead_card(card):
                    return card_idx

    def dead_card(self, card):
        firework = self.observation['fireworks']
        if (card['rank'] < firework[card['color']]):
            return True
        
        # Max Karten pro Rank die abgeworfen sein dürfen 
        max_card_per_rank = [3,2,2,2]

        cards_in_dsc_pile = [0,0,0,0]
        
        for card_dsc_pile in self.observation['discard_pile']:
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

    def duplicate_card_in_hand(self):
        pass

    def card_is_dispensable(self):
        pass
