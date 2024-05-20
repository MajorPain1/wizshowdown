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
        jewel_stats = None
        for jewel in jewels:
            StatsObject.sum(jewel_stats, jewel.stats)

        self.stats = StatsObject.sum(
            StatsObject.sum(
                StatsObject.sum(
                    StatsObject.sum(self.hat.stats, self.robe.stats), 
                    StatsObject.sum(self.boots.stats, self.wand.stats)
                ),
                StatsObject.sum(
                    StatsObject.sum(self.athame.stats, self.amulet.stats),
                    StatsObject.sum(self.ring.stats, self.deck.stats)
                )
            ),
            StatsObject.sum(self.mount.stats,jewel_stats)
        )
