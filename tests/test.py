from src.game_state import GameState
from src.player import Player, PlayerDeck
from src.gear import Equipment, Gear
from src.enums import EquipmentType, School, SpellEffects, EffectTarget, Disposition
from src.stats import StatsObject
from src.card import Card, Effect, CardType

emptyHat = Gear("EmptyHat", EquipmentType.Hat, StatsObject(), [])
emptyRobe = Gear("EmptyRobe", EquipmentType.Robe, StatsObject(), [])
emptyBoots = Gear("EmptyBoots", EquipmentType.Boots, StatsObject(), [])
emptyWand = Gear("EmptyWand", EquipmentType.Wand, StatsObject(), [])
emptyAthame = Gear("EmptyAthame", EquipmentType.Athame, StatsObject(), [])
emptyAmulet = Gear("EmptyAmulet", EquipmentType.Amulet, StatsObject(), [])
emptyRing = Gear("EmptyRing", EquipmentType.Ring, StatsObject(), [])
emptyDeck = Gear("EmptyDeck", EquipmentType.Deck, StatsObject(), [])

equipment = Equipment(
    emptyHat,
    emptyRobe,
    emptyBoots,
    emptyWand,
    emptyAthame,
    emptyAmulet,
    emptyRing,
    emptyDeck
)

stormblade = Card(
    name="Stormblade", 
    objectName="Stormblade", 
    accuracy=1.00, 
    school=School.Storm, 
    rank=0, 
    extraPipReq=[], 
    cardType=CardType.Charm, 
    effects=[Effect(35, School.Storm, 0, SpellEffects.modify_outgoing_damage, EffectTarget.friendly_single, Disposition.beneficial, [])],
    isTreasure=False,
    noReshuffle=False,
    discardable=True,
    usable=True,
    trainable=False,
    copyLimit=-1
)

deck = PlayerDeck([stormblade])

p1 = Player("Jamal AirFinder", equipment, deck, School.Storm, 170, School.Storm)

def test():
