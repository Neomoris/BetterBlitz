from enum import Enum
import numpy as np
import timeit


# Version 1.2.3 I explicitly do not give permission to use without my Consent :)
# Define the BattleType enum
class BattleType(Enum):
    STANDARD = 1
    CAPITAL = 2
    ZOMBIE = 3


# Define RiskBattle Class
class RiskBattle:
    # Define SubClasses of Risk Battles and the parameters that they have that make them unique
    class StandardBattle:
        max_dice_a = 3
        max_dice_d = 2
        prob_att_win = 0.37165637860082307
        prob_def_win = 0.2925668724279835
        prob_tie = 0.3357767489711934
        mean_troop_loss_att = 0.9209104938271604
        mean_troop_loss_def = 1.0790895061728396
        variance_loss_att = 0.6579681010421119
        variance_loss_def = 0.6579681010421119

    class CapitalBattle:
        max_dice_a = 3
        max_dice_d = 3
        prob_att_win_big = 0.1376028806584362
        prob_att_win_small = 0.21469907407407407
        prob_def_win_big = 0.3830375514403292
        prob_def_win_small = 0.2646604938271605
        mean_troop_loss_att = 1.8931327160493825
        mean_troop_loss_def = 1.1068672839506173
        variance_loss_att = 1.1380794707322388
        variance_loss_def = 0.9930492048976274

    class ZombieBattle:
        max_dice_a = 3
        max_dice_d = 2
        prob_att_win = 0.6193415637860082
        prob_def_win = 0.12590020576131689
        prob_tie = 0.25475823045267487
        mean_troop_loss_att = 0.5065586419753086
        mean_troop_loss_def = 1.4934413580246915
        variance_loss_att = 0.8296555581751642
        variance_loss_def = 0.8296555581751642

    # Initialize the RiskBattle class by defining initial troop count, and battle parameters from SubClass
    def __init__(self, attackers_initial, defenders_initial, battle_type):
        self.attackers_count = attackers_initial
        self.defenders_count = defenders_initial
        self.battle_type = battle_type
        self.battle_params = self.set_battle_parameters()

    # Generate Dice Roll for number_of_dice amount of dice
    @staticmethod
    def roll_dice(number_of_dice):
        return sorted(np.random.randint(1, 7, size=number_of_dice), reverse=True)

    # Estimate amount of skirmishes between attacker troops and defender troops it will take for either to reach 100
    @staticmethod
    def estimate_n(a_mean, d_mean, a_init, d_init):
        n_a = (a_init - 100) / a_mean
        n_d = (d_init - 100) / d_mean
        n = round(min(n_a, n_d))
        return n

    # Function to fill in battle parameters from SubClass into instanced RiskBattle
    def set_battle_parameters(self):
        if self.battle_type == BattleType.STANDARD:
            return self.StandardBattle
        elif self.battle_type == BattleType.CAPITAL:
            return self.CapitalBattle
        elif self.battle_type == BattleType.ZOMBIE:
            return self.ZombieBattle
        else:
            raise ValueError("Invalid battle type")

    def simulate_battle(self):
        # Initialize attacker count
        attacker_count, defender_count = self.attackers_count, self.defenders_count

        # Loop until a final terminal state.
        while attacker_count > 1 and defender_count > 0:
            attacker_dice = self.roll_dice(min(self.battle_params.max_dice_a, attacker_count))
            defender_dice = self.roll_dice(min(self.battle_params.max_dice_d, defender_count))

            # Divide logic by battle calculation; one for zombie logic one for regular.
            if self.battle_type == BattleType.ZOMBIE:
                for attacker_die, defender_die in zip(attacker_dice, defender_dice):
                    if attacker_die >= defender_die:
                        defender_count -= 1  # Defender loses a troop
                    else:
                        attacker_count -= 1  # Attacker loses a troop
            else:
                for attacker_die, defender_die in zip(attacker_dice, defender_dice):
                    if attacker_die > defender_die:
                        defender_count -= 1  # Defender loses a troop
                    else:
                        attacker_count -= 1  # Attacker loses a troop

            # Ensure we don't leave with an impossible (negative) terminal state
            attacker_count = max(attacker_count, 0)
            defender_count = max(defender_count, 0)

        # Return final simulation result
        return attacker_count, defender_count


# Main function to use and interact with RiskBattle class
def main():
    sample_size = 100
    wr_matrix_standard = [[None for _ in range(sample_size)] for _ in range(sample_size)]
    for a in range(1, sample_size):
        for d in range(1, sample_size):
            risk_battle = RiskBattle(a, d, BattleType.STANDARD)
            w = 0
            for _ in range(1, 1000):
                # noinspection SpellCheckingInspection
                asim, dsim = risk_battle.simulate_battle()
                if asim > dsim:
                    w += 1
            wr = w / 1000
            print("wr - " + str(a) + "v" + str(d) + ": " + str(min(100, (wr*100)) )+ "%")
            wr_matrix_standard[a-1][d-1]=wr
    print(wr_matrix_standard)
    return 0


main()
