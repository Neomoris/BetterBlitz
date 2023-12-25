from itertools import product
import numpy as np

# Define probabilities as calculated in rem_probabilities.py
prob_att_win_3v2_zombie = 0.6193415637860082
prob_def_win_3v2_zombie = 0.12590020576131689
prob_tie_3v2_zombie = 0.25475823045267487
prob_att_win_big_3v3 = 0.1376028806584362
prob_def_win_big_3v3 = 0.3830375514403292
prob_att_win_small_3v3 = 0.21469907407407407
prob_def_win_small_3v3 = 0.2646604938271605
prob_tie_3v3 = 0.0
prob_att_win_3v2 = 0.37165637860082307
prob_def_win_3v2 = 0.2925668724279835
prob_tie_3v2 = 0.3357767489711934
prob_att_win_3v1 = 0.6597222222222222
prob_def_win_3v1 = 0.3402777777777778
prob_tie_3v1 = 0.0
prob_att_win_2v2 = 0.22762345679012347
prob_def_win_2v2 = 0.44830246913580246
prob_tie_2v2 = 0.32407407407407407
prob_att_win_2v1 = 0.5787037037037037
prob_def_win_2v1 = 0.4212962962962963
prob_tie_2v1 = 0.0
# Define (expected) death value of a single skirmish. see: calculate_mean(prob_att, prob_def, prob_tie, title, is_v1)
mean_loss_att_3v2_zombie = 0.5065586419753086
mean_loss_def_3v2_zombie = 1.4934413580246915
mean_loss_att_3v3 = 1.8931327160493825
mean_loss_def_3v3 = 1.1068672839506173
mean_loss_att_3v2 = 0.9209104938271604
mean_loss_def_3v2 = 1.0790895061728396
mean_loss_att_3v1 = 0.3402777777777778
mean_loss_def_3v1 = 0.6597222222222222
mean_loss_att_2v2 = 1.220679012345679
mean_loss_def_2v2 = 0.779320987654321
mean_loss_att_2v1 = 0.4212962962962963
mean_loss_def_2v1 = 0.5787037037037037
# Define skirmish variance values
variance_att_3v3 = 1.1380794707322388
variance_def_3v3 = 0.9930492048976274
variance_3v2 = 0.6579681010421119
variance_3v1 = 0.2244888117283922
variance_2v2 = 0.6272266994360662
variance_2v1 = 0.2438057270233201
# Define skirmish standard deviation values
std_dev_att_3v3 = 1.066808075865682
std_dev_def_3v3 = 0.9965185421745184
std_dev_3v2 = 0.8111523291232738
std_dev_3v1 = 0.47380250287265496
std_dev_2v2 = 0.7919764513140944
std_dev_2v1 = 0.49376687517827694


# Calculate mean value of troops lost based on battle type
def calculate_mean(prob_att, prob_def, prob_tie, title, is_v1, is_capital):
    subtractor = 0
    if is_v1:
        subtractor += 1
    mean_att_loss = ((2 - subtractor) * prob_def) + (1 * prob_tie)
    mean_def_loss = ((2 - subtractor) * prob_att) + (1 * prob_tie)
    return title + ": Mean attacker loss is: " + str(mean_att_loss) + " and mean defender loss is " + str(mean_def_loss)


# Calculate variance (Sum of: probability*((xi - u)^2)).
def calculate_variance(a, d, prob_att, prob_def, prob_tie, mean_att, mean_def):
    # Initialize variance for attackers and defenders
    variance_att = 0
    variance_def = 0

    # All possible rolls for attacker and defender dice
    attacker_dice_combinations = list(product(range(1, 7), repeat=a))
    defender_dice_combinations = list(product(range(1, 7), repeat=d))
    combinations = (6 ** a) * (6 ** d)
    # iterate through dice combinations
    for attacker_dice in attacker_dice_combinations:
        for defender_dice in defender_dice_combinations:
            # Sort dice so that we can compare the highest ones first
            sorted_attacker_dice = sorted(attacker_dice, reverse=True)[:min(d, 2)]  # Attacker compares up to d dice
            sorted_defender_dice = sorted(defender_dice, reverse=True)[:d]  # Defender compares up to d dice

            # Determine the outcome of this dice roll
            attacker_wins = sum(att > def_dice for att, def_dice in zip(sorted_attacker_dice, sorted_defender_dice))
            defender_wins = sum(def_dice >= att for att, def_dice in zip(sorted_attacker_dice, sorted_defender_dice))

            if d > 1:
                if attacker_wins > defender_wins:
                    variance_att += ((1 / combinations) * ((0 - mean_att) ** 2))
                    variance_def += ((1 / combinations) * ((2 - mean_def) ** 2))
                elif defender_wins > attacker_wins:
                    variance_att += ((1 / combinations) * ((2 - mean_att) ** 2))
                    variance_def += ((1 / combinations) * ((0 - mean_def) ** 2))
                else:
                    variance_att += ((1 / combinations) * ((1 - mean_att) ** 2))
                    variance_def += ((1 / combinations) * ((1 - mean_def) ** 2))

            elif d == 1:
                if attacker_wins > defender_wins:
                    variance_att += ((1 / combinations) * ((0 - mean_att) ** 2))
                    variance_def += ((1 / combinations) * ((1 - mean_def) ** 2))

                elif defender_wins > attacker_wins:
                    variance_att += ((1 / combinations) * ((1 - mean_att) ** 2))
                    variance_def += ((1 / combinations) * ((0 - mean_def) ** 2))

    return variance_att, variance_def


# Main function file
def main():
    print(calculate_mean(prob_att_win_3v2_zombie, prob_def_win_3v2_zombie, prob_tie_3v2_zombie, "3v2 Zombie", False, False))
    variance_att_zombie, variance_def_zombie = calculate_variance(3, 2, prob_att_win_3v2_zombie, prob_def_win_3v2_zombie, prob_tie_3v2_zombie, mean_loss_att_3v2_zombie, mean_loss_def_3v2_zombie)
    print(variance_att_zombie, variance_def_zombie)
    print(np.sqrt(variance_att_zombie), np.sqrt(variance_def_zombie))
    return 0


main()
