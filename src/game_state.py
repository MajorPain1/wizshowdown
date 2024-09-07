from random import choice, randint, random
from typing import Callable, List
from math import floor

from src.player import Player, Team
from src.card import Card, Effect
from src.enums import SpellEffects, EffectTarget, School, ExecutionOutcomes, Disposition, CardType
from src.hangingeffect import Charm, Ward, Overtime, Bubble, Aura, reverseDisposition
from src.math import *


class GameState:
    def __init__(self, team1: Team, team2: Team):
        self.round = 1
        self.team1 = team1
        self.team2 = team2
        self.team1.opponentTeam = self.team2
        self.team2.opponentTeam = self.team1
        
        self.team1.addRoundPip()
        self.team2.addRoundPip()

    def findFirstCharm(self, player: Player, disposition: Disposition):
        charms_list = player.charms

        for charm in reversed(charms_list):
            charm: Charm
            disp = charm.getDisposition(player)
            if disp == disposition or disp == Disposition.both or disposition == Disposition.both:
                return charm
        return None

    def findFirstWard(self, player: Player, disposition: Disposition):
        wards_list = player.wards

        for ward in reversed(wards_list):
            ward: Ward
            disp = ward.getDisposition(player)
            if disp == disposition or disp == Disposition.both or disposition == Disposition.both:
                return ward
        return None
                    
    def findFirstOT(self, player: Player, disposition: Disposition):
        overtimes_list = player.wards

        for overtime in reversed(overtimes_list):
            overtime: Overtime
            disp = overtime.getDisposition(player)
            if disp == disposition or disp == Disposition.both or disposition == Disposition.both:
                return overtime
        return None

    def recursiveExecuteEffects(self, player: Player, card: Card, effect: Effect, targets: List[int]):
        for i in targets:
            match effect.target:
                case EffectTarget.invalid_target | EffectTarget.spell | EffectTarget.specific_spells | EffectTarget.target_global:
                    target = None
                case EffectTarget.enemy_team | EffectTarget.enemy_team_all_at_once | EffectTarget.enemy_single | EffectTarget.at_least_one_enemy | EffectTarget.preselected_enemy_single | EffectTarget.multi_target_enemy:
                    target = player.team.opponentTeam.slots[i]
                    if target == None:
                        continue
                case EffectTarget.friendly_team | EffectTarget.friendly_team_all_at_once | EffectTarget.friendly_single | EffectTarget.multi_target_friendly | EffectTarget.friendly_single_not_me:
                    target = player.team.slots[i]
                    if target == None:
                        continue
                case EffectTarget.self:
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
                case _:
                    pass

            # Match EVERY SINGLE SPELL EFFECT
            match effect.spelleffect:
                case SpellEffects.invalid_spell_effect:
                    pass

                case SpellEffects.damage:
                    target.updateHP(-calculateDamage(player, target, effect.param, effect.school, card.school))

                case SpellEffects.damage_no_crit:
                    target.updateHP(-calculateDamage(player, target, effect.param, effect.school, card.school, no_crit=True))

                case SpellEffects.heal:
                    target.updateHP(calculateHeal(player, effect.param))

                case SpellEffects.heal_percent:
                    target.updateHP(target.stats.health*(1+effect.param))

                case SpellEffects.steal_health:
                    damage = calculateDamage(player, effect.param, effect.school, card.school) * 0.75
                    target.updateHP(-damage)
                    player.updateHP(damage * 0.5)

                case SpellEffects.reduce_over_time:
                    for _ in range(-effect.param):
                        overtime = self.findFirstOT(target, disposition=effect.disposition)
                        if overtime != None:
                            if overtime.rounds > 1:
                                overtime.rounds -= 1
                            else:
                                target.overtimes.remove(overtime)

                case SpellEffects.detonate_over_time:
                    for _ in range(effect.param):
                        overtime = self.findFirstOT(target, disposition=effect.disposition)
                        if overtime != None:
                            target.current_hp += overtime.param * overtime.rounds * effect.healModifier

                case SpellEffects.push_charm:
                    for _ in range(effect.param):
                        neg_charm = self.findFirstCharm(player, disposition=effect.disposition)
                        if neg_charm != None:
                            neg_charm.disposition = reverseDisposition(effect.disposition)
                            neg_charm.owner = player
                            player.charms.remove(neg_charm)
                            target.charms.append(neg_charm)

                case SpellEffects.steal_charm:
                    for _ in range(effect.param):
                        pos_charm = self.findFirstCharm(target, disposition=effect.disposition)
                        if pos_charm != None:
                            pos_charm.disposition = reverseDisposition(effect.disposition)
                            pos_charm.owner = player
                            target.charms.remove(pos_charm)
                            player.charms.append(pos_charm)

                case SpellEffects.push_ward:
                    for _ in range(effect.param):
                        pos_ward = self.findFirstWard(player, disposition=effect.disposition)
                        if pos_ward != None:
                            pos_ward.disposition = reverseDisposition(effect.disposition)
                            pos_ward.owner = player
                            player.wards.remove(pos_ward)
                            target.wards.append(pos_ward)

                case SpellEffects.steal_ward:
                    for _ in range(effect.param):
                        neg_ward = self.findFirstWard(target, disposition=effect.disposition)
                        if neg_ward != None:
                            neg_ward.disposition = reverseDisposition(effect.disposition)
                            neg_ward.owner = player
                            target.wards.remove(neg_ward)
                            player.wards.append(neg_ward)

                case SpellEffects.push_over_time:
                    for _ in range(effect.param):
                        dot = self.findFirstOT(player, disposition=effect.disposition)
                        if dot != None:
                            player.overtimes.remove(dot)
                            target.overtimes.append(dot)
                            
                case SpellEffects.steal_over_time:
                    for _ in range(effect.param):
                        hot = self.findFirstOT(target, disposition=effect.disposition)
                        if hot != None:
                            target.overtimes.remove(hot)
                            player.overtimes.append(hot)

                case SpellEffects.remove_charm:
                    for _ in range(effect.param):
                        charm = self.findFirstCharm(target, disposition=effect.disposition)
                        if charm != None:
                            target.charms.remove(charm)

                case SpellEffects.remove_ward:
                    for _ in range(effect.param):
                        ward = self.findFirstWard(target, disposition=effect.disposition)
                        if ward != None:
                            target.wards.remove(ward)

                case SpellEffects.remove_over_time:
                    for _ in range(effect.param):
                        ot = self.findFirstOT(target, disposition=effect.disposition)
                        if ot != None:
                            target.overtimes.remove(ot)

                case SpellEffects.remove_aura:
                    target.aura = []

                case SpellEffects.swap_charm:
                    charm_target = []
                    for _ in range(effect.param):
                        charm = self.findFirstCharm(target, disposition=effect.disposition)
                        charm_target.append(charm)
                        target.charms.remove(charm)
                        
                    charm_self = []
                    for _ in range(effect.param):
                        charm = self.findFirstCharm(player, disposition=effect.disposition)
                        charm_self.append(charm)
                        player.charms.remove(charm)
                        
                    for charm in charm_target:
                        player.charms.append(charm)
                        
                    for charm in charm_self:
                        target.charms.append(charm)

                case SpellEffects.swap_ward:
                    ward_target = []
                    for _ in range(effect.param):
                        ward = self.findFirstWard(target, disposition=effect.disposition)
                        ward_target.append(ward)
                        target.wards.remove(ward)
                        
                    ward_self = []
                    for _ in range(effect.param):
                        ward = self.findFirstWard(player, disposition=effect.disposition)
                        ward_self.append(ward)
                        player.wards.remove(ward)
                        
                    for ward in ward_target:
                        player.wards.append(ward)
                        
                    for ward in ward_self:
                        target.wards.append(ward)

                case SpellEffects.swap_over_time:
                    ot_target = []
                    for _ in range(effect.param):
                        ot = self.findFirstOT(target, disposition=effect.disposition)
                        ot_target.append(ot)
                        target.overtimes.remove(ot)
                        
                    ot_self = []
                    for _ in range(effect.param):
                        ot = self.findFirstOT(player, disposition=effect.disposition)
                        ot_self.append(ot)
                        player.overtimes.remove(ot)
                        
                    for ot in ot_target:
                        player.overtimes.append(ot)
                        
                    for ot in ot_self:
                        target.overtimes.append(ot)

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
                    SpellEffects.modify_power_pip_chance |
                    SpellEffects.absorb_damage |
                    SpellEffects.absorb_heal |
                    SpellEffects.modify_accuracy |
                    SpellEffects.dispel |
                    SpellEffects.pip_conversion |
                    SpellEffects.crit_boost |
                    SpellEffects.crit_block |
                    SpellEffects.stun_block |
                    SpellEffects.dispel_block |
                    SpellEffects.confusion_block |
                    SpellEffects.power_pip_conversion |
                    SpellEffects.crit_boost_school_specific |
                    SpellEffects.modify_pip_round_rate 
                    ):
                    # Handle Chromatics without septupling json file size
                    if effect.school == School.ChromaticSelf:
                        effect_school = player.school
                    elif effect.school == School.ChromaticTarget:
                        effect_school = target.school
                    else:
                        effect_school = effect.school
                        
                    hangingEffect = effectClass(
                        objectName=card.objectName, 
                        owner=player, 
                        param=effect.param, 
                        school=effect_school, 
                        spellEffect=effect.spelleffect, 
                        disposition=effect.disposition,
                        rounds=effect.rounds
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

                case SpellEffects.modify_pips:
                    if effect.param < 0:
                        target.pips.destroyPips(-effect.param)
                    elif effect.param > 0:
                        target.pips.addPips(effect.param)

                case SpellEffects.modify_power_pips:
                    if effect.param < 0:
                        target.pips.destroyPips(-effect.param * 2)
                    elif effect.param > 0:
                        target.pips.addPips(effect.param * 2)

                case SpellEffects.modify_shadow_pips:
                    if effect.param < 0:
                        target.pips.destroyShadowPips(-effect.param)
                    elif effect.param > 0:
                        target.pips.addShadowPips(effect.param)

                case SpellEffects.damage_over_time | SpellEffects.deferred_damage:
                    dotdamage = calculateDamage(player, target, effect.param, effect.school, card.school, dot=True)
                    target.overtimes.append(Overtime(player, dotdamage, effect.school, effect.rounds, effect.spelleffect, effect.disposition))
                
                case SpellEffects.heal_over_time:
                    hotheal = calculateHeal(player, target, effect.param, effect.school, card.school, hot=True)
                    target.overtimes.append(Overtime(player, hotheal, effect.school, effect.rounds, effect.spelleffect, effect.disposition))
                    
                case SpellEffects.instant_kill:
                    target.current_hp = 0
                    
                case SpellEffects.after_life: # TODO: Afterlifes
                    pass
                
                case SpellEffects.damage_per_total_pip_power:
                    basedamage = effect.param * target.pips.getRawPipValue()
                    target.updateHP(-calculateDamage(player, target, basedamage, effect.school, card.school))
                    
                case SpellEffects.divide_damage:
                    basedamage = effect.param * (0.5**len(targets))
                    target.updateHP(-calculateDamage(player, target, basedamage, effect.school, card.school))
                    
                case SpellEffects.max_health_damage:
                    target.updateHP(-(target.stats.health*effect.param))
                    
                case SpellEffects.add_spell_to_deck:
                    target.deckstate.addCardToTop(effect.param)
                    

            if hangingEffect != None:
                match card.cardType:
                    case CardType.Ward:
                        target.wards.append(hangingEffect)
                    case CardType.Charm:
                        target.charms.append(hangingEffect)
                    case CardType.Aura:
                        if card.objectName != target.auraObjectName:
                            target.auraEffects = []
                            target.auraObjectName = card.objectName
                        target.auraEffects.append(hangingEffect)
                    case CardType.Global:
                        if card.objectName != self.bubbleObjectName:
                            self.bubbleEffects = []
                            self.bubbleObjectName = card.objectName
                        self.bubbleEffects.append(hangingEffect)

            for subeffect in effect.subeffects:
                if not subeffect.condition is None and subeffect.condition(player, subeffect.school, subeffect.disposition):
                    self.recursiveExecuteEffects(player, card, subeffect)

    def executeTurn(self, player: Player, card: Card, targets: List[int]) -> ExecutionOutcomes:
        if card == None:
            return ExecutionOutcomes.Pass
        if player.stunned:
            player.stunned = False
            return ExecutionOutcomes.Stunned
        if not calculateAccuracy(player, card):
            return ExecutionOutcomes.Fizzle

        for effect in card.effects:
            if effect.condition is None or effect.condition(player, effect.school, effect.disposition):
                self.recursiveExecuteEffects(player, card, effect, targets)

        for charm in player.charms:
            charm: Charm
            if charm.used:
                player.charms.remove(charm)

        player.pips.subtractPips(num=card.rank, extraPipReq=card.extraPipReq, cardSchool=card.school, mastery=player.school, pserve=player.stats.pipConserve)

        return ExecutionOutcomes.Success

    def turn(self, player: Player, used_card: Card, targets: List[int]):
        if player.current_hp <= 0:
            return
        
        # Tick player's OTs
        for ot in reversed(player.overtimes):
            ot: Overtime
            match ot.spellEffect:
                case SpellEffects.damage_over_time:
                    player.updateHP(-calculateDOT(player, ot))
                case SpellEffects.heal_over_time:
                    player.updateHP(calculateHOT(player, ot))
                case SpellEffects.deferred_damage:
                    if ot.rounds == 1:
                        player.updateHP(-calculateDOT(player, ot))
                    else:
                        ot.tick()

            if ot.rounds == 0:
                player.overtimes.remove(ot)

        if player.current_hp > 0:
            # Execute Turn
            outcome = self.executeTurn(player, used_card, targets)
            print(outcome)
            match outcome:
                case ExecutionOutcomes.Pass | ExecutionOutcomes.Stunned:
                    pass
                case ExecutionOutcomes.Fizzle:
                    player.deckstate.hand.remove(used_card)
                    player.deckstate.mainDeck.insert(randint(0, len(player.deckstate.mainDeck)), used_card)
                case ExecutionOutcomes.Success:
                    player.deckstate.hand.remove(used_card)
                    player.deckstate.usedCards.append(used_card)

            # Tick auras
            for aura in player.auraEffects:
                aura: Aura
                aura.rounds -= 1
                if aura.rounds <= 0:
                    player.auraEffects.remove(aura)
                    
            if len(player.auraEffects) == 0:
                player.auraObjectName = ""

        # Evaluate Win
        team1_dead_count = 0
        for slot in self.team1.slots:
            if slot == None or slot.current_hp <= 0:
                team1_dead_count += 1
                
        team2_dead_count = 0
        for slot in self.team2.slots:
            if slot == None or slot.current_hp <= 0:
                team2_dead_count += 1
                
        if team1_dead_count == 4 and team2_dead_count == 4:
            self.team1.win = True
            self.team2.win = True
        elif team1_dead_count == 4 and team2_dead_count < 4:
            self.team2.win = True
        elif team2_dead_count == 4 and team1_dead_count < 4:
            self.team1.win = True

        # Player draws from main
        player.deckstate.drawMain()
        player.deckstate.setAllHandToDiscardable()
        player.addRoundPip()
        
    def __repr__(self) -> str:
        return f"{self.team1}\n\n{self.team2}"
