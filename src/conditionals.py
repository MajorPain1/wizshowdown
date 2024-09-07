

from src.enums import School, Disposition
from src.hangingeffect import Ward, Charm, Overtime
from src.player import Player

# Handled elsewhere
def random(player: Player, num: int, disposition: Disposition):
    return

def xpip(player: Player, num: int, disposition: Disposition):
    return

def numTargets(player: Player, num: int, disposition: Disposition):
    return

# Player reqs
def playerIsSchool(player: Player, num: int, disposition: Disposition):
    return player.school == School(num)

def playerHasWards(player: Player, num: int, disposition: Disposition):
    num_wards = 0
    for ward in reversed(player.wards):
        ward: Ward
        if ward.getDisposition(player) == disposition:
            num_wards += 1
    
    return num_wards >= num

def playerHasCharms(player: Player, num: int, disposition: Disposition):
    num_charms = 0
    for charm in reversed(player.charms):
        charm: Charm
        if charm.getDisposition(player) == disposition:
            num_charms += 1

    return num_charms >= num

def playerHasOvertimes(player: Player, num: int, disposition: Disposition):
    num_overtimes = 0
    for overtime in reversed(player.overtimes):
        overtime: Overtime
        if overtime.getDisposition(player) == disposition:
            num_overtimes = 1

    return num_overtimes >= num

def playerHasPips(player: Player, num: int, disposition: Disposition):
    return player.pips.sumTotalValue() >= num

def playerHasShadowPips(player: Player, num: int, disposition: Disposition):
    return len(player.pips.shadow_pips) >= num

# TODO: Has Minion

def playerHasHealth(player: Player, range: range, disposition: Disposition):
    hp_percent = ((player.current_hp*100) / player.stats.health)
    return (range[0] <= hp_percent) and (hp_percent <= range[-1])


# Opponent reqs
def opponentIsSchool(player: Player, school: School, disposition: Disposition):
    return player.opponent.school == school

def opponentHasWards(player: Player, num: int, disposition: Disposition):
    num_wards = 0
    for ward in reversed(player.opponent.wards):
        ward: Ward
        if ward.getDisposition(player) == disposition:
            num_wards += 1
    
    return num_wards >= num

def opponentHasCharms(player: Player, num: int, disposition: Disposition):
    num_charms = 0
    for charm in reversed(player.opponent.charms):
        charm: Charm
        if charm.getDisposition(player) == disposition:
            num_charms += 1

    return num_charms >= num

def opponentHasOvertimes(player: Player, num: int, disposition: Disposition):
    num_overtimes = 0
    for overtime in reversed(player.opponent.overtimes):
        overtime: Overtime
        if overtime.getDisposition(player) == disposition:
            num_overtimes = 1

    return num_overtimes >= num

def opponentHasPips(player: Player, num: int, disposition: Disposition):
    return player.opponent.pips.sumTotalValue() >= num

def opponentHasShadowPips(player: Player, num: int, disposition: Disposition):
    return len(player.opponent.pips.shadow_pips) >= num

def opponentHasHealth(player: Player, range: range, disposition: Disposition):
    hp_percent = ((player.opponent.current_hp*100) / player.opponent.stats.health)
    return (range[0] <= hp_percent) and (hp_percent <= range[-1])