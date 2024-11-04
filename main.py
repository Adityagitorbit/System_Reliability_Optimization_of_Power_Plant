import matplotlib.pyplot as plt
import math
import os
import sys
from datetime import datetime

from src.utils import Generate_population, Function_values, value_of_r
from src.components.selection import Elitism_Selection, New_generations_Elitism_Selection
from src.components.crossover import sbx_Crossover  
from src.components.mutation import polynomial_Mutation
from src.components.non_dominated_sorting import Non_dominated_sorting_fitness_calculation
from src.components.crowding_distance import Crowding_distance_calculation


from src.logger import logging
from src.exception import CustomException


# Define folder name and figure name
folder_name = 'output_figures'  # Name of the folder to save figures

# Generate a dynamic file name based on the current timestamp and iteration index
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Current time formatted as YYYYMMDD_HH_MM_SS

# Generate a dynamic name for the combined figure
figure_name = f'combined_figures_{timestamp}.png'

x_values = []
y_values = []



# Check if the folder exists, and create it if it doesn't
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

#Main Function

# Elitism Selection + SBX Cross-Over + Polynomial Mutation

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

# Number of figures to generate
num_figures = 100  # You can change this to the desired number of figures

# Calculate the grid size
rows = int(math.ceil(num_figures ** 0.5))  # Square root to form a nearly square grid
cols = int(math.ceil(num_figures / rows))   # Adjust columns based on the number of rows

# Create a figure and axis array for the grid layout
fig, axes = plt.subplots(rows, cols, figsize=(100, 100))  # Adjust figsize as needed
axes = axes.flatten()  # Flatten the axes array for easy indexing


logging.info(f"Generating Data")

try:
    for i in range(num_figures):
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
        
        # Store the values in the lists
        x_values.append(x)
        y_values.append(y)
    
    logging.info(f"All the data are Created")
    
    # Create the combined scatter plot in the grid
    for i in range(num_figures):
        axes[i].scatter(y_values[i], x_values[i])  # Plot using stored values
        axes[i].set_title(f'Scatter Plot {i + 1}')
        axes[i].set_ylabel("F1")
        axes[i].set_xlabel("F2")
        #axes[i].set_xlim(0.9, 1)  # Adjust limits based on your data
        #axes[i].set_ylim(50, 300)  # Adjust limits based on your data
        axes[i].grid()

    # Hide any unused subplots (if num_figures < rows * cols)
    for j in range(num_figures, rows * cols):
        axes[j].axis('off')
    


        
    # Adjust layout to prevent overlap and give space for the title
    plt.tight_layout(pad=4.0)  # Increase padding between subplots

    # Add a title for the entire combined figure
    fig.suptitle(f'The Value of R is :-{value_of_r()}', fontsize=20, y=1.05)  # Adjust y for title position

    
    # Add a title for the entire combined figure    
    fig.suptitle(f'The Value of R is :-{value_of_r()} ', fontsize=20)  # Adjust title and fontsize as needed
    
    
    logging.info(f"Saving all the images as one")

    # Save the combined figure in the specified folder
    plt.savefig(os.path.join(folder_name, figure_name))
    
    logging.info(f"Saved all images")
    plt.close()


except Exception as e:
    raise CustomException(e, sys)

