using Random
using Distributions
using Plots

function roll_dice(number_of_dice::Int)
    return sort(rand(1:6, number_of_dice), rev=true)
end

function estimate_n(a_mean::Float64, d_mean::Float64, a_init::Int, d_init::Int)
    n_a = (a_init - 100) / a_mean
    n_d = (d_init - 100) / d_mean
    n = round(min(n_a, n_d))
    return n
end

function stage_1_sim(a_init::Int, d_init::Int, is_capital::Bool)
    a_results, d_results = a_init, d_init
    a_mean_loss = 0.9209104938271604
    d_mean_loss = 1.0790895061728396
    std_dev_att = 0.8111523291232738
    std_dev_def = std_dev_att

    if is_capital
        a_mean_loss = 1.8931327160493825
        d_mean_loss = 1.1068672839506173
        std_dev_att = 1.066808075865682
        std_dev_def = 0.9965185421745184
    end

    n = estimate_n(a_mean_loss, d_mean_loss, a_results, d_results)

    a_mean_loss_gaussian = a_mean_loss * n
    d_mean_loss_gaussian = d_mean_loss * n
    std_dev_att_gaussian = std_dev_att * sqrt(n)
    std_dev_def_gaussian = std_dev_def * sqrt(n)
    println(std_dev_att_gaussian, " ", std_dev_def_gaussian)

    x = range(a_mean_loss_gaussian - 3 * std_dev_att_gaussian, stop=a_mean_loss_gaussian + 3 * std_dev_att_gaussian, length=1000)
    y = pdf(Normal(a_mean_loss_gaussian, std_dev_att_gaussian), x)

    plot(x, y, title="Gaussian Distribution of Skirmish Outcomes (Attackers)", xlabel="Troop Loss", ylabel="Probability Density")

    a_sim_loss = rand(Normal(a_mean_loss_gaussian, std_dev_att_gaussian))
    d_sim_loss = rand(Normal(d_mean_loss_gaussian, std_dev_def_gaussian))
    a_results -= round(a_sim_loss)
    d_results -= round(d_sim_loss)

    return a_results, d_results
end

function stage_2_sim(a_init::Int, d_init::Int, is_capital::Bool)
    a_results, d_results = a_init, d_init
    prob_att_win_big_3v3 = 0.1376028806584362
    prob_def_win_big_3v3 = 0.3830375514403292
    prob_att_win_small_3v3 = 0.21469907407407407
    prob_def_win_small_3v3 = 0.2646604938271605
    prob_att_win = 0.37165637860082307
    prob_def_win = 0.2925668724279835
    prob_tie = 0.3357767489711934

    while a_results > 50 && d_results > 50
        if is_capital
            outcome = rand(["att_win_big", "att_win_small", "def_win_big", "def_win_small"], p=[prob_att_win_big_3v3, prob_att_win_small_3v3, prob_def_win_big_3v3, prob_def_win_small_3v3])
        else
            outcome = rand(["att_win", "def_win", "tie"], p=[prob_att_win, prob_def_win, prob_tie])
        end

        if outcome == "att_win"
            d_results -= 2
            a_results -= 0
        elseif outcome == "def_win"
            a_results -= 2
            d_results -= 0
        elseif outcome == "tie"
            a_results -= 1
            d_results -= 1
        elseif outcome == "att_win_big"
            a_results -= 0
            d_results -= 3
        elseif outcome == "att_win_small"
            a_results -= 1
            d_results -= 2
        elseif outcome == "def_win_big"
            a_results -= 3
            d_results -= 0
        elseif outcome == "def_win_small"
            a_results -= 2
            d_results -= 1
        end

        a_results = max(a_results, 0)
        d_results = max(d_results, 0)
    end

    return a_results, d_results
end

function stage_3_sim(a_init::Int, d_init::Int, is_capital::Bool)
    a_results, d_results = a_init, d_init

    while a_results > 1 && d_results > 0
        a_dice = roll_dice(min(3, a_results))
        d_dice_max = is_capital ? 3 : 2
        d_dice = roll_dice(min(d_dice_max, d_results))

        for (a_die, d_die) in zip(a_dice, d_dice)
            if a_die > d_die
                d_results -= 1
            else
                a_results -= 1
            end
        end

        a_results = max(a_results, 0)
        d_results = max(d_results, 0)
    end

    return a_results, d_results
end

function hybrid_battle_sim(a_initial::Int, d_initial::Int, is_capital::Bool)
    a_results, d_results = a_initial, d_initial

    while a_results > 1 && d_results > 0
        if a_results >= 150 && d_results >= 150
            a_results, d_results = stage_1_sim(a_results, d_results, is_capital)
        elseif a_results > 50 && d_results > 50 && (a_results < 150 || d_results < 150)
            a_results, d_results = stage_2_sim(a_results, d_results, is_capital)
        else
            a_results, d_results = stage_3_sim(a_results, d_results, is_capital)
        end
    end

    return a_results, d_results
end

function main()
    for _ in 1:20
        println(hybrid_battle_sim(35, 35, true))
    end
    println("===============================")
    for _ in 1:20
        println(hybrid_battle_sim(35, 35, false))
    end
    return 0
end

main()
