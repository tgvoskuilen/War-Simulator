
import random
import matplotlib.pyplot as plt
import statistics
import numpy
import time
from multiprocessing import Pool

class Card(object):
    mapping = {11:"J", 12:"Q", 13:"K", 14:"A"}
    
    def __init__(self, rank):
        """
        Init card with rank integer from 2 to 14, 11-14 are face cards
        """
        self.rank = rank
        
    def __str__(self):
        return self.mapping[self.rank] if self.rank in self.mapping else str(self.rank)
        
def shuffled_deck():
    """
    Generate shuffled deck of all 52 cards
    """
    d = []
    
    for _ in ["Heart","Club","Diamond","Spade"]:
        for rank in [2,3,4,5,6,7,8,9,10,11,12,13,14]:
            d.append(Card(rank))
    
    random.shuffle(d)
    
    return d

class OutOfCards(Exception):
    def __init__(self, name):
        self.message = "%s is out of cards" % name
        super().__init__(self.message)
        
class Player(object):
    def __init__(self, name, deck):
        self.deck = deck
        self.name = name
        
    def play(self):
        """
        Play the top card from the deck. Throw OutOfCards if
        deck is empty - player loses
        """
        if len(self.deck) > 0:
            return self.deck.pop(0)
        else:
            raise OutOfCards(self.name)
        
    def add_cards(self, cards):
        """
        Player receives a set of cards and adds them in random order
        to the back of their deck. If this is not randomized there 
        is a possibility for an infinite game - randomizing also
        matches what is done in a real game.
        
        https://arxiv.org/abs/1007.1371
        """
        random.shuffle(cards)
        self.deck.extend(cards)
        
class Game(object):
    def __init__(self, verbose=False):
        deck = shuffled_deck()
        self.player1 = Player("Player 1", deck[0:26])
        self.player2 = Player("Player 2", deck[26:])
        self.verbose = verbose

    def play(self):
        rounds = 0
        try:
            while True:
                if self.verbose:
                    print("ROUND %d" % (rounds+1))
                self._compare_cards(pot=[],indent="  ")
                rounds += 1
                
        except OutOfCards as err:
            if self.verbose:
                print(err)
            
        if self.verbose:
            print("Game complete in %d rounds" % rounds)
            
        return rounds
    
    def _compare_cards(self, pot, indent):
        """
        Draw the top cards from each player, add to pot, and see
        if there is a winner to award the pot to. For a tie,
        add face-down cards to the pot from each player then recurse.
        """
        c1 = self.player1.play()
        c2 = self.player2.play()
        pot.extend([c1,c2])
        
        if self.verbose:
            print("%s%s vs %s" % (indent,c1,c2))
            
        if c1.rank > c2.rank:
            self.player1.add_cards(pot)
            if self.verbose:
                r = ",".join([str(c) for c in pot])
                print("%sP1 wins [%s] (%d vs %d)" % (indent, r, len(self.player1.deck), len(self.player2.deck)))
                
        elif c2.rank > c1.rank:
            self.player2.add_cards(pot)
            if self.verbose:
                r = ",".join([str(c) for c in pot])
                print("%sP2 wins [%s] (%d vs %d)" % (indent, r, len(self.player1.deck), len(self.player2.deck)))
                
        else:
            if self.verbose:
                print("%sTIE!" % indent)
                
            # Add face-down cards to the pot from each player
            # Playing the game variant here where if a player runs out
            # of cards to play during a "war" they lose. Alternate rule is that
            # a player out of cards does not add to the pot and keeps re-playing their
            # last face-up card. This is a stupid rule.
            pot.append(self.player1.play())
            pot.append(self.player2.play())

            self._compare_cards(pot,indent+"  ")
    
def run_game(i):
    g = Game()
    return g.play()
    
if __name__ == "__main__":
   
    num_games = 100000
    start = time.time()

    with Pool() as pool:
        num_rounds = pool.map(run_game, range(0,num_games))
            
    end = time.time()
    
    print("Ran %d games in %3.1f seconds" % (num_games, end-start))
        
    print("Game statistics:")
    print("  Mean   = %3.0f rounds" % statistics.mean(num_rounds))
    print("  Median = %3.0f rounds" % statistics.median(num_rounds))
    print("  Longest  = %d rounds" % max(num_rounds))
    print("  Shortest = %d rounds" % min(num_rounds))
    print("  95%% = %d rounds" % numpy.percentile(num_rounds, 95.0))
    print("  99%% = %3.0f rounds" % numpy.percentile(num_rounds, 99.0))
    print("  99.9%% = %3.0f rounds" % numpy.percentile(num_rounds, 99.9))
    
    f = plt.figure()
    plt.hist(num_rounds, bins=100)
    plt.xlabel("Number of Rounds")
    plt.ylabel("Games")
    plt.show()