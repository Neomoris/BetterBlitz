using Combinatorics

# Define probabilities as calculated in rem_probabilities.py
const prob_att_win_big_3v3 = 0.1376028806584362
const prob_def_win_big_3v3 = 0.3830375514403292
const prob_att_win_small_3v3 = 0.21469907407407407
const prob_def_win_small_3v3 = 0.2646604938271605
const prob_tie_3v3 = 0.0
const prob_att_win_3v2 = 0.37165637860082307
const prob_def_win_3v2 = 0.2925668724279835
const prob_tie_3v2 = 0.3357767489711934
const prob_att_win_3v1 = 0.6597222222222222
const prob_def_win_3v1 = 0.3402777777777778
const prob_tie_3v1 = 0.0
const prob_att_win_2v2 = 0.22762345679012347
const prob_def_win_2v2 = 0.44830246913580246
const prob_tie_2v2 = 0.32407407407407407
const prob_att_win_2v1 = 0.5787037037037037
const prob_def_win_2v1 = 0.4212962962962963
const prob_tie_2v1 = 0.0

# Define a struct to hold the dice combinations
struct DiceCombinations
    attacker_dice_combinations::Vector{Tuple{Int, Int}}
    defender_dice_combinations::Vector{Tuple{Int, Int}}
end

# Calculate mean value of troops lost based on battle type
function calculate_mean(prob_att::Float64, prob_def::Float64, prob_tie::Float64, title::String, is_v1::Bool, is_capital::Bool)
    subtractor = is_v1 ? 1 : 0
    mean_att_loss = ((2 - subtractor) * prob_def) + (1 * prob_tie)
    mean_def_loss = ((2 - subtractor) * prob_att) + (1 * prob_tie)
    return title * ": Mean attacker loss is: " * string(mean_att_loss) * " and mean defender loss is " * string(mean_def_loss)
end

# Calculate variance (Sum of: probability*((xi - u)^2)).
function calculate_variance(a::Int, d::Int, prob_att::Float64, prob_def::Float64, prob_tie::Float64, mean_att::Float64, mean_def::Float64)
    # Initialize variance for attackers and defenders
    variance_att = 0.0
    variance_def = 0.0

    # All possible rolls for attacker and defender dice
    dice_combinations = DiceCombinations(collect(product(1:6, 1:a)), collect(product(1:6, 1:d)))
    combinations = (6^a)*(6^d)
    # iterate through dice combinations
    for attacker_dice in dice_combinations.attacker_dice_combinations
        for defender_dice in dice_combinations.defender_dice_combinations
            # Sort dice so that we can compare the highest ones first
            sorted_attacker_dice = sort(attacker_dice, rev=true)[1:min(d, 2)]  # Attacker compares up to d dice
            sorted_defender_dice = sort(defender_dice, rev=true)[1:d]  # Defender compares up to d dice

            # Determine the outcome of this dice roll
            attacker_wins = sum(att > def_dice for (att, def_dice) in zip(sorted_attacker_dice, sorted_defender_dice))
            defender_wins = sum(def_dice >= att for (att, def_dice) in zip(sorted_attacker_dice, sorted_defender_dice))

            if d > 1
                if attacker_wins > defender_wins
                    variance_att += ((1/combinations) * ((0 - mean_att) ^ 2))
                    variance_def += ((1/combinations) * ((2 - mean_def) ^ 2))
                elseif defender_wins > attacker_wins
                    variance_att += ((1/combinations) * ((2 - mean_att) ^ 2))
                    variance_def += ((1/combinations) * ((0 - mean_def) ^ 2))
                else
                    variance_att += ((1/combinations) * ((1 - mean_att) ^ 2))
                    variance_def += ((1/combinations) * ((1 - mean_def) ^ 2))
                end
            elseif d == 1
                if attacker_wins > defender_wins
                    variance_att += ((1/combinations) * ((0 - mean_att) ^ 2))
                    variance_def += ((1/combinations) * ((1 - mean_def) ^ 2))
                elseif defender_wins > attacker_wins
                    variance_att += ((1/combinations) * ((1 - mean_att) ^ 2))
                    variance_def += ((1/combinations) * ((0 - mean_def) ^ 2))
                end
            end
        end
    end
    return variance_att, variance_def
end

# Main function file
function main()
    mean_att_loss = (prob_att_win_big_3v3 * 0) + (prob_att_win_small_3v3 * 1) + (prob_def_win_small_3v3 * 2) + (prob_def_win_big_3v3 * 3)
    mean_def_loss = (prob_att_win_big_3v3 * 3) + (prob_att_win_small_3v3 * 2) + (prob_def_win_small_3v3 * 1) + (prob_def_win_big_3v3 * 0)
    println(mean_att_loss, mean_def_loss)

    cont1_att = prob_att_win_big_3v3 * ((0-mean_loss_att_3v3)^2)
    cont2_att = prob_att_win_small_3v3 * ((1-mean_loss_att_3v3)^2)
    cont3_att = prob_def_win_big_3v3 * ((2-mean_loss_att_3v3)^2)
    cont4_att = prob_def_win_big_3v3 * ((3-mean_loss_att_3v3)^2)
    var_att = cont1_att+cont2_att+cont3_att+cont4_att
    cont1_def = prob_att_win_big_3v3 * ((3-mean_loss_def_3v3)^2)
    cont2_def = prob_att_win_small_3v3 * ((2-mean_loss_def_3v3)^2)
    cont3_def = prob_def_win_big_3v3 * ((1-mean_loss_def_3v3)^2)
    cont4_def = prob_def_win_small_3v3 * ((0-mean_loss_def_3v3)^2)
    var_def = cont1_def + cont2_def + cont3_def + cont4_def

    println(var_att, var_def)
    println(sqrt(var_att), sqrt(var_def))
    return 0
end

main()
