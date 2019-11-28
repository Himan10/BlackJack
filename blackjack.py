import random
from os import system, name

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
VALUES = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}
PLAYING = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    """ Creating a Deck of cards and
    Deal two cards to both player and dealer. """
    
    def __init__(self):
        self.deck = []
        self.player = []
        self.dealer = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append((suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        self.player = random.sample(self.deck, 2)
        self.delete_cards(self.player)
        self.dealer = random.sample(self.deck, 2)
        self.delete_cards(self.dealer)  # Delete Drawn Cards
        return self.player, self.dealer

    def delete_cards(self, total_drawn):
        """ Delete Drawn cards from the Decks """
        
        try:
            for i in total_drawn:
                self.deck.remove(i)
        except ValueError:
            pass


class Hand:
    """ Adding the values of player/dealer cards 
    and change the values of Aces acc. to situation. """
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_cards(self, card):
        self.cards.extend(card)
        for count, ele in enumerate(card, 0):
            self.adjust_for_ace()
            self.value += VALUES[ele[1]]

    def adjust_for_ace(self):
        if self.cards[0][1] == "Ace" or self.cards[1][1] == "Ace":
            if (21 - self.value) >= 11:
                VALUES["Ace"] = 11
            else:
                VALUES["Ace"] = 1
        self.aces += 1


class Chips:
    """ Player/dealer chips for making bets
    and Adding/Deducting amount in/from Player's total. """
    
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


def blackj_options(p_chips, obj_de, obj_h, dealer_card):
    global PLAYING
    choice = str(input("[ HIT | STAND | SURRENDER | DOUBLE ] : ")).lower()
    print("\n")
    if choice == "hit":
        hits(obj_de, obj_h)
        show_some(obj_h.cards, dealer_card, obj_h)

    elif choice == "stand":
        PLAYING = False

    elif choice == "surrender":
        p_chips.bet = p_chips.bet // 2
        PLAYING = False
        obj_h.value += 21

    elif choice == "double":
        if p_chips.bet * 2 <= p_chips.total:
            p_chips.bet *= 2
            hits(obj_de, obj_h)
            PLAYING = False
        else:
            print(" --You can't Double Down, Money isn't Enough--")
    else:
        print(" --Invalid Choice--")


def show_some(player_cards, dealer_cards, obj_h):
    print(f" ----->\n PLAYER CARDS [{obj_h.value}] : {player_cards}")
    print(
        f" DEALER CARDS [{VALUES[dealer_cards[1][1]]}] : {[dealer_cards[1]]} \n ----->\n"
    )


def show_all(player_cards, dealer_cards, obj_h, obj_d):
    print(f" ----->\n PLAYER_CARDS [{obj_h.value}] : {player_cards}")
    print(f" DEALER_CARDS [{obj_d.value}] : {dealer_cards} \n ----->\n")


########################################
# End game Scenarios


def player_bust(obj_h, obj_c):
    if obj_h.value > 21:
        obj_c.loss_bet()
        return True
    return False


def player_wins(obj_h, obj_d, obj_c):
    if any((obj_h.value == 21, obj_h.value > obj_d.value and obj_h.value < 21)):
        obj_c.win_bet()
        return True
    return False


def dealer_bust(obj_d, obj_h, obj_c):
    if obj_d.value > 21:
        if obj_h.value < 21:
            obj_c.win_bet()
        return True
    return False


def dealer_wins(obj_h, obj_d, obj_c):
    if any((obj_d.value == 21, obj_d.value > obj_h.value and obj_d.value < 21)):
        obj_c.loss_bet()
        return True
    return False


def push(obj_h, obj_d):
    if obj_h.value == obj_d.value:
        return True
    return False


def player_surrender(obj_c):
    obj_c.loss_bet()
    return True


#######################################


def clear_screen():
    system("cls" if name == "nt" else "clear")


def greet():
    print(" " + "".center(40, "_"), "|" + "".center(40, " ") + "|", sep="\n")
    print(
        "|" + "HaNd Of BLaCk_JaCk".center(40, " ") + "|",
        "|" + "".center(40, "_") + "|",
        sep="\n",
    )


def greet2(p_count, d_count, draw_c):
    print(" " + "".center(30, "_"))
    print(
        "|" + "__PLAYER__".ljust(7, " ") + "|",
        "_DEALER__".center(7, " ") + "|",
        "_DRAW__".rjust(7, " ") + "|",
        sep="_",
    )
    print(
        "|"
        + "".center(10, " ")
        + "|"
        + "".center(10, " ")
        + "|"
        + "".center(8, " ")
        + "|"
    )
    print(
        "|"
        + p_count.center(10, "_")
        + "|"
        + d_count.center(10, "_")
        + "|"
        + draw_c.center(8, "_")
        + "|"
    )


def main():
    p_win, d_win, draw = 0, 0, 0
    greet()
    p_chips = Chips()
    while True:
        cards_deck = Deck()
        cards_deck.shuffle()
        p_cards, d_cards = cards_deck.deal_cards()
        p_hand = Hand()
        p_hand.add_cards(p_cards)
        print("\n Total money -> ", p_chips.total)
        bet_money = int(input(" Enter Bet amount : "))
        p_chips.bet = take_bet(bet_money, p_chips.total)
        print("\n")

        show_some(p_cards, d_cards, p_hand)
        global PLAYING
        while PLAYING:  # Recall var. from hit and stand function
            blackj_options(p_chips, cards_deck, p_hand, d_cards)
            if player_bust(p_hand, p_chips):
                d_win += 1
                print("\n -- PLAYER --> BUUUSSTTT")
                break

        PLAYING = True

        if p_hand.value <= 21:
            d_hand = Hand()
            d_hand.add_cards(d_cards)
            while d_hand.value < 17:
                hits(cards_deck, d_hand)
                if dealer_bust(d_hand, p_hand, p_chips):
                    p_win += 1
                    print("\n -- DEALER --> BUUUSSTTT\n")
                    break
            show_all(p_hand.cards, d_hand.cards, p_hand, d_hand)

            if push(p_hand, d_hand):
                draw += 1
                print("\n " + " PUSH ".center(12, "-"))
            elif player_wins(p_hand, d_hand, p_chips):
                p_win += 1
                print(" " + " PLAYER_WINS ".center(22, "-"))
            elif dealer_wins(p_hand, d_hand, p_chips):
                d_win += 1
                print(" " + " DEALER WINS ".center(22, "-"))

        else:
            print("\n " + " DEALER WINS ".center(22, "-"))

        print(f"\n >>> Available Money >>> {p_chips.total} \n")
        
        ans = str(input(" Play again(YES/NO) : ")).lower()
        if ans != "yes" or p_chips.total < 1:
            if p_chips.total < 1:
                print(" NO MORE MONEY !!! ")
            break
        clear_screen()
        greet2(str(p_win), str(d_win), str(draw))  # Score board location -> Top
        print("\n" + " ".ljust(30, "-"))

        
main()
