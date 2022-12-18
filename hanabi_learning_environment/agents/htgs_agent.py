from hanabi_learning_environment.rl_env import Agent

class HTGSAgent(Agent):
  """Agent test Class."""

  def __init__(self, config, *args, **kwargs):
    """Initialize the agent."""
    self.config = config
    self.endodeHint = None
    self.idxCluer = None


    # Get Hat to recomm 
    self.encodeActToHat = {None}
    
    # Extract max info tokens or set default to 8.
    self.max_information_tokens = config.get('information_tokens', 8)





  @staticmethod
  def playable_card(card, fireworks):
    """A card is playable if it can be placed on the fireworks pile."""
    return card['rank'] == fireworks[card['color']]

  def act(self, observation):
    """Act based on an observation."""
    if observation['current_player_offset'] != 0:
      return None

    # Sobald Hint Color oder Rank spiele gehinted Karte 
    # observation['card_knowledge'][0] : Eigene Karten

    # Iterien über eigene Karten (Also durch die Hinweise)
    for card_index, card in enumerate(observation['card_knowledge'][0]):

      # Prüfe ob die Karte vollständig bekannt  
      if card['color'] is not None and card['rank'] is not None:
        
        # Prüfe ob vollständig bekannte Karte spielbar
        if (self.playable_card(card)):

            cardPlayable = True 
            # Prüfe ob irgendeinanderer Sieler die selbe (spielbare)
            # Karte hat 
            for playerHand in range(1, observation['num_player']):
                if cardPlayable: 
                    numberCardsPerPlayer = len(observation['observed_hands'][0])
                    for numCardInHand in range(numberCardsPerPlayer):
                        if cardPlayable: 
                            # Karte 
                            handCardOtherPlayer = observation['observed_hands'][playerHand][numCardInHand]
                            
                            #Prüfe ob Karte gleich spielbarer Karte ist 
                            if (handCardOtherPlayer == card):
                                
                                # Spiele Karte nicht
                                cardPlayable = False
                                # ggf. doppelter 
            
            if cardPlayable:
                return {
                'action_type': 'Play',
                'color': card['color'],
                'target_offset': player
            }
    
    def calHint():
        None

    def giveHint():
        None 
            
        
            
            



        

    
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