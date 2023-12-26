from rem_sim_dice import RiskBattle
from rem_sim_dice import BattleType
import numpy as np


# BetterBlitz 1.2.3 I explicitly do not give permission for use without consent
def main():
    # Initialize Heatmap
    risk_heatmap = np.zeros((100, 100))
    # Iterate through all combinations of troops from 1-100 for attackers and defenders
    for a in range(1, 100):
        for d in range(1, 100):
            # Instantiate a new RiskBattle class with A,D defenders
            risk_battle = RiskBattle(a, d, BattleType.STANDARD)
            # Initialize win counter
            w = 0
            # Simulate 1000 Battles to generate accurate win-rates
            for _ in range(1, 1000):
                # Unlike rem_sim.py, this one uses pure dice rolls to ensure most "game-accurate" WR percentages
                a_sim, d_sim = risk_battle.simulate_battle()
                if a_sim > d_sim:
                    w += 1
            # Assign winrate to proper heatmap index
            risk_heatmap[a-1][d-1] = float(w / 1000)
    np.savetxt("risk_heatmap.csv", risk_heatmap, delimiter=",")
    return 0


# Run file
main()
