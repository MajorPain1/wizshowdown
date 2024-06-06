from src.enums import School

import PySimpleGUI as sg
import json
import string

alphabet = list(string.ascii_uppercase)
alphabet_index = 0

effectList = []

sg.theme("DarkBlue17")

effecttree = sg.TreeData()


spelleffects = [
    'invalid_spell_effect',
    'damage',
    'damage_no_crit',
    'heal',
    'heal_percent',
    'set_heal_percent',
    'steal_health',
    'reduce_over_time',
    'detonate_over_time',
    'push_charm',
    'steal_charm',
    'push_ward',
    'steal_ward',
    'push_over_time',
    'steal_over_time',
    'remove_charm',
    'remove_ward',
    'remove_over_time',
    'remove_aura',
    'swap_all',
    'swap_charm',
    'swap_ward',
    'swap_over_time',
    'modify_incoming_damage',
    'modify_incoming_damage_flat',
    'maximum_incoming_damage',
    'modify_incoming_heal',
    'modify_incoming_heal_flat',
    'modify_incoming_damage_type',
    'modify_incoming_armor_piercing',
    'modify_outgoing_damage',
    'modify_outgoing_damage_flat',
    'modify_outgoing_heal',
    'modify_outgoing_heal_flat',
    'modify_outgoing_damage_type',
    'modify_outgoing_armor_piercing',
    'bounce_next',
    'bounce_previous',
    'bounce_back',
    'bounce_all',
    'absorb_damage',
    'absorb_heal',
    'modify_accuracy',
    'dispel',
    'confusion',
    'cloaked_charm',
    'cloaked_ward',
    'stun_resist',
    'clue',
    'pip_conversion',
    'crit_boost',
    'crit_block',
    'polymorph',
    'delay_cast',
    'modify_card_cloak',
    'modify_card_damage',
    'modify_card_accuracy',
    'modify_card_mutation',
    'modify_card_rank',
    'modify_card_armor_piercing',
    'summon_creature',
    'teleport_player',
    'stun',
    'dampen',
    'reshuffle',
    'mind_control',
    'modify_pips',
    'modify_power_pips',
    'modify_shadow_pips',
    'modify_hate',
    'damage_over_time',
    'heal_over_time',
    'modify_power_pip_chance',
    'modify_rank',
    'stun_block',
    'reveal_cloak',
    'instant_kill',
    'after_life',
    'deferred_damage',
    'damage_per_total_pip_power',
    'modify_card_heal',
    'modify_card_charm',
    'modify_card_warn',
    'modify_card_outgoing_damage',
    'modify_card_outgoing_accuracy',
    'modify_card_outgoing_heal',
    'modify_card_outgoing_armor_piercing',
    'modify_card_incoming_damage',
    'modify_card_absorb_damage',
    'cloaked_ward_no_remove',
    'add_combat_trigger_list',
    'remove_combat_trigger_list',
    'backlash_damage',
    'modify_backlash',
    'intercept',
    'shadow_self',
    'shadow_creature',
    'modify_shadow_creature_level',
    'select_shadow_creature_attack_target',
    'shadow_decrement_turn',
    'crit_boost_school_specific',
    'spawn_creature',
    'unpolymorph',
    'power_pip_conversion',
    'protect_card_beneficial',
    'protect_card_harmful',
    'protect_beneficial',
    'protect_harmful',
    'divide_damage',
    'collect_essence',
    'kill_creature',
    'dispel_block',
    'confusion_block',
    'modify_pip_round_rate',
    'max_health_damage',
    'untargetable',
    'make_targetable',
    'force_targetable',
    'remove_stun_block',
    'exit_combat',
    'suspend_pips',
    'resume_pips',
    'auto_pass',
    'stop_auto_pass',
    'vanish',
    'stop_vanish',
    'max_health_heal',
    'heal_by_ward',
    'taunt',
    'pacify',
    'remove_target_restriction',
    'convert_hanging_effect',
    'add_spell_to_deck',
    'add_spell_to_hand',
    'modify_incoming_damage_over_time',
    'modify_incoming_heal_over_time',
    'modify_card_damage_by_rank',
    'push_converted_charm',
    'steal_converted_charm',
    'push_converted_ward',
    'steal_converted_ward',
    'push_converted_over_time',
    'steal_converted_over_time',
    'remove_converted_charm',
    'remove_converted_ward',
    'remove_converted_over_time',
    'modify_over_time_duration',
    'modify_school_pips',
]

