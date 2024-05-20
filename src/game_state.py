from random import choice, randint
from typing import Callable, List

from src.player import Player
from src.card import Card, Effect
from src.enums import SpellEffects, EffectTarget, School, ExecutionOutcomes, Disposition, CardType
from src.hangingeffect import Charm, Ward, Overtime, Bubble, Aura


hangingEffects = [

]

class GameState:
    def __init__(self, player1: Player, player2: Player):
        self.round = 1
        self.player1 = player1
        self.player2 = player2
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        self.first: Player = choice([player1, player2])
        self.second: Player = ([player1, player2].remove(self.first))[0]

        self.bubble = []

    def calculateCritChance(self, player: Player, critical: int, block: int) -> float: # TODO : these calc functions
        return

    def calculateBlockChance(self, player: Player, critical: int, block: int) -> float:
        return

    def calculateCritMultiplier(self, player: Player, critical: int, block: int) -> float:
        return
    
    def calculateHeal(self, player, param: int) -> int:
        return
    
    def calculateDOT(self, ot: Overtime) -> int:
        return

    def calculateHOT(self, ot: Overtime) -> int:
        return

    def calculateAccuracy(self, player: Player, card: Card) -> int:
        return

    def calculateDamage(self, player: Player, param: int, school: School, cardSchool: School, no_crit: bool = False) -> int:
        total = param

        damage = player.stats.damage.dict[cardSchool]
        critical = player.stats.critical.dict[cardSchool],
        pierce = player.stats.pierce.dict[cardSchool]

        resist = player.opponent.stats.resist.dict[cardSchool]
        block = player.opponent.stats.block.dict[cardSchool]

        total *= 1 + (damage/100)

        # Calculate Auras on Player
        for aura in player.aura:
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
        for bubble in self.bubble:
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
        charms_to_remove = []
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
                    case _:
                        continue
                charms_to_remove.append(charm)
                already_used_charms.append(charm.objectName)

        player.charms.reverse()
        for charm in charms_to_remove:
            player.charms.remove(charm)
        player.charms.reverse()


        # Calculate Aura on Opponent
        for aura in player.opponent.aura:
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
        for ward in player.opponent.wards:
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

        player.opponent.wards.reverse()
        for ward in wards_to_remove:
            player.opponent.wards.remove(ward)
        player.opponent.wards.reverse()


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
            crit_chance = self.calculateCritChance(player, critical, block)
            block_chance = self.calculateBlockChance(player, critical, block)
            crit_multiplier = self.calculateCritMultiplier(player, critical, block)

            if crit_chance - block_chance < randint(0,100)/100:
                total *= crit_multiplier

        #if player.school == School.Myth:   Darn Moose Yaga!
        #    total = total * 5

        return total



    def findFirstCharm(self, player: Player, disposition: Disposition, on_opponent: bool = False):
        if on_opponent:
            charms_list = player.opponent.charms
        else:
            charms_list = player.charms

        for charm in reversed(charms_list):
            charm: Charm
            disp = charm.getDisposition(player)
            if disp == disposition or disp == Disposition.both or disposition == Disposition.both:
                return charm
        return None
          
    def findFirstWard(self, player: Player, disposition: Disposition, on_opponent: bool = False):
        if on_opponent:
            wards_list = player.opponent.wards
        else:
            wards_list = player.wards

        for ward in reversed(wards_list):
            ward: Ward
            disp = ward.getDisposition(player)
            if disp == disposition or disp == Disposition.both or disposition == Disposition.both:
                return ward
        return None
                    
    def findFirstOT(self, player: Player, disposition: Disposition, on_opponent: bool = False):
        if on_opponent:
            overtimes_list = player.opponent.overtimes
        else:
            overtimes_list = player.wards

        for overtime in reversed(overtimes_list):
            overtime: Overtime
            disp = overtime.getDisposition(player)
            if disp == disposition or disp == Disposition.both or disposition == Disposition.both:
                return overtime
        return None

    def recursiveExecuteEffects(self, player: Player, card: Card, effect: Effect):
        target = None
        if effect.target.value in [4, 5, 8, 13, 12, 14]:
            target = player.opponent
        elif effect.target.value in [6, 7, 9, 15]:
            target = player

        hangingEffect = None
        effectClass: Callable = None
        match card.cardType:
            case CardType.Ward:
                effectClass = Ward
            case CardType.Charm:
                effectClass = Charm
            case CardType.Aura:
                effectClass = Aura
            case CardType.Global:
                effectClass = Bubble

        # Match EVERY SINGLE SPELL EFFECT
        match effect.spelleffect:
            case SpellEffects.damage:
                target.updateHP(-self.calculateDamage(player, effect.param, effect.school, card.school))
            case SpellEffects.damage_no_crit:
                target.updateHP(-self.calculateDamage(player, effect.param, effect.school, card.school, no_crit=True))
            case SpellEffects.heal:
                target.updateHP(self.calculateHeal(player, effect.param))
            case SpellEffects.heal_percent:
                target.updateHP(target.stats.health*(1+effect.param))
            case SpellEffects.steal_health:
                damage = self.calculateDamage(player, effect.param, effect.school, card.school) * 0.75
                target.updateHP(-damage)
                target.opponent.updateHP(damage * 0.5)
            case SpellEffects.reduce_over_time:
                if len(target.overtimes) != 0:
                    target.overtimes[-1].rounds -= effect.param
            case SpellEffects.detonate_over_time:# TODO: Figure out Detonating HOTS vs DOTS
                for _ in range(effect.param):
                    if len(target.overtimes) != 0:
                        overtime = target.overtimes[-1]
                        target.current_hp -= overtime.param * overtime.rounds
            case SpellEffects.push_charm:
                for _ in range(effect.param):
                    neg_charm = self.findFirstCharm(player, disposition=Disposition.harmful)
                    if neg_charm != None:
                        neg_charm.disposition = Disposition.beneficial
                        neg_charm.owner = player
                        player.charms.remove(neg_charm)
                        target.charms.append(neg_charm)
            case SpellEffects.steal_charm:
                for _ in range(effect.param):
                    pos_charm = self.findFirstCharm(player, disposition=Disposition.harmful, on_opponent=True)
                    if pos_charm != None:
                        pos_charm.disposition = Disposition.beneficial
                        pos_charm.owner = player
                        target.charms.remove(pos_charm)
                        player.charms.append(pos_charm)
            case SpellEffects.push_ward:
                for _ in range(effect.param):
                    pos_ward = self.findFirstWard(player, disposition=Disposition.harmful)
                    if pos_ward != None:
                        pos_ward.disposition = Disposition.beneficial
                        pos_ward.owner = player
                        player.wards.remove(pos_ward)
                        target.wards.append(pos_ward)
            case SpellEffects.steal_ward:
                for _ in range(effect.param):
                    neg_ward = self.findFirstWard(player, disposition=Disposition.harmful, on_opponent=True)
                    if neg_ward != None:
                        neg_ward.disposition = Disposition.beneficial
                        neg_ward.owner = player
                        target.wards.remove(neg_ward)
                        player.wards.append(neg_ward)
            case SpellEffects.push_over_time:
                for _ in range(effect.param):
                    dot = self.findFirstOT(player, disposition=Disposition.harmful)
                    if dot != None:
                        player.overtimes.remove(dot)
                        target.overtimes.append(dot)
            case SpellEffects.steal_over_time:
                for _ in range(effect.param):
                    hot = self.findFirstOT(player, disposition=Disposition.harmful, on_opponent=True)
                    if hot != None:
                        target.overtimes.remove(hot)
                        player.overtimes.append(hot)
            case SpellEffects.remove_charm:
                for _ in range(effect.param):
                    if target == player.opponent:
                        charm = self.findFirstCharm(target, disposition=Disposition.harmful, on_opponent=True)
                    elif target == player:
                        charm = self.findFirstCharm(target, disposition=Disposition.harmful)
                    if charm != None:
                        target.charms.remove(charm)
            case SpellEffects.remove_ward:
                for _ in range(effect.param):
                    if target == player.opponent:
                        ward = self.findFirstWard(target, disposition=Disposition.harmful, on_opponent=True)
                    elif target == player:
                        ward = self.findFirstWard(target, disposition=Disposition.harmful)
                    if ward != None:
                        target.wards.remove(ward)
            case SpellEffects.remove_over_time:
                for _ in range(effect.param):
                    if target == player.opponent:
                        ot = self.findFirstOT(player, disposition=Disposition.harmful, on_opponent=True)
                    elif target == player:
                        ot = self.findFirstOT(player, disposition=Disposition.harmful)
                    if ot != None:
                        target.overtimes.remove(ot)
            case SpellEffects.remove_aura:
                target.aura = []
            case SpellEffects.swap_charm: # TODO : Figure out swapping multiple effects
                pos_charm_target = self.findFirstCharm(player, disposition=Disposition.harmful, on_opponent=True)
                pos_charm_self = self.findFirstCharm(player, disposition=Disposition.beneficial)
                if pos_charm_target != None:
                    target.charms.remove(pos_charm_target)
                    player.charms.append(pos_charm_target)
                if pos_charm_self != None:
                    player.charms.remove(pos_charm_self)
                    target.charms.append(pos_charm_self)
            case SpellEffects.swap_ward:
                neg_ward_target = self.findFirstWard(player, disposition=Disposition.harmful, on_opponent=True)
                neg_ward_self = self.findFirstWard(player, disposition=Disposition.beneficial)
                if neg_ward_target != None:
                    target.wards.remove(neg_ward_target)
                    target.opponent.wards.append(neg_ward_target)
                if neg_ward_self != None:
                    target.opponent.wards.remove(neg_ward_self)
                    target.wards.append(neg_ward_self)
            case SpellEffects.swap_over_time:
                if len(target.overtimes) != 0:
                    ot_target = target.overtimes[-1]
                if len(target.opponent.overtimes) != 0:
                    ot_self = target.opponent.overtimes[-1]
                target.overtimes.remove(ot_target)
                target.opponent.overtimes.remove(ot_self)
                target.overtimes.append(ot_self)
                target.opponent.overtimes.append(ot_target)
            case (
                SpellEffects.modify_incoming_damage | 
                SpellEffects.modify_incoming_damage_flat | 
                SpellEffects.modify_incoming_heal |
                SpellEffects.modify_incoming_heal_flat | 
                SpellEffects.modify_incoming_damage_type |
                SpellEffects.modify_incoming_armor_piercing |
                SpellEffects.modify_outgoing_damage |
                SpellEffects.modify_outgoing_damage_flat |
                SpellEffects.modify_outgoing_heal |
                SpellEffects.modify_outgoing_heal_flat |
                SpellEffects.modify_outgoing_damage_type |
                SpellEffects.modify_outgoing_armor_piercing |
                SpellEffects.absorb_damage |
                SpellEffects.absorb_heal |
                SpellEffects.modify_accuracy |
                SpellEffects.dispel |
                SpellEffects.pip_conversion |
                SpellEffects.crit_boost |
                SpellEffects.crit_block
                ):
                hangingEffect = effectClass(
                    objectName=card.objectName, 
                    owner=player, 
                    param=effect.param, 
                    school=effect.school, 
                    spellEffect=effect.spelleffect, 
                    disposition=effect.disposition
                    )
            case SpellEffects.summon_creature:
                pass # TODO: Minions
            case SpellEffects.stun:
                stunblock = None
                for ward in target.wards:
                    ward: Ward
                    if ward.spellEffect == SpellEffects.stun_block and stunblock == None:
                        stunblock = ward
                
                if stunblock != None:
                    target.wards.remove(stunblock)
                else:
                    target.stunned = True
            case SpellEffects.reshuffle:
                target.deckstate.reshuffle()
            case SpellEffects.modify_pips | SpellEffects.modify_power_pips:
                pass # TODO: Look at Mana Burn spell effects and B Storm Owl spell Effects


        match card.cardType:
            case CardType.Ward:
                effectClass = Ward
            case CardType.Charm:
                effectClass = Charm
            case CardType.Aura:
                effectClass = Aura
            case CardType.Global:
                effectClass = Bubble

        for subeffect in effect.subeffects:
            if subeffect[0](player, subeffect[1], subeffect[2]):
                self.recursiveExecuteEffects(player, subeffect[3])

    def executeTurn(self, player: Player, card: Card) -> ExecutionOutcomes:
        if card == None:
            return ExecutionOutcomes.Pass
        if player.stunned:
            player.stunned = False
            return ExecutionOutcomes.Stunned
        if self.calculateAccuracy(player, card) > card.accuracy:
            return ExecutionOutcomes.Fizzle
        
        for effect in card.effects:
            self.recursiveExecuteEffects(player, card, effect)

        return ExecutionOutcomes.Success

    def turn(self, player: Player):
        if player.current_hp <= 0:
            if player.opponent.current_hp > 0:   
                player.opponent.win = True
            return
        # Give player actions to discard, draw, and use card
        used_card: Card = None
        # Give opponent actions to discard and draw
        # Tick player's OTs
        for ot in reversed(player.overtimes):
            ot: Overtime
            match ot.spellEffect:
                case SpellEffects.damage_over_time:
                    player.updateHP(-self.calculateDOT(player, ot))
                case SpellEffects.heal_over_time:
                    player.updateHP(self.calculateHeal(player, ot))
                case SpellEffects.deferred_damage:
                    if ot.rounds == 1:
                        player.updateHP(-self.calculateDOT(player, ot))
                    else:
                        ot.tick()

            if ot.rounds == 0:
                player.overtimes.remove(ot)
        # Execute Turn
        outcome = self.executeTurn(player, used_card)
        match outcome: # Outcome used for UI when made
            case ExecutionOutcomes.Pass:
                pass
            case ExecutionOutcomes.Fizzle:
                pass
            case ExecutionOutcomes.Stunned:
                pass
            case ExecutionOutcomes.Success:
                pass
            
        # Player draws from main
        player.deckstate.drawMain()
        player.addRoundPip()

    def run(self): # Might get rid of this when implementing pygame and multiplayer
        while self.player1.win == False or self.player1.win == False:
            # self.first's turn
            self.turn(self.first)

            # self.second's turn
            self.turn(self.second)
            
            # Increment round
            self.round += 1

        # Display winner
        if self.player1.win:
            print(f"{self.player1.name} wins")
        elif self.player2.win:
            print(f"{self.player2.name} wins")
        else:
            print("Tie")
