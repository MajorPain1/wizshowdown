from enum import Enum

class School(Enum):
    Universal = 0
    Fire = 1
    Ice = 2
    Storm = 3
    Myth = 4
    Life = 5
    Death = 6
    Balance = 7
    Shadow = 8
    ChromaticSelf = 9
    ChromaticTarget = 10

class CardType(Enum):
    Damage = 0
    Heal = 1
    Ward = 2
    Charm = 3
    Drain = 4
    AOE = 5
    Aura = 6
    Global = 7
    Enchant = 8
    Manipulation = 9

class EquipmentType(Enum):
    Hat = 0
    Robe = 1
    Boots = 2
    Wand = 3
    Athame = 4
    Amulet = 5
    Ring = 6
    Deck = 7
    Mount = 8

class JewelType(Enum):
    Tear = 0
    Circle = 1
    Square = 2
    Triangle = 3
    Sword = 4
    Power = 5
    Shield = 6

class ExecutionOutcomes(Enum):
    Pass = 0
    Fizzle = 1
    Stunned = 2
    Success = 3


class SpellEffects(Enum):
    invalid_spell_effect = 0
    damage = 1
    damage_no_crit = 2
    heal = 3
    heal_percent = 4
    set_heal_percent = 111
    steal_health = 5
    reduce_over_time = 6
    detonate_over_time = 7
    push_charm = 8
    steal_charm = 9
    push_ward = 10
    steal_ward = 11
    push_over_time = 12
    steal_over_time = 13
    remove_charm = 14
    remove_ward = 15
    remove_over_time = 16
    remove_aura = 17
    swap_all = 18
    swap_charm = 19
    swap_ward = 20
    swap_over_time = 21
    modify_incoming_damage = 22
    modify_incoming_damage_flat = 117
    maximum_incoming_damage = 23
    modify_incoming_heal = 24
    modify_incoming_heal_flat = 116
    modify_incoming_damage_type = 25
    modify_incoming_armor_piercing = 26
    modify_outgoing_damage = 27
    modify_outgoing_damage_flat = 119
    modify_outgoing_heal = 28
    modify_outgoing_heal_flat = 118
    modify_outgoing_damage_type = 29
    modify_outgoing_armor_piercing = 30
    bounce_next = 31
    bounce_previous = 32
    bounce_back = 33
    bounce_all = 34
    absorb_damage = 35
    absorb_heal = 36
    modify_accuracy = 37
    dispel = 38
    confusion = 39
    cloaked_charm = 40
    cloaked_ward = 41
    stun_resist = 42
    clue = 109
    pip_conversion = 43
    crit_boost = 44
    crit_block = 45
    polymorph = 46
    delay_cast = 47
    modify_card_cloak = 48
    modify_card_damage = 49
    modify_card_accuracy = 51
    modify_card_mutation = 52
    modify_card_rank = 53
    modify_card_armor_piercing = 54
    summon_creature = 63
    teleport_player = 64
    stun = 65
    dampen = 66
    reshuffle = 67
    mind_control = 68
    modify_pips = 69
    modify_power_pips = 70
    modify_shadow_pips = 71
    modify_hate = 72
    damage_over_time = 73
    heal_over_time = 74
    modify_power_pip_chance = 75
    modify_rank = 76
    stun_block = 77
    reveal_cloak = 78
    instant_kill = 79
    after_life = 80
    deferred_damage = 81
    damage_per_total_pip_power = 82
    modify_card_heal = 50
    modify_card_charm = 55
    modify_card_warn = 56
    modify_card_outgoing_damage = 57
    modify_card_outgoing_accuracy = 58
    modify_card_outgoing_heal = 59
    modify_card_outgoing_armor_piercing = 60
    modify_card_incoming_damage = 61
    modify_card_absorb_damage = 62
    cloaked_ward_no_remove = 84
    add_combat_trigger_list = 85
    remove_combat_trigger_list = 86
    backlash_damage = 87
    ## Need to do all this like bruh is shrike worth it
    modify_backlash = 88
    intercept = 89
    shadow_self = 90
    shadow_creature = 91
    modify_shadow_creature_level = 92
    select_shadow_creature_attack_target = 93
    shadow_decrement_turn = 94
    ##
    crit_boost_school_specific = 95
    spawn_creature = 96
    unpolymorph = 97
    power_pip_conversion = 98
    protect_card_beneficial = 99
    protect_card_harmful = 100
    protect_beneficial = 101
    protect_harmful = 102
    divide_damage = 103
    collect_essence = 104
    kill_creature = 105
    dispel_block = 106
    confusion_block = 107
    modify_pip_round_rate = 108
    max_health_damage = 110
    untargetable = 112
    make_targetable = 113
    force_targetable = 114
    remove_stun_block = 115
    exit_combat = 120
    suspend_pips = 121
    resume_pips = 122
    auto_pass = 123
    stop_auto_pass = 124
    vanish = 125
    stop_vanish = 126
    max_health_heal = 127
    heal_by_ward = 128
    taunt = 129
    pacify = 130
    remove_target_restriction = 131
    convert_hanging_effect = 132
    add_spell_to_deck = 133
    add_spell_to_hand = 134
    modify_incoming_damage_over_time = 135
    modify_incoming_heal_over_time = 136
    modify_card_damage_by_rank = 137
    push_converted_charm = 138
    steal_converted_charm = 139
    push_converted_ward = 140
    steal_converted_ward = 141
    push_converted_over_time = 142
    steal_converted_over_time = 143
    remove_converted_charm = 144
    remove_converted_ward = 145
    remove_converted_over_time = 146
    modify_over_time_duration = 147
    modify_school_pips = 148


class EffectTarget(Enum):
    invalid_target = 0
    spell = 1
    specific_spells = 2
    target_global = 3
    enemy_team = 4
    enemy_team_all_at_once = 5
    friendly_team = 6
    friendly_team_all_at_once = 7
    enemy_single = 8
    friendly_single = 9
    minion = 10
    friendly_minion = 17
    self = 11
    at_least_one_enemy = 13
    preselected_enemy_single = 12
    multi_target_enemy = 14
    multi_target_friendly = 15
    friendly_single_not_me = 16
    

class CardTarget(Enum):
    no_target = 0
    single = 1
    team = 2
    multi_target = 3


class Disposition(Enum):
    both = 0
    beneficial = 1
    harmful = 2