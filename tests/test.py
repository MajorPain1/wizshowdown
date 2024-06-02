from src.game_state import GameState
from src.player import Player, PlayerDeck
from src.gear import Equipment, Gear, Pet
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
emptyMount = Gear("EmptyMount", EquipmentType.Mount, StatsObject(), [])
emptyPet = Pet("EmptyPet", [])

equipment = Equipment(
    emptyHat,
    emptyRobe,
    emptyBoots,
    emptyWand,
    emptyAthame,
    emptyAmulet,
    emptyRing,
    emptyDeck,
    emptyMount,
    emptyPet,
    []
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

lifeblade = Card(
    name="Lifeblade", 
    objectName="Lifeblade", 
    accuracy=1.00, 
    school=School.Life, 
    rank=0, 
    extraPipReq=[], 
    cardType=CardType.Charm, 
    effects=[Effect(35, School.Life, 0, SpellEffects.modify_outgoing_damage, EffectTarget.friendly_single, Disposition.beneficial, [])],
    isTreasure=False,
    noReshuffle=False,
    discardable=True,
    usable=True,
    trainable=False,
    copyLimit=-1
)

deck1 = PlayerDeck([stormblade], [])
deck2 = PlayerDeck([lifeblade], [])

p1 = Player("Jamal VineRider", equipment, deck1, School.Storm, 170, School.Storm)
p2 = Player("Chris Story", equipment, deck2, School.Life, 170, School.Life)

gamestate = GameState(p1, p2)

def test():
    print(gamestate.player1.deckstate.hand)
    gamestate.turn(p1, gamestate.player1.deckstate.hand[0])
    print(gamestate.player1.deckstate.hand)
    print(gamestate.player1.charms)