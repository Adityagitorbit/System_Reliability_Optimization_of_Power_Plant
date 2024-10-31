from src.utils import Function_values
from src.components.non_dominated_sorting import Non_dominated_sorting_fitness_calculation
from src.components.crowding_distance import Crowding_distance_calculation




def Elitism_Selection(function_values, pareto_optimal_fronts, distance_values, population_size, population):
    # Initialize lists for holding selected individuals
    selected_list = []  # ["Function_value_index", "pareto_optimal_front_number", "crowding_distance_value"]
    final_selected_list = []  # ["Population Values"] that is the new population after calculation and selection 

    # Create a list of tuples (function_value_index, pareto_optimal_front_number, crowding_distance_value)
    for i, x in enumerate(function_values):
        _ = [] # ["Function_value_Index", "Pareto_optimal_Front_Position", "crowding_distance_value"]
        for j, y in enumerate(pareto_optimal_fronts):
            for k, z in enumerate(y):
                if x == z:
                    _.append(i)
                    _.append(j)
                    _.append(distance_values[j][k])

        selected_list.append(_)
    # Sort the selected list first by Pareto front number (ascending), then by crowding distance (descending)
    selected_list.sort(key=lambda x: (x[1], -x[2]))

    # # Select the top `population_size` individuals
    for i in range(population_size):
        population_value = population[selected_list[i][0]]
        final_selected_list.append(population_value)  # the final population values that is of X1, x2. ..
        
    
    # Select the top `population_size` individuals
    # for i in range(population_size//2):
    #     population_value = population[selected_list[i][0]]
    #     for j in range(2):
    #         final_selected_list.append(population_value)  # the final population values that is of X1, x2. ..

    return final_selected_list  # [[X1,X2,..], [X1,X2,..], [X1,X2,..],..]



# Function to generate the new Generation of better solutions
def New_generations_Elitism_Selection(Parent_population, Offspring_population):
    
    combination_of_generations = [] # List containing the combination of both parent and child population
    next_generation_values = [] # List containing the values of the next/new generations
    
    
    for i in range(len(Parent_population)):
        combination_of_generations.append(Parent_population[i])
        combination_of_generations.append(Offspring_population[i])
    
    # List containing the function values
    function_values = Function_values(combination_of_generations)
    # list containing pareto optimal fronts
    pareto_optimal_front_values = Non_dominated_sorting_fitness_calculation(function_values)
    # List containing the Crowding distance
    crowding_distance_calculation_values = Crowding_distance_calculation(pareto_optimal_front_values)
    # List containing the final selected values
    final_selected_values = Elitism_Selection(function_values, pareto_optimal_front_values, crowding_distance_calculation_values, 
                                                len(combination_of_generations), combination_of_generations)
    
    for i in range(len(Parent_population)):
        next_generation_values.append(final_selected_values[i])
    
    return next_generation_values