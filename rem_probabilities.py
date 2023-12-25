from itertools import product

# Version 1.2.1 I explicitly do not give permission to use without my Consent :)

def main():
    probs = [calculate_dice_outcomes_avd(3, 3, True), calculate_dice_outcomes_avd(3, 2),
             calculate_dice_outcomes_avd(3, 1), calculate_dice_outcomes_avd(2, 2),
             calculate_dice_outcomes_avd(2, 1)]
    # Append the calculated probabilities for each scenario to the list

    # Print out the probabilities for each scenario
    for scenario in probs:
        print(scenario)
    return 0


def calculate_dice_outcomes_avd(a, d, is_capital=False):
    # All possible rolls for attacker and defender dice
    attacker_dice_combinations = list(product(range(1, 7), repeat=a))
    defender_dice_combinations = list(product(range(1, 7), repeat=d))

    # Outcomes
    outcomes = {
        'attacker_wins' + str(a) + "v" + str(d): 0,
        'defender_wins' + str(a) + "v" + str(d): 0,
        'tie' + str(a) + "v" + str(d): 0,
    }

    outcomes_capital = {
        'attacker_wins_big' + str(a) + "v" + str(d): 0,
        'attacker_wins_small' + str(a) + "v" + str(d): 0,
        'defender_wins_small' + str(a) + "v" + str(d): 0,
        'defender_wins_big' + str(a) + "v" + str(d): 0,
    }

    if is_capital == False:
        # iterate through dice combinations
        for attacker_dice in attacker_dice_combinations:
            for defender_dice in defender_dice_combinations:
                # Sort dice so that we can compare the highest ones first
                sorted_attacker_dice = sorted(attacker_dice, reverse=True)[:max(2, a)]
                sorted_defender_dice = sorted(defender_dice, reverse=True)[:max(2, d)]

                # Determine the outcome of this dice roll
                attacker_wins = sum(a >= d for a, d in zip(sorted_attacker_dice, sorted_defender_dice))
                defender_wins = sum(d > a for a, d in zip(sorted_attacker_dice, sorted_defender_dice))

                # Update the outcomes based on the dice roll results
                if attacker_wins > defender_wins:
                    outcomes['attacker_wins' + str(a) + "v" + str(d)] += 1
                elif defender_wins > attacker_wins:
                    outcomes['defender_wins' + str(a) + "v" + str(d)] += 1
                else:
                    outcomes['tie' + str(a) + "v" + str(d)] += 1

        # Total possible outcomes
        total_outcomes = len(attacker_dice_combinations) * len(defender_dice_combinations)

        # Calculate probabilities
        probabilities = {outcome: count / total_outcomes for outcome, count in outcomes.items()}
        counts = {outcome: count for outcome, count in outcomes.items()}
        return probabilities, counts, {total_outcomes}
    else:
        # iterate through dice combinations
        for attacker_dice in attacker_dice_combinations:
            for defender_dice in defender_dice_combinations:
                # Sort dice so that we can compare the highest ones first
                sorted_attacker_dice = sorted(attacker_dice, reverse=True)[:max(3, a)]
                sorted_defender_dice = sorted(defender_dice, reverse=True)[:max(3, d)]

                # Determine the outcome of this dice roll
                attacker_wins = sum(a > d for a, d in zip(sorted_attacker_dice, sorted_defender_dice))
                defender_wins = sum(d >= a for a, d in zip(sorted_attacker_dice, sorted_defender_dice))

                # Update the outcomes based on the dice roll results
                if attacker_wins > defender_wins and ((attacker_wins - defender_wins) > 1):
                    outcomes_capital['attacker_wins_big' + str(a) + "v" + str(d)] += 1
                elif attacker_wins > defender_wins and ((attacker_wins - defender_wins) == 1):
                    outcomes_capital['attacker_wins_small' + str(a) + "v" + str(d)] += 1
                elif defender_wins > attacker_wins and ((defender_wins - attacker_wins) > 1):
                    outcomes_capital['defender_wins_big' + str(a) + "v" + str(d)] += 1
                elif defender_wins > attacker_wins and ((defender_wins - attacker_wins) == 1):
                    outcomes_capital['defender_wins_small' + str(a) + "v" + str(d)] += 1

        # Total possible outcomes
        total_outcomes = len(attacker_dice_combinations) * len(defender_dice_combinations)

        # Calculate probabilities
        probabilities = {outcome: count / total_outcomes for outcome, count in outcomes_capital.items()}
        counts = {outcome: count for outcome, count in outcomes_capital.items()}
        return probabilities, counts, {total_outcomes}


main()
