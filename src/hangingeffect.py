from typing import List

from src.player import Player
from src.enums import School, SpellEffects, Disposition

def reverseDisposition(disposition: Disposition):
    match disposition:
        case Disposition.both:
            return Disposition.both
        case Disposition.harmful:
            return Disposition.beneficial
        case Disposition.beneficial:
            return Disposition.harmful

class DispositionEffect:
    def __init__(self, owner: Player, disposition: Disposition):
        self.owner = owner
        self.disposition = disposition

    def getDisposition(self, player: Player):
        if player == self.owner:
            return self.disposition
        else:
            return reverseDisposition(self.disposition)

class Charm(DispositionEffect):
    def __init__(self, objectName: str, owner: Player, param: int, school: School, spellEffect: SpellEffects, disposition: Disposition):
        super().__init__(owner, disposition)
        self.objectName = objectName
        self.spellEffect = spellEffect
        self.used = False
        self.param = param
        self.school = school

class Ward(DispositionEffect):
    def __init__(self, objectName: str, owner: Player, param: int, school: School, spellEffect: SpellEffects, disposition: Disposition):
        super().__init__(owner, disposition)
        self.objectName = objectName
        self.spellEffect = spellEffect
        self.param = param
        self.school = school
        self.disposition = disposition

class Overtime(DispositionEffect):
    def __init__(self, owner: Player, param: int, school: School, rounds: int, spellEffect: SpellEffects, disposition: Disposition):
        super().__init__(owner, disposition)
        self.spellEffect = spellEffect
        self.param = param
        if spellEffect != SpellEffects.deferred_damage:
            self.param = self.param / rounds
        self.school = school
        self.rounds = rounds

    def tick(self):
        self.rounds -= 1
        return self.param

class Bubble:
    def __init__(self, objectName: str, owner: Player, param: int, school: School, spellEffect: SpellEffects, disposition: Disposition):
        self.objectName = objectName
        self.owner = owner
        self.spellEffect = spellEffect
        self.param = param
        self.school = school
        self.disposition = disposition

class Aura:
    def __init__(self, objectName: str, owner: Player, param: int, school: School, spellEffect: SpellEffects, disposition: Disposition):
        self.objectName = objectName
        self.owner = owner
        self.spellEffect = spellEffect
        self.param = param
        self.school = school
        self.disposition = disposition

