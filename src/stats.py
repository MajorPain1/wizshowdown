from typing import List

from src.card import Card
from src.enums import School


class SchoolStat:
    def __init__(
            self,
            fire: int = 0,
            ice: int = 0,
            storm: int = 0,
            myth: int = 0,
            life: int = 0,
            death: int = 0,
            balance: int = 0,
            shadow: int = 0,
        ):
        self.fire = fire
        self.ice = ice
        self.storm = storm
        self.myth = myth
        self.life = life
        self.death = death
        self.balance = balance
        self.shadow = shadow

        self.dict = {
            School.Fire: self.fire,
            School.Ice: self.ice,
            School.Storm: self.storm,
            School.Myth: self.myth,
            School.Life: self.life,
            School.Death: self.death,
            School.Balance: self.balance,
            School.Shadow: self.shadow,
        }

    @classmethod
    def sum(cls, ss1: 'SchoolStat', ss2: 'SchoolStat') -> 'SchoolStat':
        fire = ss1.fire + ss2.fire
        ice = ss1.ice + ss2.ice
        storm = ss1.storm + ss2.storm
        myth = ss1.myth + ss2.myth
        life = ss1.life + ss2.life
        death = ss1.death + ss2.death
        balance = ss1.balance + ss2.balance
        shadow = ss1.shadow + ss2.shadow
        return SchoolStat(fire, ice, storm, myth, life, death, balance, shadow)

class StartingPips:
    def __init__(self, powerPips: int = 0, whitePips: int = 0):
        self.powerPips = powerPips
        self.whitePips = whitePips

class StatsObject:
    def __init__(
            self,
            health: int = 0,
            mana: int = 0,
            damage: SchoolStat = SchoolStat(),
            resist: SchoolStat = SchoolStat(),
            accuracy: SchoolStat = SchoolStat(),
            critical: SchoolStat = SchoolStat(),
            block: SchoolStat = SchoolStat(),
            pierce: SchoolStat = SchoolStat(),
            outgoing: int = 0,
            pipConserve: SchoolStat = SchoolStat(),
            powerPipChance: int = 0,
            shadowRating: int = 0,
            archmastery: int = 0,
            startingPips: StartingPips = StartingPips(),
            itemcards: List[Card] = []
        ):
        self.health = health
        self.mana = mana
        self.damage = damage
        self.resist = resist
        self.accuracy = accuracy
        self.critical = critical
        self.block = block
        self.pierce = pierce
        self.outgoing = outgoing
        self.pipConserve = pipConserve
        self.powerPipChance = powerPipChance
        self.shadowRating = shadowRating
        self.archmastery = archmastery
        self.startingPips = startingPips
        self.itemcards = itemcards

    @classmethod
    def sum(cls, so1: 'StatsObject', so2: 'StatsObject') -> 'StatsObject':
        health = so1.health + so2.health
        mana = so1.mana + so2.mana
        damage = SchoolStat.sum(so1.damage, so2.damage)
        resist = SchoolStat.sum(so1.resist, so2.resist)
        accuracy = SchoolStat.sum(so1.accuracy, so2.accuracy)
        critical = SchoolStat.sum(so1.critical, so2.critical)
        block = SchoolStat.sum(so1.block, so2.block)
        pierce = SchoolStat.sum(so1.pierce, so2.pierce)
        outgoing = so1.outgoing + so2.outgoing
        pipConserve = SchoolStat.sum(so1.pipConserve, so2.pipConserve)
        powerPipChance = so1.powerPipChance + so2.powerPipChance
        shadowRating = so1.shadowRating + so2.shadowRating
        archmastery = so1.archmastery + so2.archmastery
        startingPips = StartingPips(powerPips=so1.startingPips.powerPips + so2.startingPips.powerPips, whitePips=so1.startingPips.whitePips + so2.startingPips.whitePips)
        itemcards = so1.itemcards + so2.itemcards

        return StatsObject(health, mana, damage, resist, accuracy, critical, block, pierce, outgoing, pipConserve, powerPipChance, shadowRating, archmastery, startingPips, itemcards)

# TODO
def getBaseStats(school: School, level: int) -> StatsObject:
    return StatsObject(health=2000)
