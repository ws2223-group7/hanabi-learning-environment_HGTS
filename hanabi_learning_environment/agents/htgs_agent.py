from hanabi_learning_environment.rl_env import Agent

class HTGSAgent(Agent):
  """Agent test Class."""

  def __init__(self, config, *args, **kwargs):
    """Initialize the agent."""
    self.config = config
  
    self.givenHint = None  
    self.sinceHintPlayedCard = False


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
    pass

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

  def calOwnHat():
    pass 




  def playable_card(self, card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]
            



        

    
    ### Ab hier Regeln Hat Agent ### 

    # Check if it's possible to hint a card to your colleagues.
    fireworks = observation['fireworks']
    if observation['information_tokens'] > 0:

      # Check if there are any playable cards in the hands of the opponents.
      for player_offset in range(1, observation['num_players']):
        player_hand = observation['observed_hands'][player_offset]
        player_hints = observation['card_knowledge'][player_offset]

        # Check if the card in the hand of the opponent is playable
        # and if it is playable and the color is not hinted hint the color 
        for card, hint in zip(player_hand, player_hints):
          if HatInfoAgent.playable_card(card,
                                       fireworks) and hint['color'] is None:
            return {
                'action_type': 'REVEAL_COLOR',
                'color': card['color'],
                'target_offset': player_offset
            }

    # If no card is hintable then discard or play.
    if observation['information_tokens'] < self.max_information_tokens:
      return {'action_type': 'DISCARD', 'card_index': 0}
    else:
      return {'action_type': 'PLAY', 'card_index': 0}

  def playable_card(self, card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]