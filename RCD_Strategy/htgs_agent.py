
from hanabi_learning_environment.rl_env import Agent

class HTGSAgent(Agent):
  """Agent test Class."""

  def __init__(self, config, *args, **kwargs):
    """Initialize the agent."""
    self.config = config
  
    self.given_hint = None  
    self.since_hint_plyd_card = False
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

  def act(self, observation):
    """Act based on an observation."""
    self.observation = observation

    rcd_act = self.decode_hint()

    if (rcd_act['action_type'] == 'PLAY' and self.rcd_card_not_plyd):
      
      # PlayRule 1
      if (self.since_hint_played_card):
        self.rcd_card_plyd = True
        return rcd_act

      # PlayRule 2
      else:
        if (observation['life_tokens'] >= 1):
          self.rcd_card_plyd = True
          return rcd_act

    # PlayRule 3
    elif (observation['information_tokens'] != 0):
      return self.give_Hint(observation)

    # PlayRule 4
    elif (rcd_act['action_type'] == 'DISCARD' and self.rcd_card_not_plyd):
      self.rcd_card_plyd = True
      return rcd_act
      

    # PlayRule 5
    else:
      dsc_c1 = {'action_type': 'DISCARD', 'card_index': 0}
      return dsc_c1 


  def give_hint(self):
    act_hint = self.encode_hint()
    return act_hint
            
  def encode_hint(self):
      hatSumMod8 = self.calHatSumMod8()

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

  def hint_hat_sum_smaller_4(self, hat_sum_mod8):
    # See Paper Cox for calculation 
    idxPly = hat_sum_mod8 + 1

    # Get a random rank to hint from player (idxPly)
    # which get the hint 
    hand_player = self.observation['observed_hands'][idxPly]
    first_hand_card = hand_player[0]
    rank = first_hand_card['rank']

    hint =  {'action_type': 'REVEAL_Rank',
            'rank': rank,
            'target_offset': idxPly } 

    return hint
  
  def get_hint_hat_bigger_3(self, hatSumMod8):
    # See Paper Cox for calculation 
    idx_ply = hatSumMod8 - 3

    # Get a random color to hint from player (idxPly)
    # which get the hint 
    hand_ply = self.observation['observed_hands'][idx_ply]
    first_hand_card = hand_ply[0]
    color = first_hand_card['color']

  
    hint =  {'action_type': 'REVEAL_COLOR',
            'Color': color,
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
        if card['Rank'] == 4:
            if self.card_is_playable(card):
                # Der Hat ist gleich der KartenIndex (Siehe Paper)
                hat = idx_card
                return hat
    return None

  def rule2_hat_player_value(self, player_hand):
    min_rank = 999
    idx_ply_card = 5
    for idx_card, card in enumerate(player_hand):
      if (self.card_is_playable(card) and card['rank'] < min_rank):
        min_rank = card['rank']
        idx_ply_card = idx_card

    if (min_rank == 999):
      return None

    hat = idx_ply_card
    return hat

  def rule3_hat_player_value(self, player_hand):
    for idx_card,card in enumerate(player_hand):
      if (self.cardIsDead(card)):
          hat = idx_card
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
    
    hat = idx_ply_card
    return hat

  def rule5_hat_player_value(self, player_hand):
    return 0    
    
  def decode_hint(self):
    # Spielanfang kein encodedHint vorhanden
      # => Gebe Hint
      if (self.encode_hint == None):
          if (self.observation['information_tokens'] >= 1):
              rcd_act = self.give_hint()
              
          else:
              rcd_act = {'action_type': 'DISCARD', 'card_index': 0}
              

      else:
        hat = self.cal_own_hat()
        rcd_act = self.encode_act_to_hat[hat]

      return rcd_act

  def cal_own_hat(self):
    pass




  def playable_card(self, card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]

  def dead_card(self, card, firework):
    if (card['rank'] < firework[card['color']]):
        return True
    
    # Max Karten pro Rank die abgeworfen sein dürfen 
    max_card_per_rank = {3,2,2,2}

    cards_in_dsc_pile = {0,0,0,0}
    
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
    nr_rem_card_in_deck = {3,2,2,2,1}
    
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


    