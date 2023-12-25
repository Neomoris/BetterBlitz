# Version 1.2.1 I explicitly do not give permission to use without my Consent :)

#({'attacker_wins_big3v3': 0.1376028806584362, 'attacker_wins_small3v3': 0.21469907407407407, 'defender_wins_small3v3': 0.2646604938271605, 'defender_wins_big3v3': 0.3830375514403292}, {'attacker_wins_big3v3': 6420, 'attacker_wins_small3v3': 10017, 'defender_wins_small3v3': 12348, 'defender_wins_big3v3': 17871}, {46656})
std_dev_att_3v3 = 1.0646471604257168
std_dev_def_3v3 = 0.859159267051949
std_dev_3v2 = 0.8111523291232738
prob_att_win_3v2 = 0.37165637860082307
prob_def_win_3v2 = 0.2925668724279835
prob_tie_3v2 = 0.3357767489711934
mean_loss_att_3v2 = 0.9209104938271604
mean_loss_def_3v2 = 1.0790895061728396
mean_loss_att_3v3 = 1.9430941358024691
mean_loss_def_3v3 = 1.0569058641975309

test_var_att = (0.37165637860082307*((0 - 0.9209104938271604)**2))
test_var_def = (0.37165637860082307*((2 - 1.0790895061728396)**2))
print("var att = " + str(test_var_att) + ". var def = " + str(test_var_def))