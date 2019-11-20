import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing = True

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append((suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        self.player = random.sample(self.deck, 2)
        self.dealer = random.sample(self.deck, 2)
        self.delete_cards(self.player + self.dealer)
        return self.player, self.dealer
    
    def delete_cards(self, total_cards):
        try:
            for i in total_cards:
                self.deck.remove(i)
        except ValueError:
            pass


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_cards(self, card):
        self.cards.extend(card)
        for i in range(0, len(card)):
            self.value += values[card[i][1]]


    def adjust_for_ace(self):
        if self.cards[0][1] == 'Ace' or self.cards[1][1] == 'Ace':
            if (21-self.value) >= 11:
                values['Ace'] = 11
            else:
                values['Ace'] = 1
        self.aces += 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0
        self.winnings = 0

    def win_bet(self):
        self.total += self.bet
        self.winnings += 1

    def loss_bet(self):
        self.total -= self.bet
        self.winnings += 1


def take_bet(bet_amount, player_money):
    try:
        while bet_amount > player_money or bet_amount <= 0:
            bet_amount = int(input(" Enter amount again : "))
        return bet_amount

    except TypeError:
        return "Invalid bet amount"


def hits(obj_de, obj_h):
    new_card = obj_de.deal_cards()[0][0]
    new_card = [new_card]
    obj_h.add_cards(new_card)

def hit_or_stand(obj_de, obj_h, dealer_card):
    global playing
    choice = str(input(" HIT or STAND : ")).lower()
    if choice == "hit":
        hits(obj_de, obj_h)
        show_some(obj_h.cards, dealer_card, obj_h)
    elif choice == "stand":
        playing = False
    else:
        print(" --INVALID CHOICE-- ")


def show_some(player_cards, dealer_cards, obj_h):
    print(f" ----->\n PLAYER CARDS [{obj_h.value}] : {player_cards}")
    print(f" DEALER CARDS [{values[dealer_catds[1][1]]}] : {[dealer_cards[1]]} \n ----->\n")

def show_all(player_cards, dealer_cards):
    print(f" ----->\n PLAYER_CARDS : {player_cards}")
    print(f" DEALER_CARDS : {dealer_cards} \n ----->\n")


# End game Scenarios
def player_bust(obj_h, obj_c):
    if obj_h.value > 21:
        obj_c.loss_bet()
        return True

def player_wins(obj_h, obj_d, obj_c):
    if obj_h.value == 21:
        obj_c.win_bet()
        return True
    elif (obj_h.value > obj_d.value and obj_h.value < 21):
        obj_c.win_bet()
        return True

def dealer_bust(obj_d, obj_h, obj_c):
    if obj_d.value > 21:
        if obj_h.value < 21:
            obj_c.win_bet()
        return True

def dealer_wins(obj_h, obj_d, obj_c):
    if obj_d.value == 21:
        obj_c.loss_bet()
        return True
    elif (obj_d.value > obj_h.value and obj_d.value < 21):
        obj_c.loss_bet()
        return True

def push(obj_h, obj_d):
    if obj_h.value == obj_d.value:
        print("\n "+ 'PUSH'.center(10, '-'))


def greet():
    print(' '+''.center(40, '_'), '|'+''.center(40, ' ')+'|', sep='\n')
    print('|'+'HaNd Of BLaCk_JaCk'.center(40, ' ')+'|', '|'+''.center(40, '_')+'|', sep='\n')


def main():
    greet()
    a = Deck()                                              # Creating a Deck
    c = Chips()                                             # Setting up Chips
    while True:
        
        a.shuffle()                                         # shuffle the deck
        p_cards, d_cards = a.deal_cards()                   # deal cards

        b = Hand()
        b.add_cards(p_cards)                                # Add player cards to extract their values

        print("\n Total money -> ", c.total)
        bet_money = int(input(" Enter Bet amount : "))      # Prompt for bet amount
        c.bet = take_bet(bet_money, c.total)                # New bet amount


        show_some(p_cards, d_cards, b)                      # Show cards (keep dealer one hidden)
        global playing
        while playing:                                      # Recall var. from hit and stand function
            hit_or_stand(a, b, d_cards)                     # Prompt for hit or stand   
            #b.adjust_for_ace()
            if player_bust(b, c):                           # Calling function player bust
                print(str(" -- PLAYER --> BUUUSSTTT"))
                break
        playing = True
        
        if b.value <= 21:                                       # if player hasn't busted
            d = Hand()
            d.add_cards(d_cards)                                # Add dealer cards to extract their values
            while d.value < 17:
                hits(a, d)                                      # Add new cards to dealer pack too
                if dealer_bust(d, b, c):
                    print(str(" -- DEALER --> BUUUSSTTT\n"))
                    break
            show_all(b.cards, d.cards)                          # Show all cards (both player and dealer)

            push(b, d)
            if player_wins(b, d, c):
                print(' '+"PLAYER_WINS".center(20, '-'))
            elif dealer_wins(b, d, c):
                print(' '+"DEALER WINS".center(20, '-'))
        
        ans = str(input(" Play again(YES/NO) : ")).lower()
        if ans != "yes" or c.total < 1:
            if c.total < 1:
                print(" NO MORE MONEY !!! ")
            break
        print('\n'+' '.ljust(30, '-'))
