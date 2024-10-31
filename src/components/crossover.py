import random as rnd
import numpy as np


from src.utils import constraint_handling







# Cross - Over Function

def sbx_Crossover(population, eta_c=10, lows=None, highs=None): # Using SBX cross-over method
    
    offspring = []
    
    for i in range(0,len(population)):
        
        parent1 = population[i]
        
        if i+1 > len(population)-1:
            parent2 = population[0]
        else:
            parent2 = population[i+1]
        
        child1 = np.zeros_like(parent1)
        child2 = np.zeros_like(parent2)
        
        
        for j in range(len(parent1)):
            low = lows[j]
            high = highs[j]
            u = rnd.random()
            if u <= 0.5:
                beta = (2 * u) ** (1 / (eta_c + 1))
            else:
                beta = (1 / (2 * (1 - u))) ** (1 / (eta_c + 1))
            
            child1[j] = 0.5 * (((1 + beta) * parent1[j]) + ((1 - beta) * parent2[j]))
            child2[j] = 0.5 * (((1 - beta) * parent1[j]) + ((1 + beta) * parent2[j]))
            
            child1[j] = max(low, min(child1[j], high))
            child2[j] = max(low, min(child2[j], high))
        
        check = constraint_handling(child1, len(parent1))
        if check != 1:
            child1 = parent1
        
        check = constraint_handling(child2, len(parent2))
        if check != 1:
            child2 = parent2
        
        offspring.append(child1)
        offspring.append(child2)
        
        i += 2
    
    return offspring