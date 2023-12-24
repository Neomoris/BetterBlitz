using Combinatorics

function calculate_dice_outcomes_avd(a::Int, d::Int, is_capital::Bool=false)
    # All possible rolls for attacker and defender dice
    attacker_dice_combinations = collect(product(1:6, 1:a))
    defender_dice_combinations = collect(product(1:6, 1:d))

    # Outcomes
    outcomes = Dict(
        "attacker_wins" * string(a) * "v" * string(d) => 0,
        "defender_wins" * string(a) * "v" * string(d) => 0,
        "tie" * string(a) * "v" * string(d) => 0
    )

    outcomes_capital = Dict(
        "attacker_wins_big" * string(a) * "v" * string(d) => 0,
        "attacker_wins_small" * string(a) * "v" * string(d) => 0,
        "defender_wins_small" * string(a) * "v" * string(d) => 0,
        "defender_wins_big" * string(a) * "v" * string(d) => 0
    )

    if !is_capital
        # iterate through dice combinations
        for attacker_dice in attacker_dice_combinations
            for defender_dice in defender_dice_combinations
                # Sort dice so that we can compare the highest ones first
                sorted_attacker_dice = sort(attacker_dice, rev=true)[1:max(2, a)]
                sorted_defender_dice = sort(defender_dice, rev=true)[1:max(2, d)]

                # Determine the outcome of this dice roll
                attacker_wins = sum(a > d for (a, d) in zip(sorted_attacker_dice, sorted_defender_dice))
                defender_wins = sum(d >= a for (a, d) in zip(sorted_attacker_dice, sorted_defender_dice))

                # Update the outcomes based on the dice roll results
                if attacker_wins > defender_wins
                    outcomes["attacker_wins"*string(a)*"v"*string(d)] += 1
                elseif defender_wins > attacker_wins
                    outcomes["defender_wins"*string(a)*"v"*string(d)] += 1
                else
                    outcomes["tie"*string(a)*"v"*string(d)] += 1
                end
            end
        end

        # Total possible outcomes
        total_outcomes = length(attacker_dice_combinations) * length(defender_dice_combinations)

        # Calculate probabilities
        probabilities = Dict(outcome => count / total_outcomes for (outcome, count) in outcomes)
        counts = Dict(outcome => count for (outcome, count) in outcomes)
        return probabilities, counts, total_outcomes
    else
        # iterate through dice combinations
        for attacker_dice in attacker_dice_combinations
            for defender_dice in defender_dice_combinations
                # Sort dice so that we can compare the highest ones first
                sorted_attacker_dice = sort(attacker_dice, rev=true)[1:max(3, a)]
                sorted_defender_dice = sort(defender_dice, rev=true)[1:max(3, d)]

                # Determine the outcome of this dice roll
                attacker_wins = sum(a > d for (a, d) in zip(sorted_attacker_dice, sorted_defender_dice))
                defender_wins = sum(d >= a for (a, d) in zip(sorted_attacker_dice, sorted_defender_dice))

                # Update the outcomes based on the dice roll results
                if attacker_wins > defender_wins && ((attacker_wins - defender_wins) > 1)
                    outcomes_capital["attacker_wins_big"*string(a)*"v"*string(d)] += 1
                elseif attacker_wins > defender_wins && ((attacker_wins - defender_wins) == 1)
                    outcomes_capital["attacker_wins_small"*string(a)*"v"*string(d)] += 1
                elseif defender_wins > attacker_wins && ((defender_wins - attacker_wins) > 1)
                    outcomes_capital["defender_wins_big"*string(a)*"v"*string(d)] += 1
                elseif defender_wins > attacker_wins && ((defender_wins - attacker_wins) == 1)
                    outcomes_capital["defender_wins_small"*string(a)*"v"*string(d)] += 1
                end
            end
        end

        # Total possible outcomes
        total_outcomes = length(attacker_dice_combinations) * length(defender_dice_combinations)

        # Calculate probabilities
        probabilities = Dict(outcome => count / total_outcomes for (outcome, count) in outcomes_capital)
        counts = Dict(outcome => count for (outcome, count) in outcomes_capital)
        return probabilities, counts, total_outcomes
    end
end

function main()
    probs = [calculate_dice_outcomes_avd(3, 3, true), calculate_dice_outcomes_avd(3, 2),
        calculate_dice_outcomes_avd(3, 1), calculate_dice_outcomes_avd(2, 2),
        calculate_dice_outcomes_avd(2, 1)]
    # Append the calculated probabilities for each scenario to the list

    # Print out the probabilities for each scenario
    for scenario in probs
        println(scenario)
    end
    return 0
end

main()
