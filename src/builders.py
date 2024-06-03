from typing import List
from operator import attrgetter

from src.card import Card
from src.player import PlayerDeck


class DeckBuilder:
    def __init__(self, mainDeck: List[Card] = [], treasureCards: List[Card] = []):
        self.mainDeck = mainDeck
        self.treasureCards = treasureCards

    def loadDeck(self, mainDeck, treasureCards):
        self.mainDeck = mainDeck
        self.treasureCards = treasureCards

    def getDeck(self):
        return PlayerDeck(self.mainDeck, self.treasureCards)

    def orderDeck(self):
        self.mainDeck = sorted(self.mainDeck, key=attrgetter('school', 'rank', 'name'))
        self.treasureCards = sorted(self.treasureCards, key=attrgetter('school', 'rank', 'name'))

    def addCardToDeck(self, card: Card):
        if not card.isTreasure:
            deck = self.mainDeck
            if len(deck) >= 64:
                return
        else:
            deck = self.treasureCards
            if len(deck) >= 36:
                return
            
        if self.getCopiesOfCard(card) >= card.copyLimit:
            return
        
        deck.append(card)
        self.orderDeck()

    def removeCardFromDeck(self, index: int, tc: bool = False):
        if tc:
            if index <= 36:
                self.treasureCards.pop(index)
        else:
            if index <= 64:
                self.mainDeck.pop(index)
            

    def getCopiesOfCard(self, card: Card) -> int:
        copies = 0
        if card.isTreasure:
            return
        
        for c in self.mainDeck:
            if c.objectName == card.objectName:
                copies += 1
        
        return 
