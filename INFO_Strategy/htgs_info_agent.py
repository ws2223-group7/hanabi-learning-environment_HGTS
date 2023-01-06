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
        
        # Rule 1.
        player_hand = self.table.get_hand_table(0) 
        act_playable_card = self.playable_card_in_hand(player_hand)
        if (act_playable_card is not None):
            return act_playable_card

        # Rule 2.
        if (len(self.observation['discard_pile']) < 5 and self.dead_card_in_hand(player_hand)):
            return self.dead_card_in_hand(player_hand)
        
        # Rule 3.
        if (self.observation['information_tokens'] > 0):
            return self.give_hint()
        
        # Rule 4. 
        if (self.dead_card_in_hand() is not None):
            return self.dead_card_in_hand()
        
        # Rule 5. 
        if (self.duplicate_card_in_hand() is not None):
            return self.duplicate_card_in_hand()
        
        # Rule 6.
        if (self.card_is_dispensable() is not None):
            return self.self.card_is_dispensable()

        # Rule 7
        else:
            act = {'action_type': 'DISCARD', 'card_index': 0}
            return act
        

    def playable_card_in_hand(self):
        """ Es wird überprüft ob eine Karte in der Hand spielbar ist"""
        hand_table = self.table.get_hand_table(0)
        
        
        for idx, card in enumerate(hand_table):

            #Prüfe ob eine Karte eindeutig identifizier bar ist
            if (self.table.getTi(card) == 1):
                card = self.table.get_card(0,idx)

                # Prüfe ob diese Karte spielebar ist 
                if (self.card_is_playable(card) is True):
                    return card 



    def dead_card_in_hand(self):
        hand_table = self.table.get_hand_table()
        for card in hand_table:
            if self.table.

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
