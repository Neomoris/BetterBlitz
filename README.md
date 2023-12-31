BetterBlitz 1.2.3 I explicitly do not give permission to any of the project's contents without consent.


BetterBlitz organizes Battle Size into 3 distinct categories of scale, where each category has a unique solution that optimizes the ratio of computational complexity to accuracy. We begin by defining the deterministic category at the lowest troop count range. Here, the computational requirements to simulate dice roll observations are incredibly low, especially in relation to the near-perfect accuracy we get from dice rolls. We can afford to use the dice roll method in this range, so we do. The second category is defined as the probabilistic stage of simulation in the medium troop count range. Here, we maintain the iterative accuracy of the dice-rolling simulation method but streamline the process by utilizing the aggregate outcome probabilities of a given skirmish as the driving force behind random number generation, as opposed to randomly generating 5 dice per skirmish and then comparing them. Finally, we define the large troop count range as the gaussian simulation; where we utilize the Law of Large Numbers and the Central Limit Theorem to efficiently calculate the aggregate results of a battle in one calculation as opposed to iterating through potentially hundreds of thousands of dice rolls. 
	The entire battle is simulated by transitioning through these calculation methods as the troop counts approach a terminal state – a point where either the attacker or the defender can no longer attack. By being able to transition from one technique to the next as army sizes decrease, we can effectively modulate the computational requirements of the battle and still maintain accuracy in simulation. 
	The Deterministic Stage of simulation is very simple in theory and implementation. We simply simulate dice rolling and generate skirmish results iteratively until we reach a terminal state. This emulates the real-life board game Risk and is the most accurate method possible. 
	The Probabilistic Stage of simulation utilizes the fact that we can observe all combinations of dice rolls for a skirmish and find the probability of any roll resulting in one of our three outcomes: win, loss, or tie (from the perspective of the attacker). To do so, we simply iterate over all combinations of dice rolls, determine the outcome, sum all outcomes, and calculate the ratio of outcomes to observations. We represent the outcome probability, P_i  , as P_i=〖outcome count〗_i/(total observations). The results are as follows:
P_win=37.166%
P_lose=29.256%
P_tie=33.578%
From these percentage values, we use Random Number generation to select between three outcomes win,loss,and tie where each outcome is assigned with their Respective P_i. After the outcome is randomly generated, we apply troop change results of outcome i to attackers and defenders. This is repeated until we reach the battle size threshold to transition to Deterministic Simulation. 

μ_Attacker=0.3717(0)+0.2926(2)+0.3358(1)=0.921
μ_Defender=0.3717(2)+0.2926(0)+0.3358(1)=1.079
We finish modeling the independent distribution of a single battle by calculating variance, which is defined as the sum of outcome probabilities multiplied by the squared difference of outcome results and mean results. This is algebraically written as σ^2=∑▒〖P_i 〖(X_i-μ)〗^2 〗. Attackers and defenders have unique variance values, which when calculated result in 
σ_Attacker^2=(0.3717(0-0.921)^2 )+(0.2926(2-0.921)^2 )+(0.3358(1-0.921)^2 )=0.6580 
σ_Defender^2=(0.3717(2-1.079)^2 )+(0.2926(0-1.079)^2 )+(0.3358(1-1.079)^2 )=0.6580  
We conclude that σ_Attacker^2=σ_Defender^2=σ_Skirmish^2 so we use the same σ_i^2 for both independent distributions of attackers and defenders. 
	We know that even though these distributions are randomly sampled and independently calculated, as we aggregate many samples the distribution will take the form of a normal distribution. We define transforming the distributions of skirmishes into these normal curves as Gaussian transformations. The number of skirmishes that we will use to scale and shape the initial distribution curves we define as N. We can estimate how many skirmishes N that will take place over our battle (and, therefore, by how many skirmishes we scale the independent distribution by) by dividing the mean loss of a skirmish and the difference between our initial troop counts, and the threshold of the battle where we want to end Gaussian calculations. After estimating N for both attackers and defender we compare N_A to N_D and assigning the battle estimation N to the lower of two. Definition for N can be algebraically written as 
N=  (Troop Count-Threshold)/μ
After estimating this, we scale independent distributions in accordance with the ratios defined in the Central Limit Theorem
μ_(Attacker-Gaussian)=μ_Attacker (N)
μ_(Defender-Gaussian)=μ_Attacker (N)
σ_(Skirmish-Gaussian)=σ_Skirmish (√N)

These define the expected troop losses for attackers and defenders after N skirmishes in Battle B. From this, all BetterBlitz will do is randomly sample from these gaussian curves to generate a figure that represents total lost troops in B. BetterBlitz then will subtract total lost troops from initial troop counts and return a reduced troop count from B. This algorithm will repeat until either troop count falls below the threshold; wherein BetterBlitz will transition from Gaussian estimation to Probabilistic Estimation. 
The general Flow of a battle simulation is as follows:
Stage 1: Use gaussian estimation until either side’s troop count falls below threshold.
Stage 2: Use probabilistic simulation until either side falls below final threshold.
Stage 3: Use deterministic simulation until a terminal state is reached. 

 If the initial troop counts fall below the threshold for a given stage (ex: not enough to dictate starting in stage 1, then BetterBlitz will automatically begin the simulation in the highest applicable stage. (ex: 6v6 will automatically begin simulation in stage 3, 60v60 will begin in stage 2 and 600v600 will begin in stage 3).
This flow results in a very accurate yet computationally efficient Blitz algorithm. 
