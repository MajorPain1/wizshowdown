from src.game_state import GameState
from src.player import Player, PlayerDeck, Team
from src.gear import Equipment, Gear, Pet
from src.enums import EquipmentType, School, SpellEffects, EffectTarget, Disposition, CardTarget
from src.stats import StatsObject, SchoolStat, StartingPips
from src.card import Card, Effect, CardType, CardToExecute

emptyHat = Gear("EmptyHat", EquipmentType.Hat, StatsObject(damage=SchoolStat(storm=100), powerPipChance=100), [])
emptyRobe = Gear("EmptyRobe", EquipmentType.Robe, StatsObject(), [])
emptyBoots = Gear("EmptyBoots", EquipmentType.Boots, StatsObject(), [])
emptyWand = Gear("EmptyWand", EquipmentType.Wand, StatsObject(startingPips=StartingPips(1, 1)), [])
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
    target=CardTarget.single,
    isTreasure=False,
    noReshuffle=False,
    discardable=True,
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
    target=CardTarget.single,
    isTreasure=False,
    noReshuffle=False,
    discardable=True,
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
    target=CardTarget.single,
    isTreasure=False,
    noReshuffle=False,
    discardable=True,
    trainable=False,
    copyLimit=-1
)

deck1 = PlayerDeck([stormblade, thundersnake], [])
deck2 = PlayerDeck([lifeblade], [])

p1 = Player("Jamal VineRider", equipment, deck1, School.Storm, 170, School.Storm)
p2 = Player("Chris Story", equipment, deck2, School.Life, 170, School.Life)

t1 = Team()
t1.addTeamMember(p1)
t2 = Team()
t2.addTeamMember(p2)

gamestate = GameState(t1, t2)

def test():
    teams_up = t1
    while True:
        print(gamestate)
        # Team 1's turn
        cards_to_execute = []
        for slot in teams_up.slots:
            if slot == None:
                continue
            
            print(f"{slot.name}'s turn")
            print(f"{slot.deckstate.hand}")
            card_i = int(input("Give index of card to use: "))
            card = slot.deckstate.hand[card_i]
            targets = []
            match card.target:
                case CardTarget.no_target:
                    pass
                
                case CardTarget.single:
                    targets.append(int(input("What index targets? ")))
                    
                case CardTarget.team:
                    for i in range(4):
                        targets.append(i)
                        
                case CardTarget.team:
                    for i in range(4):
                        targets.append(i)
                        
                case CardTarget.multi_target:
                    inp = input("What index targets? (q to exit): ")
                    while inp != "q":
                        targets.append(int(inp))
                        inp = input("What index targets? (q to exit): ")

            targets = list(set(targets))
            cards_to_execute.append(CardToExecute(slot, card, targets))
        
        for cardtoexecute in cards_to_execute:
            cardtoexecute: CardToExecute
            gamestate.turn(cardtoexecute.player, cardtoexecute.card, cardtoexecute.targets)
        
        teams_up = teams_up.opponentTeam
        
if __name__ == "__main__":
    test()