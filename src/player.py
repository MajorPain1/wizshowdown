from typing import List
from random import randint, uniform

from src.card import Card
from src.deck_state import DeckState
from src.gear import Equipment
from src.enums import School
from src.stats import StatsObject
from src.hangingeffect import Charm, Ward, Overtime
from src.pips import Pip, PipArray
from src.object_data import getBaseStats

class PlayerDeck:
    def __init__(self, mainDeck: List[Card], treasureCards: List[Card]):
        self.mainDeck = mainDeck[:64]
        self.treasureCards = treasureCards[:36]

    def addCards(self, cards: List[Card]):
        for card in cards:
            self.mainDeck.append(card)

class Player:
    def __init__(
            self,
            name: str,
            equipment: Equipment,
            deck: PlayerDeck,
            school: School,
            level: int,
            selectedArch: School,
        ):
        self.name = name
        self.equipment = equipment
        self.deck = deck
        self.school = school
        self.level = level
        self.deckstate = DeckState(self.deck.mainDeck, self.deck.treasureCards)
        self.charms = []
        self.wards = []
        self.overtimes = []
        self.auraObjectName = None
        self.auraEffects = []
        self.stunned = False
        self.selectedArch: School = selectedArch
        self.outgoingDamageEffects = (-1.0, -1, -1)
        self.outgoingHealModifier = -1.0
        self.win = False
        self.opponent: Player = None

        self.stats = StatsObject.sum(getBaseStats(level=level, school=school), equipment.stats)

        self.current_hp = self.stats.health
        self.power_pips = self.stats.startingPips.powerPips
        self.white_pips = self.stats.startingPips.whitePips
        self.pips: PipArray

        self.addRoundPip()


        self.deck.addCards(self.stats.itemcards)

    def updateHP(self, num):
        if num + self.current_hp > self.stats.health:
            self.current_hp = self.stats.health
        else:
            self.current_hp = num + self.current_hp

    def updatePips(self, rank: int, extraPipReq: List[Pip], cardSchool: School):
        self.pips.subtractPips(rank, extraPipReq, cardSchool, self.school, self.stats.pipConserve.dict[cardSchool])
        

    def addRoundPip(self):
        self.pips.archmastery += self.stats.archmastery / self.opponent.stats.archmastery
        
        # Shadow Pips
        if len(self.pips.shadow_pips) < 2:
            self.pips.shadow_guage += uniform(self.stats.shadowRating*0.75, self.stats.shadowRating) / (self.opponent.stats.shadowRating*5)
            if self.pips.shadow_guage >= 1.0:
                self.pips.shadow_pips.append(Pip(isPower=True, school=School.Shadow))

        # Reg Pips
        if randint(0, 100) < self.stats.powerPipChance:
            if self.pips.archmastery >= 1.0:
                self.pips.pips.append(Pip(isPower=True, school=self.selectedArch))
                self.pips.archmastery = 0.0
            else:
                self.pips.pips.append(Pip(isPower=True, school=School.Universal))
        else:
            self.pips.pips.append(Pip(isPower=False, school=School.Universal))

        self.pips.orderPips()
        