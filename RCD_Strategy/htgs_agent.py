
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
    self.encodeActToHat = {0: {'action_type': 'PLAY', 'card_index': 0},
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
    elif (rcd_act['action_type'] == 'DISCARD'):
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
      if (hatSumMod8 < 4):
        hint = self.get_hint_hat_sum_smaller_4(hatSumMod8)
        return hint 

      else:
        hint = self.get_hint_hat_sum_bigger_3(hatSumMod8)
        return hint
  
  def hint_hat_sum_smaller_4(self, hatSumMod8):
    # See Paper Cox for calculation 
    idxPly = hatSumMod8 + 1

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
    idxPly = hatSumMod8 - 3

    # Get a random color to hint from player (idxPly)
    # which get the hint 
    hand_player = self.observation['observed_hands'][idxPly]
    first_hand_card = hand_player[0]
    color = first_hand_card['color']

  
    hint =  {'action_type': 'REVEAL_COLOR',
            'Color': color,
            'target_offset': idxPly }

    return hint

  def cal_hat_sum_mod8(self):
    pass

  def cal_hat_player(self, player_hand):
    pass

  def rule1_hat_player_value(self, player_hand):
    pass

  def rule2_hat_player_value(self, player_hand):
    pass

  def rule3_hat_player_value(self, player_hand):
    pass

  def rule4_hat_player_value(self, player_hand):
    pass

  def rule5_hat_player_value(self, player_hand):
    pass    
    
  def decode_hint(self):
    pass

  def cal_own_hat(self):
    pass

  def check_card_available(self):
    pass 

  def playable_card(self, card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]
            



        
