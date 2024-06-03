from typing import List

from src.enums import EquipmentType, JewelType
from src.stats import StatsObject


class Jewel:
    def __init__(
            self,
            name: str,
            jewelType: JewelType,
            stats: StatsObject,
        ):
        self.name = name
        self.jewelType = jewelType
        self.stats = stats

class Talent:
    def __init__(
            self,
            name: str,
            stats: StatsObject,
        ):
        self.name = name
        self.stats = stats

class Pet:
    def __init__(
            self,
            name: str,
            talents: List[Talent],
        ):
            self.name = name
            self.talents = talents

class Gear:
    def __init__(
            self,
            name: str,
            equipmentType: EquipmentType,
            stats: StatsObject,
            jeweltypes: List[JewelType],
        ):
            self.name = name
            self.equipmentType = equipmentType
            self.stats = stats
            self.jeweltypes = jeweltypes

class Equipment:
    def __init__(
            self,
            hat: Gear,
            robe: Gear,
            boots: Gear,
            wand: Gear,
            athame: Gear,
            amulet: Gear,
            ring: Gear,
            deck: Gear,
            mount: Gear,
            pet: Pet,
            jewels: List[Jewel]
        ):
        self.hat = hat
        self.robe = robe
        self.boots = boots
        self.wand = wand
        self.athame = athame
        self.amulet = amulet
        self.ring = ring
        self.deck = deck
        self.mount = mount
        self.pet = pet

        # TODO: Add check for number of jewel types
        self.jewels = jewels

        self.stats = StatsObject()
        self.updateStats()

    def updateStats(self):
        sumStats = StatsObject()

        for jewel in self.jewels:
            sumStats = StatsObject.sum(sumStats, jewel.stats)
        
        for talent in self.pet.talents:
            sumStats = StatsObject.sum(talent.stats, sumStats)

        if self.hat != None:
            sumStats = StatsObject.sum(self.hat.stats, sumStats)
        if self.robe != None:
            sumStats = StatsObject.sum(self.robe.stats, sumStats)
        if self.boots != None:
            sumStats = StatsObject.sum(self.boots.stats, sumStats)
        if self.wand != None:
            sumStats = StatsObject.sum(self.wand.stats, sumStats)
        if self.athame != None:
            sumStats = StatsObject.sum(self.athame.stats, sumStats)
        if self.amulet != None:
            sumStats = StatsObject.sum(self.amulet.stats, sumStats)
        if self.ring != None:
            sumStats = StatsObject.sum(self.ring.stats, sumStats)
        if self.deck != None:
            sumStats = StatsObject.sum(self.deck.stats, sumStats)
        if self.mount != None:
            sumStats = StatsObject.sum(self.mount.stats, sumStats)
        
        self.stats = sumStats

    def equipItem(self, gear: Gear):
        match gear.equipmentType:
            case EquipmentType.Hat:
                self.hat = gear
            case EquipmentType.Robe:
                self.robe = gear
            case EquipmentType.Boots:
                self.boots = gear
            case EquipmentType.Wand:
                self.wand = gear
            case EquipmentType.Athame:
                self.athame = gear
            case EquipmentType.Amulet:
                self.amulet = gear
            case EquipmentType.Ring:
                self.ring = gear
            case EquipmentType.Deck:
                self.deck = gear
            case EquipmentType.Mount:
                self.mount = gear

        self.updateStats()

    def equipItem(self, gears: List[Gear]):
        for gear in gears:
            self.equipItem(gear)