effect_targets = [
    'invalid_target',
    'spell',
    'specific_spells',
    'target_global',
    'enemy_team',
    'enemy_team_all_at_once',
    'friendly_team',
    'friendly_team_all_at_once',
    'enemy_single',
    'friendly_single',
    'minion',
    'friendly_minion',
    'self',
    'at_least_one_enemy',
    'preselected_enemy_single',
    'multi_target_enemy',
    'multi_target_friendly',
    'friendly_single_not_me'
]

schools = ['Universal', 'Fire', 'Ice', 'Storm', 'Myth', 'Life', 'Death', 'Balance', 'Shadow', 'Star', 'Sun', 'Moon']

school_dict = {
    'Universal': 0,
    'Fire': 2343174,
    'Ice': 72777,
    'Storm': 83375795,
    'Myth': 2448141,
    'Life': 2330892,
    'Death': 78318724,
    'Balance': 1027491821,
    'Shadow': 1429009101
}

dispositions = [
    'both',
    'beneficial',
    'harmful'
]

conditions = [
    'random',
    'xpip',
    'playerIsSchool',
    'playerHasWards',
    'playerHasCharms',
    'playerHasOvertimes',
    'playerHasPips',
    'playerHasShadowPips',
    'playerHasHealth',
    'opponentIsSchool',
    'opponentHasWards',
    'opponentHasCharms',
    'opponentHasOvertimes',
    'opponentHasPips',
    'opponentHasShadowPips',
    'opponentHasHealth'    
]

layout = [
    [sg.Text('Quick Card Builder')],
    [sg.Text('Name', size=(13,1)), sg.InputText(key='name', size=(20,1)), sg.Text("ObjectName", size=(13,1)), sg.InputText(key='objectName', size=(20,1))],
    [sg.Text("School", size=(13,1)), sg.OptionMenu(schools, key='school'), sg.Text("Accuracy", size=(13,1)), sg.OptionMenu(['100', 'Regular', 'Lore'], key='accuracy', default_value="100")],
    [sg.Text("Rank", size=(13,1)), sg.Input(key='rank', default_text=0, size=(5,1)), sg.Text("Card Type", size=(13,1)), sg.OptionMenu(['Damage', 'Heal','Ward','Charm','Drain','AOE','Aura','Global','Enchant'], default_value='Damage', key='cardType')],
    [sg.Text("Is Treasure Card", size=(13,1)), sg.OptionMenu(['True', 'False'], default_value='False', key='istc'), sg.Text("No Reshuffle", size=(13,1)), sg.OptionMenu(['True', 'False'], default_value='False',key='noreshuf')],
    [sg.Text("Discardable", size=(13,1)), sg.OptionMenu(['True', 'False'], default_value='True',key='discardable'), sg.Text("Trainable", size=(13,1)), sg.OptionMenu(['True', 'False'], default_value='True',key='trainable')],
    [sg.Text("Copy Limit", size=(13,1)), sg.Input(key='copyLimit', default_text=6, size=(5,1)), sg.Text("Level Requirement", size=(13,1)), sg.Input(key='levelreq', default_text=0, size=(5,1))],
    [sg.Text("Extra Pips"), 
        sg.Text("Fire", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="fire"), 
        sg.Text("Ice", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="ice"),
        sg.Text("Storm", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="storm"),
        sg.Text("Myth", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="myth"),
        sg.Text("Life", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="life"),
        sg.Text("Death", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="Death"),
        sg.Text("Balance", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="balance"),
        sg.Text("Shadow", size=(6,1)), sg.InputText(default_text=0, size=(2,1), key="shadow"),
    ],
    [sg.Text("Effect Tree")],
    [sg.Tree(effecttree, headings=["Param", "School", "Rounds", "Spell Effect", "Target", "Disposition", "Condition", "Condition Value"], key="tree")],
    [sg.Text("Add Effect")],
    [ 
        sg.Text("Parent"), sg.InputText(default_text='', size=(5,1), key="effectparent"),
        sg.Text("Param"), sg.InputText(default_text='', size=(5,1), key="effectparam"),  
        sg.Text("School"), sg.OptionMenu(schools, key='effectschool'), 
        sg.Text("Rounds"), sg.InputText(default_text=0, size=(5,1), key="effectrounds"),
    ],
    [ 
        sg.Text("Spell Effect"), sg.OptionMenu(spelleffects, key='spelleffect'), 
        sg.Text("Effect Target"), sg.OptionMenu(effect_targets, key='effecttarget'),
        sg.Text("Disposition"), sg.OptionMenu(dispositions, key='effectdisposition'),
    ],
    [
        sg.Text("Condition"), sg.OptionMenu(conditions, key='effectcondition'),
        sg.Text("Conditional Value"), sg.InputText(size=(5,1), key="effectcv"),
    ],
    [sg.Button("Add Effect"), sg.Button("Clear Effect Tree")],
    [sg.Submit(), sg.Cancel(), sg.Button("Clear"), sg.Input(size=(0, 0), enable_events=True, key='File'), sg.FileBrowse()]
]

