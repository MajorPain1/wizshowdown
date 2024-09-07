from typing import List
from random import randint, uniform

from src.card import Card
from src.deck_state import DeckState
from src.gear import Equipment
from src.enums import School
from src.stats import StatsObject, getBaseStats
from src.pips import Pip, PipArray

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
        self.team: Team = None

        self.stats = StatsObject.sum(getBaseStats(level=level, school=school), equipment.stats)

        self.current_hp = self.stats.health

        self.power_pips = self.stats.startingPips.powerPips
        self.white_pips = self.stats.startingPips.whitePips
        self.pips = PipArray()
        print(self.name)
        self.pips.addPips((self.power_pips*2 + self.white_pips), self.stats.pipConserve)


        self.deck.addCards(self.stats.itemcards)

    def updateHP(self, num):
        if num + self.current_hp > self.stats.health:
            self.current_hp = self.stats.health
        else:
            self.current_hp = num + self.current_hp

    def updatePips(self, rank: int, extraPipReq: List[Pip], cardSchool: School):
        self.pips.subtractPips(rank, extraPipReq, cardSchool, self.school, self.stats.pipConserve.dict[cardSchool])
        

    def addRoundPip(self):
        # Archmastery
        deckEff = len(self.deck.mainDeck) / 64
        if self.team.opponentTeam.maxArch > 0:
            self.pips.archmastery += (self.stats.archmastery / self.team.opponentTeam.maxArch) * deckEff
        else:
            self.pips.archmastery = 1.0 * deckEff
        
        # Shadow Pips
        if len(self.pips.shadow_pips) < 2:

            if self.stats.shadowRating == 0:
                self.stats.shadowRating = 90
            if self.team.opponentTeam.maxShad == 0:
                self.team.opponentTeam.maxShad = 90

            self.pips.shadow_guage += uniform(self.stats.shadowRating*0.75, self.stats.shadowRating) / (self.team.opponentTeam.maxShad*5)
            if self.pips.shadow_guage >= 1.0:
                self.pips.addShadowPips(1)

        # Reg Pips
        if randint(0, 99) < self.stats.powerPipChance:
            if self.pips.archmastery >= 1.0:
                self.pips.addPips(2, self.stats.pipConserve, school=self.selectedArch)
                self.pips.archmastery = 0.0
            else:
                self.pips.addPips(2, self.stats.pipConserve, school=School.Universal)
        else:
            self.pips.addPips(1, self.stats.pipConserve)

        self.pips.orderPips()
        
        
    def __repr__(self) -> str:
        return f"{self.name} {self.school} {self.level}\n{self.current_hp=} {self.pips=}\n{self.charms=} {self.wards=}\n{self.overtimes=} {self.auraEffects=}"

class Team:
    def __init__(
            self,
            slot0: Player = None,
            slot1: Player = None,
            slot2: Player = None,
            slot3: Player = None,
    ):
        self.slots = [slot0, slot1, slot2, slot3]
        
        for slot in self.slots:
            if slot != None:
                slot.team = self

        self.opponentTeam: Team = None

        self.maxArch = 0
        self.maxShad = 0
        self._calc_maxArch()
        self._calc_maxShad()
        
        self.bubbleObjectName = None
        self.bubbleEffects = []
        
        self.win = False

    def _calc_maxArch(self):
        for slot in self.slots:
            if slot != None and slot.stats.archmastery > self.maxArch:
                self.maxArch = slot.stats.archmastery

    def _calc_maxShad(self):
        for slot in self.slots:
            if slot != None and slot.stats.shadowRating > self.maxShad:
                self.maxShad = slot.stats.shadowRating

    def addRoundPip(self):
        for slot in self.slots:
            if slot != None:
                slot.addRoundPip()

    def addTeamMember(self, player: Player) -> bool:
        for i, slot in enumerate(self.slots):
            if slot == None:
                player.team = self
                self.slots[i] = player
                self._calc_maxArch()
                self._calc_maxShad()
                return True
        return False

    def removeTeamMember(self, player: Player) -> bool:
        for i, slot in enumerate(self.slots):
            if slot == player:
                player.team = None
                self.slots[i] = None
                self._calc_maxArch()
                self._calc_maxShad()
                return True
        return False
    
    def __repr__(self) -> str:
        return f"{self.slots[0]}\t{self.slots[1]}\t{self.slots[2]}\t{self.slots[3]}\n"