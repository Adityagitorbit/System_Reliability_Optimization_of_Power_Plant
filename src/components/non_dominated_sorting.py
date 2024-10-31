



# Fitness calculation of the Function Values
# Finding the Pareto Optimal solutions

def Non_dominated_sorting_fitness_calculation(function_values):
    
    pareto_optimal_fronts = [] # Contains the list of final function values all the fronts
    domination = {} # Contains the index as Key and the dominates Indexes and How many are dominating
                    # {"Index of the Function Value": [["dominating index"], No of solutions dominates by]}
    front = []      # Contains fronts Indexes
    front1 = [] # Contains the Index of the Solutions of the first front
    for i, x in enumerate(function_values):
        sp = []     # Contains the list of Solutions that the current value is Dominating
        np = 0      # Contains the number of solutions that are Dominating the current solution 
        for j, y in enumerate(function_values):
            if x[0] > y[0] and x[1] < y[1]: # Since Maximization Criteria of F1 and Minimization Criteria of F2
                sp.append(j)
            elif x[0] < y[0] and x[1] > y[1]:
                np += 1
        
        domination[i] = [sp, np]
        
        if np == 0:
            front1.append(i)
    front.append(front1)
    
    
    i = 0
    while len(front[i]) > 0:
        temp = []
        for individual in front[i]:
            for other_individual in domination[individual][0]:
                domination[other_individual][1] -= 1
                if domination[other_individual][1] == 0:
                    temp.append(other_individual)
        i += 1
        front.append(temp) # Entering the Values in the Next
    
    for i  in range(len(front)):
        _ = []
        for individual in front[i]:
            _.append(function_values[individual]) # Converting Index Values to Function
        
        pareto_optimal_fronts.append(_)
    
    return pareto_optimal_fronts    # [[[F1, F2], [F1,F2],..]-> Front1, [[F1,F2], [F1,F2],....]-> Front2, ...]