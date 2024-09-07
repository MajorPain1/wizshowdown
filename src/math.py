from random import choice, randint, random
from typing import Callable, List
from math import floor

from src.player import Player
from src.card import Card
from src.enums import SpellEffects, School
from src.hangingeffect import Charm, Ward, Overtime, Bubble, Aura

def calculateCritChance(level: int, critical: int, block: int) -> float: # TODO : these calc functions
    return min(min(level/185,1) * (12*critical)/(12*critical+block),.95)

def calculateBlockChance(level: int, critical: int, block: int) -> float:
    return min(level/185,1) * block/(block + 12*critical)

def calculateCritMultiplier(critical: int, block: int) -> float:
    return 2 - (5*block)/(critical+5*block)

def calculateHeal(player: Player, param: int, school: School, hot: bool = False, no_crit: bool = False) -> int:
    total = param * (1 + player.stats.outgoing/100.0)
    
    critical = player.stats.critical.dict[school]
    school = player.school

    # Calculate Auras on Player
    for aura in player.auraEffects:
        aura: Aura
        if aura.school == School.Universal or aura.school == school:
            match aura.spellEffect:
                case SpellEffects.modify_outgoing_heal:
                    total *= 1 + aura.param/100
                case SpellEffects.modify_outgoing_heal_flat:
                    total += aura.param
                case SpellEffects.crit_boost:
                    critical # TODO: Figure out how crit boost works
                case _:
                    continue                 
    
    # Calculate Charms on Self
    charms_to_remove = []
    already_used_charms = []
    for charm in player.charms:
        charm: Charm
        if charm.objectName in already_used_charms:
            continue

        if charm.school == School.Universal or charm.school == school:
            match charm.spellEffect:
                case SpellEffects.modify_outgoing_heal:
                    total *= 1 + charm.param/100
                case SpellEffects.modify_outgoing_heal_flat:
                    total += charm.param
                case SpellEffects.crit_boost:
                    critical # TODO: Figure out how crit boost works
                case _:
                    continue
            charms_to_remove.append(charm)
            already_used_charms.append(charm.objectName)

    player.charms.reverse()
    for charm in charms_to_remove:
        player.charms.remove(charm)
    player.charms.reverse()

    # Calculate Bubble
    for bubble in player.team.bubbleEffects:
        bubble: Bubble
        if bubble.school == School.Universal or bubble.school == school:
            match bubble.spellEffect:
                case SpellEffects.modify_outgoing_heal:
                    total *= 1 + bubble.param/100
                case SpellEffects.modify_outgoing_heal_flat:
                    pierce += bubble.param
                case SpellEffects.crit_boost:
                    critical # TODO: Figure out how crit boost works
                case _:
                    continue

    # Calculate Wards on Self
    wards_to_remove = []
    already_used_wards = []
    for ward in player.wards:
        ward: Ward
        if ward.objectName in already_used_wards:
            continue

        if ward.school == School.Universal or charm.school == school:
            match ward.spellEffect:
                case SpellEffects.modify_incoming_heal:
                    pass # TODO: Heal wards
                case _:
                    continue
            wards_to_remove.append(ward)
            already_used_wards.append(ward.objectName)

    player.wards.reverse()
    for ward in wards_to_remove:
        player.wards.remove(ward)
    player.wards.reverse()

    crit_chance = calculateCritChance(player.level, player.stats.critical, player.stats.block)
    crit_multiplier = calculateCritMultiplier(player.stats.critical, player.stats.block)
    critroll = random()

    if crit_chance > critroll:
        total *= crit_multiplier

    return total

def calculateDOT(player: Player, ot: Overtime) -> int:
    return

def calculateHOT(player: Player, ot: Overtime) -> int:
    return

def calculateAccuracy(player: Player, card: Card) -> int:
    baseAccuracyRoll = randint(1,100)
    playerAccuracy = player.stats.accuracy.dict[player.school]
    totalMantle = 0

    mantles_to_remove = []
    already_used_mantles = []
    for charm in player.charms:
        charm: Charm
        if charm.objectName in already_used_mantles:
            continue

        if charm.school == School.Universal or charm.school == player.school:
            match charm.spellEffect:
                case SpellEffects.modify_accuracy:
                    totalMantle+=charm.param
                case _:
                    continue
            mantles_to_remove.append(charm)
            already_used_mantles.append(charm.objectName)

    player.charms.reverse()
    for mantle in mantles_to_remove:
        player.charms.remove(mantle)
    player.charms.reverse()

    return playerAccuracy + baseAccuracyRoll - totalMantle > (100-card.accuracy)