outputKeys = [
    'name',
    'objectName',
    'school',
    'accuracy',
    'rank',
    'cardType',
    'istc',
    'discardable',
    'trainable',
    'copyLimit',
    'levelreq',
    'extraPipReq',
    'spelleffects'
]

schoolacc = {
    "Fire": 75,
    "Ice": 80,
    "Storm": 70,
    "Myth": 80,
    "Life": 90,
    "Death": 85,
    "Balance": 85,
    "Star": 100,
    "Sun": 100,
    "Moon": 100,
    "Shadow": 100,
}

effectKeys = [
    'effectparent',
    'effectparam',
    'effectschool',
    'effectrounds',
    'spelleffect',
    'effecttarget',
    'effectdisposition',
    'effectcondition',
    'effectcv'
]

def main():
    global alphabet_index
    global effectList

    window = sg.Window('Card Builder', layout)
    tree = window["tree"]

    while True:
        event, values = window.read()

        match event:
            case sg.WIN_CLOSED | 'Cancel':
                break

            case "Submit":
                outputDict = {}
                for key, value in values.items():
                    if key in outputKeys:
                        if key == "school":
                            value = school_dict[value]

                        outputDict[key] = value

                outputDict['copyLimit'] = int(outputDict['copyLimit'])
                outputDict['rank'] = int(outputDict['rank'])
                outputDict['levelreq'] = int(outputDict['levelreq'])

                if outputDict["accuracy"] == "Regular":
                    outputDict["accuracy"] = schoolacc[outputDict["school"]]
                elif outputDict["accuracy"] == "Lore":
                    outputDict["accuracy"] = schoolacc[outputDict["school"]] - 5
                else:
                    outputDict["accuracy"] = int(outputDict["accuracy"])

                if outputDict['istc'] == 'True':
                    filename = f"cards/tc/{outputDict['objectName']}.json"
                else:
                    filename = f"cards/{outputDict['objectName']}.json"

                for entry in effectList:
                    print(entry)

                with open(filename, 'w') as outfile:
                    outfile.truncate(0)
                    json.dump(outputDict, outfile)

            case "File":
                file = values['File']
                with open(file) as f:
                    data = json.load(f)

                data["school"] = School(data["school"]).name

                for key, value in data.items():
                    window[key].update(value)

                window['File'].update("")

            case "Clear":
                for key, value in values.items():
                    if key in outputKeys:
                        window[key].update("")

            case "Add Effect":
                effectDict = {}
                effectDict['key'] = alphabet[alphabet_index]
                for key, value in values.items():
                        if key in effectKeys:
                            effectDict[key] = value

                effectDict['subeffects'] = []

                treevalues = [
                    effectDict['effectparam'], 
                    effectDict['effectschool'], 
                    effectDict['effectrounds'],
                    effectDict['spelleffect'],
                    effectDict['effecttarget'],
                    effectDict['effectdisposition'],
                    effectDict['effectcondition'],
                    effectDict['effectcv']
                ]

                effectList.append(effectDict)

                effecttree.Insert(parent=effectDict['effectparent'], key=f"{alphabet[alphabet_index]}", text=alphabet[alphabet_index], values=treevalues)
                tree.update(values=effecttree)
                alphabet_index += 1

            case "Clear Effect Tree":
                emptytreedata = sg.TreeData()
                effecttree.tree_dict.clear()
                tree.update(values=emptytreedata)
                alphabet_index = 0



            



if __name__ == "__main__":
    main()

