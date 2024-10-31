import random as rnd
import numpy as np


from src.utils import constraint_handling







# Mutation Function
def polynomial_Mutation(population, pm=0.4, eta_m=20, lows= None, highs=None):  # Polynomial Mutation
    mutated_individual = np.copy(population)
    
    for i in range(len(population)):
        if rnd.random() < pm:
            for j in range(len(lows)):
                low = lows[j] if lows else None
                high = highs[j] if highs else None
                u = rnd.random()
                delta = min(mutated_individual[i][j] - low, high - mutated_individual[i][j])
                delta_q = (2 * u) ** (1 / (eta_m + 1)) - 1 if np.random.random() < 0.5 else 1 - (2 * (1 - u)) ** (1 / (eta_m + 1))
                mutated_individual[i][j] += delta * delta_q
                
                mutated_individual[i][j] = max(low, min(mutated_individual[i][j], high))
        
        check = constraint_handling(mutated_individual[i], len(mutated_individual[i]))
        if check != 1:
            mutated_individual[i] = population[i] # If constraint is violated, revert back to the original individual.
    
    return mutated_individual