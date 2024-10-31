import matplotlib.pyplot as plt

from src.utils import Generate_population, Function_values
from src.components.selection import Elitism_Selection, New_generations_Elitism_Selection
from src.components.crossover import sbx_Crossover  
from src.components.mutation import polynomial_Mutation
from src.components.non_dominated_sorting import Non_dominated_sorting_fitness_calculation
from src.components.crowding_distance import Crowding_distance_calculation

#Main Function

# Binary Tournament Selection + SBX Cross-Over + Polynomial Mutation

population_size = 1000
number_of_variables = 4
variable_upper_bound = [] 
variable_lower_bound = []
for i in range(number_of_variables):
    variable_upper_bound.append(10)
    variable_lower_bound.append(1)
    
# print(variable_lower_bound)
# print(variable_upper_bound)

threshold = population_size*0.8

print(f'Threshold = {threshold}')

population = Generate_population(population_size, number_of_variables, variable_upper_bound, variable_lower_bound)

for i in range(100):
    print(f"GENERATION :- {i+1}")
    counter = 0
    first_counter = 0
    function_values = Function_values(population)
    ##print(function_values)
    
    first_value = function_values[0] # Get the first element of the first sublist
    first_f1_point = first_value[0]
    
    for sublist in function_values:
        if sublist == first_value:
                first_counter += 1
        for value in sublist:
            if value == first_f1_point:
                counter += 1 # Found different value
    
    if counter >= threshold or first_counter >= threshold:
        print(f"Convergence reached after {i+1} generations as there are {threshold} same values")
        break
    
    pareto_optimal_front_values = Non_dominated_sorting_fitness_calculation(function_values)
    #print(pareto_optimal_front_values)
    crowding_distance_calculation_values = Crowding_distance_calculation(pareto_optimal_front_values)
    #print(crowding_distance_calculation_values)
    final_selected_values = Elitism_Selection(function_values, pareto_optimal_front_values, crowding_distance_calculation_values, 
                                                population_size, population)
    population = final_selected_values
    offspring_population = sbx_Crossover(population, lows=variable_lower_bound, highs=variable_upper_bound)
    offspring_population = polynomial_Mutation(offspring_population,  lows=variable_lower_bound, highs=variable_upper_bound)
    population = New_generations_Elitism_Selection(population, offspring_population)
    #print(population)
    x = []
    y = []
    for i in function_values:
        x.append(i[0])
        y.append(i[1])
    #plt.figure(figsize=(8, 6))
    #plt.xlim(50, 300)  # Limit x-axis from 0 to 6
    #plt.ylim(0.9, 0.99)  # Limit y-axis from 0 to 6

    plt.scatter(y,x)
    plt.ylabel("F1")
    plt.xlabel("F2")
    plt.grid()
    plt.show()