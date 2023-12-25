from enum import Enum
import timeit as ti
import numpy as np

# Version 1.2.1 I explicitly do not give permission to use without my Consent :)
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

    # Stage 1 - Gaussian Sampling
    def stage_1_sim(self, attackers_init, defenders_init):
        # Initialize troop count
        attackers_count, defenders_count = attackers_init, defenders_init

        # Retrieve battle parameters
        mean_troop_loss_att = self.battle_params.mean_troop_loss_att
        mean_troop_loss_def = self.battle_params.mean_troop_loss_def
        variance_loss_att = self.battle_params.variance_loss_att
        variance_loss_def = self.battle_params.variance_loss_def

        # Estimate N
        n_estimate = self.estimate_n(mean_troop_loss_att, mean_troop_loss_att, attackers_count, defenders_count)

        # Scale mean and variance
        mean_troop_loss_att_gaussian = mean_troop_loss_att * n_estimate
        mean_troop_loss_def_gaussian = mean_troop_loss_def * n_estimate
        variance_loss_att_gaussian = variance_loss_att * np.sqrt(n_estimate)
        variance_loss_def_gaussian = variance_loss_def * np.sqrt(n_estimate)

        # Simulate N skirmishes by randomly sampling from the Gaussian distribution curves
        attackers_simulated_loss = np.random.normal(mean_troop_loss_att_gaussian, variance_loss_att_gaussian, 1)
        defenders_simulated_loss = np.random.normal(mean_troop_loss_def_gaussian, variance_loss_def_gaussian, 1)

        # Update troop counts
        attackers_count -= attackers_simulated_loss
        defenders_count -= defenders_simulated_loss


        # Return updated troop counts
        print("Stage 1: " + str(int(np.round(attackers_count))) + " " +  str(int(np.round(defenders_count))))
        return int(np.round(attackers_count)), int(np.round(defenders_count))

    # Stage 2 - Probabilistic Simulation
    def stage_2_sim(self, attackers_initial, defenders_initial):
        # Initialize troop counts
        attackers_count, defenders_count = attackers_initial, defenders_initial

        # Define which battle type will be simulated
        if self.battle_type == BattleType.CAPITAL:
            # Initialize outcome and probability dictionary
            results = ['att_win_big', 'att_win_small', 'def_win_big', 'def_win_small']
            probabilities = [self.battle_params.prob_att_win_big, self.battle_params.prob_att_win_small,
                             self.battle_params.prob_def_win_big, self.battle_params.prob_def_win_small]
            while attackers_count > 50 and defenders_count > 50:
                outcome = np.random.choice(results, p=probabilities)
                # Apply troop count losses based on the selected outcome
                if outcome == 'att_win_big':
                    # Attacker wins big
                    defenders_count -= 3
                elif outcome == 'att_win_small':
                    # Attacker wins small
                    defenders_count -= 2
                    attackers_count -= 1
                elif outcome == 'def_win_big':
                    # Defender wins big
                    attackers_count -= 3
                elif outcome == 'def_win_small':
                    # Defender wins small
                    attackers_count -= 2
                    defenders_count -= 1
        else:
            # Initialize outcome and probability dictionary
            results = ['att_win', 'def_win', 'tie']
            probabilities = [self.battle_params.prob_att_win, self.battle_params.prob_def_win,
                             self.battle_params.prob_tie]
            while attackers_count > 50 and defenders_count > 50:
                outcome = np.random.choice(results, p=probabilities)
                # Apply troop count losses based on the selected outcome
                if outcome == 'att_win':
                    defenders_count -= 2
                elif outcome == 'def_win':
                    attackers_count -= 2
                else:
                    defenders_count -= 1
                    attackers_count -= 1
        print("Stage 2: " + str(attackers_count) + " " + str(defenders_count))
        return attackers_count, defenders_count

    # Stage 3 - Dice Rolling
    def stage_3_sim(self, attacker_initial, defender_initial):
        # Initialize attacker count
        attacker_count, defender_count = attacker_initial, defender_initial

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

        print("Stage 3: " + str(attacker_count) + " " + str(defender_count))
        # Return final simulation result
        return attacker_count, defender_count

    # Battle simulation logic
    def simulate_battle(self):
        # Initialize troop count
        attacker_count, defender_count = self.attackers_count, self.defenders_count

        # Loop battle sim until terminal state is reached
        while attacker_count > 1 and defender_count > 0:
            # Stage 1 - Gaussian Sampling
            if attacker_count >= 150 and defender_count >= 150:
                attacker_count, defender_count = self.stage_1_sim(attacker_count, defender_count)
            # Stage 2 - Probabilistic Simulation
            elif attacker_count > 50 and defender_count > 50 and (attacker_count < 150 or defender_count < 150):
                attacker_count, defender_count = self.stage_2_sim(attacker_count, defender_count)
            # Stage 3 - Deterministic Simulation
            else:
                attacker_count, defender_count = self.stage_3_sim(attacker_count, defender_count)

        # Return simulation results
        return attacker_count, defender_count


# Main function to use and interact with RiskBattle class
def main():

    return 0


main()
