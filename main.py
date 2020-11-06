import random

class Card(object):
    def __init__(self, name, value, suit, symbol):
        self.value = value
        self.suit = suit
        self.name = name
        self.symbol = symbol
        self.showing = False

    def __repr__(self):
        if self.showing:
            return self.symbol
        else:
            return "Carte"


class Deck(object):
    def shuffle(self, times=1):
        random.shuffle(self.cards)
        print("Jeu distribué")

    def deal(self):
        return self.cards.pop(0)


class StandardDeck(Deck):
    def __init__(self):
        self.cards = []
        suits = {"Hearts": "H", "Spades": "S", "Diamonds": "D", "Clubs": "C"}
        values = {"Two": 2,
                  "Three": 3,
                  "Four": 4,
                  "Five": 5,
                  "Six": 6,
                  "Seven": 7,
                  "Eight": 8,
                  "Nine": 9,
                  "Ten": 10,
                  "Jack": 11,
                  "Queen": 12,
                  "King": 13,
                  "Ace": 14}

        for name in values:
            for suit in suits:
                symbolIcon = suits[suit]
                if values[name] < 11:
                    symbol = str(values[name]) + symbolIcon
                else:
                    symbol = name[0] + symbolIcon
                self.cards.append(Card(name, values[name], suit, symbol))

    def __repr__(self):
        return "Jeu de cartes standard:{0} restantes".format(len(self.cards))


class Player(object):
    def __init__(self):
        self.cards = []

    def cardCount(self):
        return len(self.cards)

    def addCard(self, card):
        self.cards.append(card)


class PokerScorer(object):
    def __init__(self, cards):
        # Number of cards
        if not len(cards) == 5:
            return "Erreur: Mauvais nombre de cartes"

        self.cards = cards

    def flush(self):
        suits = [card.suit for card in self.cards]
        if len(set(suits)) == 1:
            return True
        return False

    def straight(self):
        values = [card.value for card in self.cards]
        values.sort()

        if not len(set(values)) == 5:
            return False

        if values[4] == 14 and values[0] == 2 and values[1] == 3 and values[2] == 4 and values[3] == 5:
            return 5

        else:
            if not values[0] + 1 == values[1]: return False
            if not values[1] + 1 == values[2]: return False
            if not values[2] + 1 == values[3]: return False
            if not values[3] + 1 == values[4]: return False

        return values[4]

    def highCard(self):
        values = [card.value for card in self.cards]
        highCard = None
        for card in self.cards:
            if highCard is None:
                highCard = card
            elif highCard.value < card.value:
                highCard = card

        return highCard

    def highestCount(self):
        count = 0
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) > count:
                count = values.count(value)

        return count

    def pairs(self):
        pairs = []
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 2 and value not in pairs:
                pairs.append(value)

        return pairs

    def square(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 4:
                return True

    def full(self):
        two = False
        three = False

        values = [card.value for card in self.cards]
        if values.count(values) == 2:
            two = True
        elif values.count(values) == 3:
            three = True

        if two and three:
            return True

        return False



def videoPoker():
    player = Player()

    print("Saisissez votre montant initial:")
    # Montant initial
    points = int(input())

    end = False
    while not end:
        print("Vous avez {0} points".format(points))
        print()
        print("Saisissez votre mise:")
        handCost = int(input())
        points -= handCost

        ## Mélange et distribution
        deck = StandardDeck()
        deck.shuffle()
        for i in range(5):
            player.addCard(deck.deal())

        # Afficher jeu
        for card in player.cards:
            card.showing = True

        print(player.cards)

        validInput = False
        while not validInput:
            print("Quelles cartes voulez vous échanger? ( ex. 1, 2, 3 )")
            print("*Taper Entree pour toutes les garder, taper exit pour quitter")
            inputStr = input()

            if inputStr == "exit":
                end = True
                break

            try:
                inputList = [int(inp.strip()) for inp in inputStr.split(",") if inp]

                for inp in inputList:
                    if inp > 6:
                        continue
                    if inp < 1:
                        continue

                for inp in inputList:
                    player.cards[inp - 1] = deck.deal()
                    player.cards[inp - 1].showing = True

                validInput = True
            except:
                print("")
                print("Erreur de saisie: utiliser les virgules pour separer les cartes que vous voulez changer")

        print(player.cards)
        # Score
        score = PokerScorer(player.cards)
        straight = score.straight()
        flush = score.flush()
        highestCount = score.highestCount()
        pairs = score.pairs()

        # Quinte Flush Royale
        if straight and flush and straight == 14:
            print("Quinte Flush Royale!!!")
            print("+" + str(250*handCost))
            points += 250*handCost

        # Quinte flush
        elif straight and flush:
            print("Quinte flush!")
            print("+" + str(50*handCost))
            points += 50*handCost

        # Carré
        elif score.square():
            print("Carré!")
            print("+" + str(25*handCost))
            points += 25*handCost

        # Full
        elif score.full():
            print("Full!")
            print("+" + str(9*handCost))
            points += 9*handCost

        # Flush
        elif flush:
            print("Flush!")
            print("+" + str(6*handCost))
            points += 6*handCost

        # Quinte
        elif straight:
            print("Quinte!")
            print("+" + str(4*handCost))
            points += 4*handCost

        # Brelan
        elif highestCount == 3:
            print("Brelan!")
            print("+" + str(3*handCost))
            points += 3*handCost

        # Double Paire
        elif len(pairs) == 2:
            print("Double Paire!")
            print("+" + str(2*handCost))
            points += 2*handCost

        # Paire
        elif pairs and pairs[0] > 10:
            print("Paire!")
            print("+" + str(handCost))
            points += handCost

        # Perdu
        else:
            print("Pas de chance, c'est perdu!")

        player.cards = []

        print()
        print("------------------requirements.txt-----------------")
        print()

if __name__ == "__main__":
    videoPoker()