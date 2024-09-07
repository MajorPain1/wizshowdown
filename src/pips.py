from typing import List
from random import randint

from src.enums import School

schoolPipOrdering = {
    School.Universal: 0,
    School.Balance: 1,
    School.Death: 2,
    School.Fire: 3,
    School.Ice: 4,
    School.Life: 5,
    School.Myth: 6,
    School.Storm: 7,
}

def calculatePipConserveChance(pserve: int) -> int: # TODO: do this one too noodle
    return 100

class Pip:
    def __init__(self, isPower: bool, school: School):
        self.isPower = isPower
        self.school = school

    def __eq__(self, other):
        return self.isPower == other.isPower and self.school == other.school
    
    def __repr__(self):
        if self.isPower:
            return f"Power Pip" #[{self.school}]
        else:
            return f"White Pip"

class PipArray:
    def __init__(self, pips: List[Pip] = [], shadow_pips: List[Pip] = []):
        self.pips = pips
        self.shadow_pips = shadow_pips
        self.archmastery = 0
        self.shadow_guage = 0
        
    def __repr__(self) -> str:
        res = ""
        for pip in self.pips:
            res += str(pip) + " "
        return res

    def getRawPipValue(self) -> int:
        res = 0
        for pip in self.pips:
            if pip.isPower:
                res += 2
            else:
                res += 1
        return res
    
    def getPowerPip(self):
        for pip in self.pips:
            if pip.isPower:
                return pip
        return None
    
    def getSpecificSchoolPip(self, school: School):
        for pip in self.pips:
            if pip.school == school:
                return pip
        return None
    
    def getAnySchoolPip(self):
        for pip in self.pips:
            if pip.school != School.Universal:
                return pip
        return None
            
    def getWhitePip(self):
        for pip in self.pips:
            if not pip.isPower:
                return pip
        return None

    def orderPips(self):
        whitePips: List[Pip] = []
        # White pips in front
        for pip in self.pips:
            if not pip.isPower:
                whitePips.append(pip)
                self.pips.remove(pip)

        schoolPips = sorted(self.pips, key=lambda pip:schoolPipOrdering[pip.school])
        self.pips = whitePips + schoolPips

    def sumTotalValue(self, school: School, mastery: bool) -> int:
        total = 0
        for pip in self.pips:
            if pip.isPower and mastery:
                total += 2
            elif pip.school == school:
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

    def addPips(self, num: int, pserve: int = -1, school: School = School.Universal, white_only: bool = False):
        while num > 0:
            self.orderPips()
            if self.getRawPipValue() == 14:
                self.orderPips()
                return
            
            if len(self.pips) < 7:
                if num > 1 and not white_only:
                    self.pips.append(Pip(isPower=True, school=school))
                    num -= 2
                if num == 1 or white_only:
                    self.pips.append(Pip(isPower=False, school=School.Universal))
                    num -= 1
            elif pserve == -1 or randint(0, 99) < calculatePipConserveChance(pserve):
                self.convertWhiteToPower()
                num -= 1
                
        self.orderPips()

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
        if self.sumTotalValue(cardSchool, cardSchool == mastery) < num:
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
                    extraPipReq.remove(pip)

        if cardSchool == mastery:
            # Evaluate White Pips if odd
            if num % 2 == 1 and not self.getWhitePip() is None:
                num -= 1
                self.pips.remove(self.getWhitePip())

            # Evaluate all Power Pips
            while not self.getPowerPip() is None and num > 0:
                num -= 2
                self.pips.remove(self.getPowerPip())
            
            # On-school pips
            while not self.getSpecificSchoolPip(cardSchool) is None and num > 0:
                num -= 2
                self.pips.remove(self.getSpecificSchoolPip(cardSchool))

            # Off-school pips
            while not self.getAnySchoolPip() is None and num > 0:
                num -= 2
                self.pips.remove(self.getAnySchoolPip())

            # White pips
            while not self.getWhitePip() is None and num > 0:
                num -= 1
                self.pips.remove(self.getWhitePip())

        else:
            # Evaluate White Pips if odd
            if num % 2 == 1 and not self.getWhitePip() is None:
                num -= 1
                self.pips.remove(self.getWhitePip())

            # Evaluate school pip of card school
            while not self.getSpecificSchoolPip(cardSchool) is None and num > 0:
                num -= 2
                self.pips.remove(self.getSpecificSchoolPip(cardSchool))

            # White Pips
            while not self.getWhitePip() is None and num > 0:
                num -= 1
                self.pips.remove(self.getWhitePip())

            # Power Pips
            while not self.getPowerPip() is None and num > 0:
                num -= 1
                self.pips.remove(self.getPowerPip())

        if num == -1:
            if randint(0, 99) < calculatePipConserveChance(pserve):
                self.pips.append(Pip(isPower=False, school=School.Universal))

        self.orderPips()

