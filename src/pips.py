from typing import List
from random import randint

from src.enums import School

schoolPipOrdering = {
    School.Balance: 0,
    School.Death: 1,
    School.Fire: 2,
    School.Ice: 3,
    School.Life: 4,
    School.Myth: 5,
    School.Storm: 6,
}

class Pip:
    def __init__(self, isPower: bool, school: School):
        self.isPower = isPower
        self.school = school

    def __eq__(self, other):
        return self.isPower == other.isPower and self.school == other.school

class PipArray:
    def __init__(self, pips: List[Pip], shadow_pips: List[Pip]):
        self.pips = pips
        self.shadow_pips = shadow_pips
        self.archmastery = 0
        self.shadow_guage = 0

    def orderPips(self):
        whitePips: List[Pip] = []
        # White pips in front
        for pip in self.pips:
            if not pip.isPower:
                whitePips.append(pip)
                self.pips.remove(pip)

        schoolPips = sorted(self.pips, key=lambda pip:schoolPipOrdering[pip.school])
        self.pips = whitePips + schoolPips

    def sumTotalValue(self) -> int:
        total = 0
        for pip in self.pips:
            if pip.isPower:
                total += 2
            else:
                total += 1
        return total

    def convertPowerPip(self, school: School):
        for pip in self.pips:
            if pip.isPower:
                pip.school = school
                return
            
    def convertWhiteToPower(self):
        for pip in self.pips:
            if not pip.isPower:
                pip.isPower = True
                self.orderPips()
                return
            
    def destroyPips(self, num: int):
        while num > 1 and len(self.pips) > 0:
            destroyedPip = self.pips.pop()
            if destroyedPip.isPower:
                num -= 2
            else:
                num -= 1

        if num == 1 and len(self.pips) > 0:
            if self.pips[0].isPower:
                self.pips[0].isPower = False
                self.pips[0].school = School.Universal
            else:
                self.pips.pop(0)

        self.orderPips()

    def addPips(self, num: int):
        while num > 0:
            if self.sumTotalValue() == 14:
                self.orderPips()
                return
            
            if len(self.pips) < 7:
                if num > 1:
                    self.pips.append(Pip(isPower=True, school=School.Universal))
                    num -= 2
                if num == 1:
                    self.pips.append(Pip(isPower=False, school=School.Universal))
                    num -= 1
            else:
                self.convertWhiteToPower()
                num -= 1

    def destroyShadowPips(self, num: int):
        while num > 0:
            if len(self.shadow_pips) == 0:
                return
            
            self.shadow_pips.pop()
            num -= 1
        
    def addShadowPips(self, num: int):
        while num > 0:
            if len(self.shadow_pips == 2):
                return
            
            self.shadow_pips.append(Pip(isPower=True, school=School.Shadow))

    def subtractPips(self, num: int, extraPipReq: List[Pip], cardSchool: School, mastery: School, pserve: int) -> bool:
        if self.sumTotalValue() < num:
            return False
        
        for pip in extraPipReq:
            if not pip in self.pips:
                return False

        for pip in extraPipReq:
            match pip.school:
                case School.Shadow:
                    self.shadow_pips.pop()
                case _:
                    self.pips.remove(pip)
                    num -= 2

        if cardSchool == mastery:
            # Evaluate all Power Pips first
            for pip in self.pips:
                if pip.isPower:
                    num -= 2
                    self.pips.remove(pip)
            
            # On-school pips
            for pip in self.pips:
                if pip.school == cardSchool:
                    num -= 2
                    self.pips.remove(pip)

            # Off-school pips
            for pip in self.pips:
                if pip.school != School.Universal and pip.school != cardSchool:
                    num -= 2
                    self.pips.remove(pip)

            # White pips
            for pip in self.pips:
                if not pip.isPower:
                    num -= 1
                    self.pips.remove(pip)

        else:
            # Evaluate school pip of card school
            for pip in self.pips:
                if pip.school == cardSchool:
                    num -= 2
                    self.pips.remove(pip)

            # White Pips
            for pip in self.pips:
                if not pip.isPower:
                    num -= 1
                    self.pips.remove(pip)

            # Power Pips
            for pip in self.pips:
                if pip.isPower:
                    num -= 1
                    self.pips.remove(pip)

        if num == -1:
            if randint(0, 100) < self.calculatePipConserveChance(pserve):
                self.pips.append(Pip(isPower=False, school=School.Universal))

        self.orderPips()

    def calculatePipConserveChance(self, pserve: int): # TODO: do this one too noodle
        return