def calculateDamage(player: Player, opponent: Player, param: int, school: School, cardSchool: School, dot: bool = False, no_crit: bool = False) -> int:
    total = param

    damage = player.stats.damage.dict[cardSchool]
    critical = player.stats.critical.dict[cardSchool]
    pierce = player.stats.pierce.dict[cardSchool]

    resist = opponent.stats.resist.dict[cardSchool]
    block = opponent.stats.block.dict[cardSchool]

    total *= 1 + (damage/100)

    # Calculate Auras on Player
    for aura in player.auraEffects:
        aura: Aura
        if aura.school == School.Universal or aura.school == school:
            match aura.spellEffect:
                case SpellEffects.modify_outgoing_damage:
                    total *= 1 + aura.param/100
                case SpellEffects.modify_outgoing_armor_piercing:
                    pierce += aura.param
                case SpellEffects.crit_boost:
                    critical # TODO: Figure out how crit boost works
                case _:
                    continue

    
    # Calculate Bubble
    for bubble in player.team.bubbleEffects:
        bubble: Bubble
        if bubble.school == School.Universal or bubble.school == school:
            match bubble.spellEffect:
                case SpellEffects.modify_outgoing_damage:
                    total *= 1 + bubble.param/100
                case SpellEffects.modify_outgoing_armor_piercing:
                    pierce += bubble.param
                case SpellEffects.crit_boost:
                    critical # TODO: Figure out how crit boost works
                case _:
                    continue
                
    
    # Calculate Charms on Player
    already_used_charms = []
    for charm in player.charms:
        charm: Charm
        if charm.objectName in already_used_charms:
            continue

        if charm.school == School.Universal or charm.school == school:
            match charm.spellEffect:
                case SpellEffects.modify_outgoing_damage:
                    total *= 1 + charm.param/100
                case SpellEffects.modify_outgoing_armor_piercing:
                    pierce += charm.param
                case SpellEffects.modify_outgoing_damage_flat:
                    total += charm.param
                case SpellEffects.modify_outgoing_damage_type:
                    school = School(charm.param)
                case SpellEffects.crit_boost:
                    critical # TODO: Figure out how crit boost works
                case _:
                    continue
            charm.used = True
            already_used_charms.append(charm.objectName)

    if not dot:
        # Calculate Aura on Opponent
        for aura in opponent.auraEffects:
            aura: Aura
            if aura.school == School.Universal or aura.school == school:
                match aura.spellEffect:
                    case SpellEffects.modify_incoming_damage:
                        # Handling Pierce
                        if aura.param < 0:
                            if aura.param + pierce >= 0:
                                aura.param += pierce
                                pierce = 0
                            else:
                                pierce += aura.param
                                aura.param = 0

                        total *= 1 + aura.param/100
                    case SpellEffects.crit_block:
                        block # TODO: Figure out how crit block works
                    case _:
                        continue


        # Calculate Wards on Opponent
        wards_to_remove = []
        already_used_wards = []
        for ward in opponent.wards:
            ward: Ward
            if ward.objectName in already_used_wards:
                continue

            if ward.school == School.Universal or charm.school == school:
                match ward.spellEffect:
                    case SpellEffects.modify_incoming_damage:
                        # Handling Pierce
                        if ward.param < 0:
                            if ward.param + pierce >= 0:
                                ward.param += pierce
                                pierce = 0
                            else:
                                pierce += ward.param
                                ward.param = 0

                        total *= 1 + ward.param/100
                    case SpellEffects.modify_incoming_armor_piercing:
                        pierce += ward.param
                    case SpellEffects.absorb_damage:
                        total -= ward.param
                    case _:
                        continue
                wards_to_remove.append(ward)
                already_used_wards.append(ward.objectName)

        opponent.wards.reverse()
        for ward in wards_to_remove:
            opponent.wards.remove(ward)
        opponent.wards.reverse()


        # Handling Pierce
        if resist > 0:
            if resist - pierce >= 0:
                resist -= pierce
                pierce = 0
            else:
                pierce -= resist
                resist = 0

        total *= 1 - resist/100
        
    if not no_crit:
        if critical == 0:
            crit_chance = 0.0
        else:
            crit_chance = calculateCritChance(player.level, critical, block)

        if block == 0 or critical == 0:
            block_chance = 0.0
        else:
            block_chance = calculateBlockChance(player.level, critical, block)

        if block == 0 and critical == 0:
            crit_multiplier = 1.0
        elif block == 0 and critical > 0:
            crit_multiplier = 2.0
        else:
            crit_multiplier = calculateCritMultiplier(player.level, critical, block)

        if crit_chance - block_chance < randint(0,100)/100:
            total *= crit_multiplier

    #if player.school == School.Myth:   Darn Moose Yaga!
    #    total = total * 5

    return floor(total)
