from typing import List
from random import shuffle

from src.card import Card

class DeckState:
    def __init__(
            self,
            mainDeck: List[Card],
            treasureCards: List[Card],
        ):
        self.mainDeck: List[Card] = mainDeck[:64]
        self.treasureCards: List[Card] = treasureCards[:36]
        self.hand: List[Card] = []
        self.usedCards: List[Card] = []
        self.discards: List[Card] = []

        shuffle(self.mainDeck)
        shuffle(self.treasureCards)

        for _ in range(7):
            if len(self.mainDeck) > 0:
                self.hand.append(self.mainDeck.pop())

    def drawTC(self):
        if len(self.hand) >= 7 or len(self.treasureCards) == 0:
            return
        tc = self.treasureCards.pop()
        tc.discardable = False
        self.hand.insert(0, tc)

    def drawMain(self):
        while len(self.hand) < 7:
            if len(self.mainDeck) == 0:
                break
            
            self.hand.insert(0, self.mainDeck.pop())

    def discardCard(self, index: int):
        if index < 0 or index > 6:
            return
        
        self.discards.append(self.hand.pop(index))

    def useCard(self, index: int) -> Card:
        if index < 0 or index > 6:
            return None
        
        card_to_cast = self.hand.pop(index)
        self.usedCards.append(card_to_cast)
        return card_to_cast

    def addCardToTop(self, card: Card):
        self.mainDeck.append(card)

    def reshuffle(self):
        for card in self.usedCards:
            if card.isTreasure or card.noReshuffle:
                continue
            else:
                self.mainDeck.append(card)

        for card in self.discards:
            if card.noReshuffle:
                continue
            elif card.isTreasure:
                self.treasureCards.append(card)
            else:
                self.mainDeck.append(card)


        self.usedCards = []
        self.discards = []

        shuffle(self.mainDeck)
        shuffle(self.treasureCards)

    def setAllHandToDiscardable(self):
        for card in self.hand:
            card.discardable = True

    def getCardInHand(self, objectName: str):
        for card in self.hand:
            if card.objectName == objectName:
                return card
