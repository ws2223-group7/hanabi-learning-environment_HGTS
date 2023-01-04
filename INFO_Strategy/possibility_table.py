class Table(list):
    def __init__(self,observation):
        super().__init__(self.init_table(observation))
    
    def init_table(self, observation):
        #num_players = observation['num_players']
        num_players = 5
        #num_cards_per_hand = len(observation['observed_hands'])
        num_cards_per_hand = 4
        num_color = 5
        num_ranks = 5 
        table = [[[[1] * num_ranks]*num_color]*num_cards_per_hand for i in range (num_players)]
        return table

if __name__ == '__main__':
    test = Table(5)
    print(test)

    
