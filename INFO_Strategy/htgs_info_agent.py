from hanabi_learning_environment.rl_env import Agent
from possibility_table import Table

class HTGSAgent(Agent):
    def __init__(self, config, *args, **kwargs):
        self.config = config

        self.max_rank = 4 
        self.mc = self.init_mc()
        self.observation = None
        self.table = None

        self.colors = ['B', 'G', 'R', 'W', 'Y']

        # Get Hat to recomm 
        self.encode_act_to_hat = {0: {'action_type': 'PLAY', 'card_index': 0},
                                  1: {'action_type': 'PLAY', 'card_index': 1},
                                  2: {'action_type': 'PLAY', 'card_index': 2},
                                  3: {'action_type': 'PLAY', 'card_index': 3},
                                4: {'action_type': 'DISCARD', 'card_index': 0},
                                5: {'action_type': 'DISCARD', 'card_index': 1},
                                6: {'action_type': 'DISCARD', 'card_index': 2},
                                7: {'action_type': 'DISCARD', 'card_index': 3}}
        
        self.decode_act_to_hat_sum_mod8 = {
                                        ('REVEAL_RANK', 1) : 0,
                                        ('REVEAL_RANK', 2) : 1,
                                        ('REVEAL_RANK', 3) : 2,
                                        ('REVEAL_RANK', 4) : 3,
                                        ('REVEAL_COLOR', 1) : 4,
                                        ('REVEAL_COLOR', 2) : 5,
                                        ('REVEAL_COLOR', 3) : 6,
                                        ('REVEAL_COLOR', 4) : 7
                                        }
    
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
        
        poss_tables_hand = self.table.get_poss_table_hand(0) 

        # Rule 1.
        playable_card_idx = self.playable_card_in_hand(poss_tables_hand)
        if (playable_card_idx is not None):
            act = {'action_type': 'PLAY','card_index': playable_card_idx}
            return act

        # Rule 2.
        dead_card_idx = self.dead_card_in_hand(poss_tables_hand)
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
        duplicate_card_idx = self.duplicate_card_in_hand(poss_tables_hand) 
        if (dead_card_idx is not None):
            act = {'action_type': 'DISCARD','card_index': duplicate_card_idx}
            return act
        
        # Rule 6.
        dispensable_card_idx = self.duplicate_card_in_hand(poss_tables_hand) 
        if (dispensable_card_idx is not None):
            act = {'action_type': 'DISCARD','card_index': dispensable_card_idx}
            return act

        # Rule 7
        else:
            act = {'action_type': 'DISCARD', 'card_index': 0}
            return act
        
    def playable_card_in_hand(self, poss_tables_hand):
        """ Return Index der ersten spielbaren Karte
        wenn keine Karte spielbare return None"""
       
        
        for card_idx, poss_table_card in enumerate(poss_tables_hand):

            #Prüfe ob eine Karte eindeutig identifizier bar ist
            if (self.table.get_ti(poss_table_card) == 1):
                card = self.table.get_card(poss_table_card)

                # Prüfe ob diese Karte spielebar ist 
                if (self.card_is_playable(card) is True):
                    return card_idx

        return None 

    def playable_card(self, card)-> bool:
        """Return True wenn Karte spielbar sonst False"""
        
        fireworks = self.observation['fireworks']
        return card['rank'] == fireworks[card['color']]
    
    def dead_card_in_hand(self, poss_tables_hand)->int:
        """ Return index der ersten dead Kart
        wenn keine dead Kart vorhanden return None"""
        
         
        for card_idx, poss_table_card in enumerate(poss_tables_hand):
            # Prüfe ob Karte bekannt ist
            if (self.table.get_ti(poss_table_card) == 1):
    
                # Ermittele Karte  
                card = self.table.get_card(poss_table_card)

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

    def give_hint(self):
        act_hint = self.encode_hint()

        return act_hint
                
    def encode_hint(self):
        hatSumMod8 = self.cal_hat_sum_mod8()

        # if hatSumMod8 < 4 give hint rank (See Paper Cox)
        if (hatSumMod8 < 4):
            hint = self.get_hint_hat_sum_smaller_4(hatSumMod8)
            return hint 

        # if hatSumMod8 > 3 give hint color (See Paper Cox) 
        else:
            hint = self.get_hint_hat_sum_bigger_3(hatSumMod8)
            return hint

    def cal_hat_sum_mod8(self):
        """Returns the sum of hats from all other player mod 8"""
        hat_sum_player = 0
        
        for agent_idx in range(1, self.observation['num_players']):
            hat_player = self.cal_hat_player(agent_idx)
            hat_sum_player += hat_player

        hat_sum_mod8 = hat_sum_player % 8

        return hat_sum_mod8
    
    def cal_hat_player(self, agent_idx, act = None):
        """Return hat vom Spieler mit Index agent_idx
        
        Parameter
            action(dict): Wenn der eigene Hat berechnet werden soll
                          muss die Action mit übergeben werden.
                          Hierbei muss es sich natürlich um ein Hint handeln 
        """

        # Sonderfall wenn der eigene Hat berechnet werden soll 
        # ! Hierfür muss der Hint übergeben werden 
        if agent_idx == 0:
            return self.cal_own_hat(act)

        return self.cal_other_hat(agent_idx)

    def cal_own_hat(self, act):
        """Returned eigenen hat
        
        Parameters
            action (dict): Die Action muss ein Hint sein 
        """
        
        # Throw Exception wenn Action kein Hint ist 
        if (act['action_type'] == 'PLAY' or 
            act['action_type'] == 'DISCARD'):
                raise Exception("In update_tables action must be a hint")

        # given_hat_sum_mod8 := r1 (Paper Cox)
        # hat_sum_mod8 := ri (Paper Cox)
        # own_hat := ci (Paper Cox)
        given_hat_sum_mod8 = self.decode_act_to_hat_sum_mod8 \
                                  [(act['action_type'], act['target_offset'])]

        idx_cur_ply = self.observation['current_player_offset']

        hat_sum = self.cal_hat_sum_mod8()
        hat_hinted_ply = self.cal_hat_player(idx_cur_ply)
        own_hat = (given_hat_sum_mod8 - (hat_sum - hat_hinted_ply)) % 8

        return own_hat           
    
    def cal_other_hat(self, agent_idx):
        """Returned hat von anderen Agent nicht dem eigenen"""

        # Raise Expection wenn man den eigenen Hat berechnen will 
        if (agent_idx == 0):
            raise Exception("Es kann nur der Hat von anderen Spielern \
                             berechnet werden")

        target_card, target_card_idx = self.get_target_card(agent_idx)
        
        poss_table_card = self.table.get_poss_table(agent_idx, target_card_idx)
        part_table = self.table.get_part_table(self.observation, poss_table_card)
        
        rank_target_card = target_card['rank']
        color_target_card = target_card['color']
        hat = part_table[color_target_card][rank_target_card]

        return hat

    def get_target_card(self, agent_idx):
        """Return Target Card und Index der Target Card in Hand"""

        poss_tables_hand = self.table.get_poss_table_hand(agent_idx)
        sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards = self.get_sum_mc_Ti_and_sum_mc_Ti_cut_Si(
                                                        poss_tables_hand)
        pb_playable_cards = self.get_pb_playable_cards(sum_mc_Ti_cards, 
                                                       sum_mc_Ti_cut_Si_cards)
        
        target_card_idx = pb_playable_cards.index(max(pb_playable_cards))
        player_hand = self.observation['observed_hands'][agent_idx]
        target_card = player_hand[target_card_idx]

        return target_card, target_card_idx

    def get_sum_mc_Ti_and_sum_mc_Ti_cut_Si(self, poss_tables_hand):
        """Return Nenner und Zahler von Formel S3"""
        max_rank = 4
        sum_mc_Ti_cut_Si_cards = []
        sum_mc_Ti_cards = []

        for poss_table_card in poss_tables_hand:

            sum_mc_Ti_cut_Si = 0
            sum_mc_Ti = 0    
            
            for rank in range(max_rank+1):
                for color in self.colors:
                    card = {'color': color, 'rank': rank}
                    
                    # Alle Ti in 
                    if(poss_table_card[color][rank] == 1):
                        sum_mc_Ti += self.mc[color][rank]


                    if (self.playable_card(card) and poss_table_card[color][rank] == 1):
                        sum_mc_Ti_cut_Si += self.mc[color][rank]
        
            sum_mc_Ti_cards.append(sum_mc_Ti)
            sum_mc_Ti_cut_Si_cards.append(sum_mc_Ti_cut_Si)
        
        return sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards
      
    def get_pb_playable_cards(self, sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards):

        pb_playable_cards = []

        for sum_mc_Ti, sum_mc_Ti_cut_Si in zip(sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards):
            try:
                pb_playable_cards.append(sum_mc_Ti_cut_Si / sum_mc_Ti)
            except ZeroDivisionError:
                print("Zero Division Error")
                raise ZeroDivisionError
        
        return pb_playable_cards

    def get_hint_hat_sum_smaller_4(self, hat_sum_mod8):
        # Überprüftr
        # See Paper Cox for calculation 
        idxPly = hat_sum_mod8 + 1

        # Get a random rank to hint from player (idxPly)
        # which get the hint 
        hand_player = self.observation['observed_hands'][idxPly]
        first_hand_card = hand_player[0]
        rank = first_hand_card['rank']

        hint =  {'action_type': 'REVEAL_RANK',
                'rank': rank,
                'target_offset': idxPly } 

        return hint

    def get_hint_hat_sum_bigger_3(self, hatSumMod8):
        # See Paper Cox for calculation 
        idx_ply = hatSumMod8 - 3

        # Get a random color to hint from player (idxPly)
        # which get the hint 
        hand_ply = self.observation['observed_hands'][idx_ply]
        first_hand_card = hand_ply[0]
        color = first_hand_card['color']


        hint =  {'action_type': 'REVEAL_COLOR',
                'color': color,
                'target_offset': idx_ply }

        return hint        

    def duplicate_card_in_hand(self):
        pass

    def card_is_dispensable(self):

        pass

    def update_mc(self):
        """Based on the Public Information we calculate mc
        For each card we find in public information (card_knowledge,
        discard_pile and firework) we reduce max number by one"""

        self.mc = self.init_mc()

        self.update_mc_based_on_card_knowledge()

        self.update_mc_based_on_discard_pile()

        self.update_mc_based_on_firework()
        
    def update_mc_based_on_firework(self):
        """ Update mc based on Firework"""

        # Jede Karte die im Firework liegt kann nicht 
        # mehr auf der Hand eines Spieles sein  
        firework = self.observation['fireworks']
        for color, max_rank in firework.items():
            for rank in range(max_rank):
                self.mc[color][rank] -= 1
    
    def update_mc_based_on_card_knowledge(self):
        """Update mc based on card_knowledge """
        
        card_knowledge = self.observation['card_knowledge']
        
        # Prüfe alle Karten in card_knowledge
        for player_card_knowledge in card_knowledge:
            for card in player_card_knowledge:

                # Wenn eine Karte vollständig bekannt dann reduziere mc
                # Diese Karte kann ja nicht mehr einer anderen Hand sein
                if (card['rank'] is not None and  
                    card['color'] is not None):

                    self.mc[card['color']][card['rank']] -= 1

    def update_mc_based_on_discard_pile(self): 
        """Update mc based on discard_pile """

        # Jede Karte die im Discard Pile ist kann nicht mehr in der Hand 
        # eines anderen Spieler sein 
        discard_pile = self.observation['discard_pile']
        for card in discard_pile:
            self.mc[card['color']][card['rank']] -= 1   
        
    def update_poss_tables_based_card_knowledge(self):
        """Updaten den Possibilty Table auf Basis der card_knowledge
        (Also der Informationen die NUR aus einem hint entstehen, also nicht
        aus dem Hatguessig"""

        card_knowledge = self.observation['card_knowledge']

        for agent_idx, player_card_knowledge in enumerate(card_knowledge):
            for card_idx, card in enumerate(player_card_knowledge):

                # Update possibility table based on card 
                self.update_poss_tables_based_card(card, agent_idx, card_idx)

    def update_poss_tables_based_card(self, card, agent_idx, card_idx):
        """Update poss table based on card from card_knowledge

        Args:
            card (list): card from card_knowledge
            agent_idx (int): player index where the card came from
            card_idx (int): card index in hand from player 

        Returns:
            None
        """
       
        max_rank = 4
        
        # Wenn man Rank von Karte Kennt, kann ausgeschlossen
        # werden das die Karte einen anderen Rank hat 
        if (card['rank'] is not None):
            
            # Setze für jeden Rank außer den bekannten Rank
            # Den Wert auf 0 für 
            for rank in range(max_rank+1):
            
                if rank == card['rank']:
                    continue

                for color in self.colors:
                    self.table[agent_idx][card_idx]\
                              [color][rank] = 0
            
        if (card['color'] is not None):
            
            # Setze jede Karte einer anderen Farbe auf 0
            for color in self.colors:
                
                # Überspringe die Farbe welche die Karte hat 
                if color == card['colors']:
                    continue

                for rank in range(max_rank+1):
                    self.table[agent_idx][card_idx]\
                              [color][rank] = 0        

    def update_observation(self, observation):
        """Update Observation"""
        self.observation = observation
    
    def update_tables(self, action):
        """Update the table based on hint
        
        Parameters
        action (dict): Die Action muss ein Hint sein 
        """
        # Throw Exception wenn Action kein Hint ist 
        if (action['action_type'] == 'PLAY' or 
            action['action_type'] == 'DISCARD'):
                raise Exception("In update_tables action must be a hint")
        
        # Berechne die Hütte aller Spieler (auch den eigenen)
        # auf Basis vom hint
        player_hats = self.player_hats(action)
        target_cards_idx = self.targeted_cards_idx()
              
        for agent_idx in range(self.observation['num_player']):
            self.update_table(agent_idx,
                              player_hats[agent_idx], 
                              target_cards_idx[agent_idx])
    
    def update_poss_table(self, agent_idx, player_hat, target_card_idx):

        poss_table_card = self.table[agent_idx][target_card_idx]
        part_table = self.table.get_part_table(self.observation, poss_table_card)

        for color in self.colors: 
            for rank in range(self.max_rank + 1):
                if (part_table[color][rank] != player_hat):
                    self.table[agent_idx][color][rank] == -1
        

    def player_hats(self, action):
        """Return list with hats off all Players"""
        player_hats = []

        for agent_idx in range(self.observation['num_players']):
           
           player_hats.append(self.cal_hat_player(agent_idx, action))
        
        return player_hats
    def targeted_cards_idx(self):
        """Return list mit targed_cards von allen Agent
        außer dem der aktuell dar ist. Also dem der gehintet hat"""

        targeted_cards_idx = []
        idx_hinting_player = self.observation['current_player_offset']

        for agent_idx in range (self.observation['num_players']):

            # Der Spieler der den Hint gibt kann ja nicht seinen Hat wissen
            # Damit wird dieser auch nicht berechnet den es ist keine 
            # Public Information  
            if idx_hinting_player == agent_idx:
                targeted_cards_idx.append(None)
                continue
        
            else:
                _, target_idx = self.get_target_card(agent_idx)
                targeted_cards_idx.append(target_idx)
        
        return targeted_cards_idx
           
    def decode_hint(self, act):
        """Return Partition und Card Idx 
        
        Parameter:
            action(dict): action muss ein hint sein sonst 
                          throw exception
        
        """
        # Spielanfang kein Hint wurde gegeben
        # => given_hint == None
        # => gebe hint
     
        

        # Der eigene hat entspricht der Partition der targed_card
        own_hat = self.cal_own_hat(act)
        _, target_card_idx = self.get_target_card(0)
        
        return own_hat, target_card_idx
        







