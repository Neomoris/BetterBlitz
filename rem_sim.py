import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def roll_dice(number_of_dice):
    return sorted(np.random.randint(1, 7, size=number_of_dice), reverse=True)


def estimate_n(a_mean, d_mean, a_init, d_init):
    n_a = (a_init - 100) / a_mean
    n_d = (d_init - 100) / d_mean
    n = round(min(n_a, n_d))
    return n


def stage_1_sim(a_init, d_init, is_capital):
    a_results, d_results = a_init, d_init
    # Define distribution curve variables for Attackers and Defenders. See: rem_main.py
    a_mean_loss = 0.9209104938271604
    d_mean_loss = 1.0790895061728396
    std_dev_att = 0.8111523291232738
    std_dev_def = std_dev_att

    if is_capital:
        a_mean_loss = 1.8931327160493825
        d_mean_loss = 1.1068672839506173
        std_dev_att = 1.066808075865682
        std_dev_def = 0.9965185421745184

    # Estimate N skirmishes
    n = estimate_n(a_mean_loss, d_mean_loss, a_results, d_results)

    # Scale curves into gaussian form over N skirmishes
    a_mean_loss_gaussian = a_mean_loss * n
    d_mean_loss_gaussian = d_mean_loss * n
    std_dev_att_gaussian = std_dev_att * np.sqrt(n)
    std_dev_def_gaussian = std_dev_def * np.sqrt(n)
    print(std_dev_att_gaussian, std_dev_def_gaussian)
    # Create a range of values for plotting the Gaussian distribution
    x = np.linspace(a_mean_loss_gaussian - 3 * std_dev_att_gaussian, a_mean_loss_gaussian + 3 * std_dev_att_gaussian,
                    1000)

    # Create the Gaussian distribution for these values
    y = stats.norm.pdf(x, a_mean_loss_gaussian, std_dev_att_gaussian)

    # Plotting
    plt.plot(x, y)
    plt.title('Gaussian Distribution of Skirmish Outcomes (Attackers)')
    plt.xlabel('Troop Loss')
    plt.ylabel('Probability Density')
    plt.show()
    # Sample expected troop losses from both sides over N skirmishes
    a_sim_loss = np.random.normal(a_mean_loss_gaussian, std_dev_att_gaussian)
    d_sim_loss = np.random.normal(d_mean_loss_gaussian, std_dev_def_gaussian)
    a_results -= round(a_sim_loss)
    d_results -= round(d_sim_loss)
    # Return results variable
    return a_results, d_results


def stage_2_sim(a_init, d_init, is_capital):

    a_results, d_results = a_init, d_init
    # Define probability table RNG will use to simplify skirmish calculations
    prob_att_win_big_3v3 = 0.1376028806584362
    prob_def_win_big_3v3 = 0.3830375514403292
    prob_att_win_small_3v3 = 0.21469907407407407
    prob_def_win_small_3v3 = 0.2646604938271605
    prob_att_win = 0.37165637860082307
    prob_def_win = 0.2925668724279835
    prob_tie = 0.3357767489711934
    while a_results > 50 and d_results > 50:
        # Determine the outcome of the skirmish
        if is_capital:
            outcome = np.random.choice(['att_win_big', 'att_win_small', 'def_win_big', 'def_win_small'],
                                       p=[prob_att_win_big_3v3, prob_att_win_small_3v3, prob_def_win_big_3v3, prob_def_win_small_3v3])
        else:
            outcome = np.random.choice(['att_win', 'def_win', 'tie'],
                                       p=[prob_att_win, prob_def_win, prob_tie])

        # Update troop counts based on the outcome
        if outcome == 'att_win':
            # Attacker wins, defender loses  troops
            d_results -= 2
            a_results -= 0
        elif outcome == 'def_win':
            # Defender wins, attacker loses troops
            a_results -= 2
            d_results -= 0
        elif outcome == 'tie':
            # Tie, both sides lose troops
            a_results -= 1
            d_results -= 1
        elif outcome == 'att_win_big':
            # Attacker wins big, defender loses three troops
            a_results -= 0
            d_results -= 3
        elif outcome == 'att_win_small':
            # Attacker wins small, defender loses two attacker loses one
            a_results -= 1
            d_results -= 2
        elif outcome == 'def_win_big':
            # Defender wins big, attacker loses three troops
            a_results -= 3
            d_results -= 0
        elif outcome == 'def_win_small':
            # Defender wins small, attacker loses two defender loses one.
            a_results -= 2
            d_results -= 1

        # Ensure troop counts don't go below zero
        a_results = max(a_results, 0)
        d_results = max(d_results, 0)
    return a_results, d_results


def stage_3_sim(a_init, d_init, is_capital):
    a_results, d_results = a_init, d_init
    # Stage 3 goes until we reach a terminal state
    while a_results > 1 and d_results > 0:
        # Attacker and defender roll dice based on their troop counts
        a_dice = roll_dice(min(3, a_results))
        d_dice_max = 3 if is_capital else 2  # Defender rolls up to 3 dice if it's a capital
        d_dice = roll_dice(min(d_dice_max, d_results))

        # Compare the dice and determine losses
        for a_die, d_die in zip(a_dice, d_dice):
            if a_die > d_die:
                d_results -= 1  # Defender loses a troop
            else:
                a_results -= 1  # Attacker loses a troop

        # Ensure troop counts don't go below zero
        a_results = max(a_results, 0)
        d_results = max(d_results, 0)

    return a_results, d_results


def hybrid_battle_sim(a_initial, d_initial, is_capital):
    a_results, d_results = a_initial, d_initial
    while a_results > 1 and d_results > 0:
        # Simulation stage logic
        if a_results >= 150 and d_results >= 150:
            # Stage 1: Gaussian distribution sampling
            a_results, d_results = stage_1_sim(a_results, d_results, is_capital)
        elif a_results > 50 and d_results > 50 and (a_results < 150 or d_results < 150):
            # Stage 2: Simplified simulation using 3v2 probability tables
            a_results, d_results = stage_2_sim(a_results, d_results, is_capital)
        else:
            # Stage 3: Pure dice roll simulation
            a_results, d_results = stage_3_sim(a_results, d_results, is_capital)

    return a_results, d_results


def main():
    for _ in range(1, 20):
        print(hybrid_battle_sim(35, 35, True))
    print('===============================')
    for _ in range(1, 20):
        print(hybrid_battle_sim(35, 35, False))
    return 0


main()
