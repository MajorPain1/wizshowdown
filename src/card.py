from typing import List, Callable, Any, Tuple

from src.enums import School, CardType, SpellEffects, EffectTarget, Disposition, CardTarget
from src.pips import Pip


class Effect:
    def __init__(
            self,
            param: int = 0,
            school: School = School.Universal,
            rounds: int = 0,
            spelleffect: SpellEffects = SpellEffects.invalid_spell_effect,
            target: EffectTarget = EffectTarget.invalid_target,
            disposition: Disposition = Disposition.both,
            healModifier: float = 1.0,
            condition: Callable = None,
            conditionValue: Any = None,
            subeffects: List['Effect'] = []
        ):
        self.condition = condition
        self.conditionValue = conditionValue
        self.param = param
        self.school = school
        self.rounds = rounds
        self.spelleffect = spelleffect
        self.target = target
        self.subeffects = subeffects
        self.disposition = disposition
        self.healModifier = healModifier
        
    def fromID(cls, id: int):
        pass # TODO: Implement


class Card:
    def __init__(
            self, 
            name: str, 
            objectName: str,
            accuracy: float = 1, 
            school: School = School.Fire, 
            rank: int = 0,
            extraPipReq: List[Pip] = [],
            cardType: CardType = CardType.Damage,
            effects: List[Effect] = [],
            target: CardTarget = CardTarget.no_target,
            isTreasure: bool = False,
            noReshuffle: bool = False,
            discardable: bool = True,
            trainable: bool = True,
            copyLimit: int = -1,
            levelReq: int = 0,
            ):
        
        self.name = name
        self.objectName = objectName
        self.school = school
        self.extraPipReq = extraPipReq
        self.cardType = cardType
        self.effects = effects
        self.isTreasure = isTreasure
        self.noReshuffle = noReshuffle
        self.discardable = discardable
        self.trainable = trainable
        self.copyLimit = copyLimit
        self.levelReq = levelReq
        self.target = target

        if accuracy <= 1 and accuracy >= 0:
            self.accuracy = accuracy

        if rank >= -1 and rank <= 14:
            self.rank = rank

    def __repr__(self) -> str:
        return f"{self.name} [{self.objectName}]"


class CardToExecute:
    def __init__(self, player, card: Card, targets: List[int]):
        self.player = player
        self.card = card
        self.targets = targets