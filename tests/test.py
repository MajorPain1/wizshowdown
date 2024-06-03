from src.game_state import GameState
from src.player import Player, PlayerDeck
from src.gear import Equipment, Gear, Pet
from src.enums import EquipmentType, School, SpellEffects, EffectTarget, Disposition
from src.stats import StatsObject, SchoolStat
from src.card import Card, Effect, CardType

emptyHat = Gear("EmptyHat", EquipmentType.Hat, StatsObject(damage=SchoolStat(storm=100), powerPipChance=70), [])
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

thundersnake = Card(
    name="Thundersnake", 
    objectName="Thundersnake", 
    accuracy=1.00, 
    school=School.Storm, 
    rank=1, 
    extraPipReq=[], 
    cardType=CardType.Damage, 
    effects=[Effect(125, School.Storm, 0, SpellEffects.damage, EffectTarget.enemy_single, Disposition.beneficial, [])],
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

deck1 = PlayerDeck([stormblade, thundersnake], [])
deck2 = PlayerDeck([lifeblade], [])

p1 = Player("Jamal VineRider", equipment, deck1, School.Storm, 170, School.Storm)
p2 = Player("Chris Story", equipment, deck2, School.Life, 170, School.Life)

gamestate = GameState(p1, p2)

def test():
    print("P1 has 100 Storm Damage Hat equipped")
    print("Turn 1")
    print(f"P1 Hand: {gamestate.player1.deckstate.hand}")
    print(f"P1 Pips: {gamestate.player1.pips.pips}")
    print(f"P2 HP: {gamestate.player2.current_hp}")
    blade = gamestate.player1.deckstate.getCardInHand("Stormblade")
    print("Using card Stormblade")
    gamestate.turn(p1, blade)
    print("\n")
    print("Turn 2 (skipped p2's turn)")
    print(f"P1 Hand: {gamestate.player1.deckstate.hand}")
    print(f"P1 Charms: {gamestate.player1.charms}")
    print(f"P1 Pips: {gamestate.player1.pips.pips}")
    snake = gamestate.player1.deckstate.getCardInHand("Thundersnake")
    print("Using Card Thundersnake (125 Storm Damage)")
    gamestate.turn(p1, snake)
    print("\n")
    print("Turn 3")
    print(f"P1 Hand: {gamestate.player1.deckstate.hand}")
    print(f"P1 Charms: {gamestate.player1.charms}")
    print(f"P1 Pips: {gamestate.player1.pips.pips}")
    print(f"P2 HP: {gamestate.player2.current_hp}")
    print("\n")
    print("500 - 125 * 1.35 * 2.0 = 162.5")