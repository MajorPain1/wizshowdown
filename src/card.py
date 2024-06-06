from typing import List, Callable, Any, Tuple

from src.enums import School, CardType, SpellEffects, EffectTarget, Disposition
from src.pips import Pip


class Effect:
    def __init__(
            self,
            param: int,
            school: School,
            rounds: int,
            spelleffect: SpellEffects,
            target: EffectTarget,
            disposition: Disposition,
            condition: Callable,
            conditionValue: Any,
            subeffects: List['Effect']
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


class Card:
    def __init__(
            self, 
            name: str, 
            objectName: str,
            accuracy: float, 
            school: School, 
            rank: int,
            extraPipReq: List[Pip],
            cardType: CardType,
            effects: List[Effect],
            isTreasure: bool,
            noReshuffle: bool,
            discardable: bool,
            trainable: bool,
            copyLimit: int,
            levelReq: int,
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

        if accuracy <= 1 and accuracy >= 0:
            self.accuracy = accuracy

        if rank >= -1 and rank <= 14:
            self.rank = rank

    def __repr__(self) -> str:
        return f"{self.name} [{self.objectName}]"

        