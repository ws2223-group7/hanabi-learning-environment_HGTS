import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.rl_env import Agent

class HTGSAgent(Agent):
  """Agent test Class."""

  def __init__(self, config, *args, **kwargs):
    """Initialize the agent."""
    self.config = config

    self.rcd_act = None 

    self.nr_card_ply_since_hint = 0 
    self.rcd_card_plyd = False

    self.observation = None

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

  def act(self, observation):
    """Act based on an observation."""
    self.observation = observation

    # Wenn kein 
    if self.rcd_act == None:
      if observation['information_tokens'] == 0:
        print("Try to give hint with 0 Token")
      return self.give_hint()

    
    # PlayRule1 
    if (self.rcd_act['action_type'] == 'PLAY' 
        and not self.rcd_card_plyd
        and (self.nr_card_ply_since_hint == 0)):
      
      self.rcd_card_plyd = True
      return self.rcd_act
      
      

  # PlayRule 2
    elif (self.rcd_act['action_type'] == 'PLAY' 
          and not self.rcd_card_plyd 
          and (self.nr_card_ply_since_hint == 1)
          and self.observation['life_tokens'] > 1):
      
      self.rcd_card_plyd = True
      return self.rcd_act
  
      
    # PlayRule 3
    elif (observation['information_tokens'] != 0):
      return self.give_hint()

    # PlayRule 4
    elif (self.rcd_act['action_type'] == 'DISCARD' and not self.rcd_card_plyd):
      self.rcd_card_plyd = True
      return self.rcd_act
      

    # PlayRule 5
    else:
      dsc_c1 = {'action_type': 'DISCARD', 'card_index': 0}
      return dsc_c1 

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
      hat_sum_player = 0
      
      for idx_ply in range(1, self.observation['num_players']):
          hand_player = self.observation['observed_hands'][idx_ply]
          hat_player = self.cal_hat_player(hand_player)
          hat_sum_player += hat_player

      hat_sum_mod8 = hat_sum_player % 8

      return hat_sum_mod8

  def get_hint_hat_sum_smaller_4(self, hat_sum_mod8):
    # Überprüftr
    # See Paper Cox for calculation 
    idx_ply = hat_sum_mod8 + 1

    # Get a random rank to hint from player (idxPly)
    # which get the hint
     
    if idx_ply > (self.observation['num_players'] - 1):
        discard = {'action_type': 'DISCARD', 'card_index': 0}
        return discard



    hand_player = self.observation['observed_hands'][idx_ply]
    first_hand_card = hand_player[0]
    rank = first_hand_card['rank']

    

    hint =  {'action_type': 'REVEAL_RANK',
            'rank': rank,
            'target_offset': idx_ply } 

    return hint
  
  def get_hint_hat_sum_bigger_3(self, hatSumMod8):
    # See Paper Cox for calculation 
    idx_ply = hatSumMod8 - 3

    if idx_ply > (self.observation['num_players'] - 1):
        discard = {'action_type': 'DISCARD', 'card_index': 0}
        return discard

    # Get a random color to hint from player (idxPly)
    # which get the hint 
    hand_ply = self.observation['observed_hands'][idx_ply]
    first_hand_card = hand_ply[0]
    color = first_hand_card['color']

  
    hint =  {'action_type': 'REVEAL_COLOR',
            'color': color,
            'target_offset': idx_ply }

    return hint

  def cal_hat_player(self, player_hand):
    rules = [self.rule1_hat_player_value,
             self.rule2_hat_player_value,
             self.rule3_hat_player_value,
             self.rule4_hat_player_value,
             self.rule5_hat_player_value,]

    for rule in rules:
        hat = rule(player_hand)
        if (hat is not None):
          return hat

  def rule1_hat_player_value(self, player_hand):
    # Recommend playable Card Rank 5 with lowest Index
    for idx_card, card in enumerate(player_hand):
        if card['rank'] == 4:
            if self.playable_card(card):
                # Der Hat ist gleich der KartenIndex (Siehe Paper)
                hat = idx_card
                return hat
    return None

  def rule2_hat_player_value(self, player_hand):
    # Überprüft
    min_rank = 999
    idx_ply_card = 5
    for idx_card, card in enumerate(player_hand):
      if (self.playable_card(card) and card['rank'] < min_rank):
        min_rank = card['rank']
        idx_ply_card = idx_card

    if (min_rank == 999):
      return None

    hat = idx_ply_card
    return hat

  def rule3_hat_player_value(self, player_hand):
    for idx_card,card in enumerate(player_hand):
      if (self.dead_card(card)):
          hat = idx_card + 4
          return hat

    return None

  def rule4_hat_player_value(self, player_hand):
    max_rank = -1
    idx_ply_card = 5
    for idx_card, card in enumerate(player_hand):
        if (self.indispensable_card(card) == False and card['rank'] > max_rank):
            max_rank = card['rank']
            idx_ply_card = idx_card
     
    if (max_rank == -1):
        return None
    
    hat = idx_ply_card + 4
    return hat

  def rule5_hat_player_value(self, player_hand):
    return 4    


  def decode_hint(self, act, ply_hand):
    # Spielanfang kein Hint wurde gegeben
    # => given_hint == None
    # => gebe hint

    act_type = act['action_type']
    ply_idx = act['target_offset']
    given_hat_sum_mod8 = self.decode_act_to_hat_sum_mod8[(act_type, ply_idx)]

    own_hat = self.cal_own_hat(given_hat_sum_mod8)
    
    # rcd_act is der decoded Hint also der empfolene move
    self.rcd_act = self.encode_act_to_hat[own_hat]
   
    self.rcd_card_plyd = False
    self.nr_card_ply_since_hint = 0
    

  def cal_own_hat(self, given_hat_sum_mod8):
    # given_hat_sum_mod8 := r1 (Paper Cox)
    # hat_sum_mod8 := ri (Paper Cox)
    # own_hat := ci (Paper Cox)

    idx_cur_ply = self.observation['current_player_offset']
    hand_cur_ply = self.observation['observed_hands'][idx_cur_ply]
    

    hat_sum = self.cal_hat_sum_mod8()
    hat_hinted_ply = self.cal_hat_player(hand_cur_ply)
    own_hat = (given_hat_sum_mod8 - (hat_sum - hat_hinted_ply)) % 8

    return own_hat


  def playable_card(self, card):
    """A card is playable if it can be placed on the fireworks pile."""
    fireworks = self.observation['fireworks']
    return card['rank'] == fireworks[card['color']]

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

  def indispensable_card(self,card):

    # Anzahl der verbleiben Karten
    # in Deck, Firework und Händen   
    nr_rem_card_in_deck = [3,2,2,2,1]
    
    for card_dsc_pile in self.observation['discard_pile']:
      # Prüfe alle Karten im dsc_pile mit der selben Farbe und
      # einem geringen Rank 
      if card_dsc_pile['color'] == card['color']:
        nr_rem_card_in_deck[card_dsc_pile['rank']] -= 1    

    # Wenn die Karten nur noch einmal da ist
    # dann return True (Karte ist ToT)
    if nr_rem_card_in_deck[card['rank']] == 1:
      return True

    return False


    