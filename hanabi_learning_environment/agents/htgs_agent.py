
from hanabi_learning_environment.rl_env import Agent

class HTGSAgent(Agent):
  """Agent test Class."""

  def __init__(self, config, *args, **kwargs):
    """Initialize the agent."""
    self.config = config
  
    self.givenHint = None  
    self.sinceHintPlayedCard = False
    self.rcd_card_plyd = False


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
    rcd_act = self.decode_hint()

    if (rcd_act['action_type'] == 'PLAY' and self.rcd_card_not_plyd):
      
      # PlayRule 1
      if (self.since_hint_played_card):
        self.rcd_card_plyd = True
        return rcd_act

      # PlayRule 2
      else:
        if (observation >= 1):
          self.rcd_card_plyd = True
          return rcd_act

    # PlayRule 3
    elif (NrHintToken != 0):
      return self.give_Hint()

    # PlayRule 4
    elif (rcd_act['action_type'] == 'DISCARD'):
      return rcd_act

    # PlayRule 5
    else:
      dsc_c1 = {'action_type': 'DISCARD', 'card_index': 0}
      return dsc_c1 


  def giveHint(self):
    pass 
            
  def encodeHint(self):
    pass

  def calHatSumMod8(self):
    pass

  def calHatPlayer(self, playerHand):
    pass

  def rule1HatPlayerValue(self, playerHand):
    pass

  def rule2HatPlayerValue(self, playerHand):
    pass

  def rule3HatPlayerValue(self, playerHand):
    pass

  def rule4HatPlayerValue(self, playerHand):
    pass

  def rule5HatPlayerValue(self, playerHand):
    pass    
    
  def decodeHint(self):
    pass

  def calOwnHat(self):
    pass

  def checkCardAvailable(self):
    pass 


  def playable_card(self, card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]
            


