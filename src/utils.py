import numpy as np
import math as m






# Global Variables  
r = []
w = [6,6,8,7]
v = [1,2,3,2]
alpha = [1, 2.3, 0.3, 2.3]
beta = [1.5, 1.5, 1.5, 1.5]
C = 400
V = 250
W = 500










# Constraint Handling
def constraint_handling(x, number_of_variables):
    
    global r
    
    g1, g2, g3 =0,0,0
    for j in range(number_of_variables):
        g1 += ((alpha[j]*pow(10,-5))*(-1000/np.log(r[j]))**beta[j])*(x[j] + np.exp(x[j]/4))
        g2 += v[j]*(x[j])**2
        g3 += w[j]*(x[j] + m.exp(x[j]/4))
        
            
    if g1 <= C and g2 <= V and g3 <= W:
        return 1
    else:
        return 0






# Creation of the initial population
def Generate_population(population_size, number_of_variables, variable_upper_bound, variable_lower_bound):
    global r
    pseudo_list = []
    rt = np.random.uniform(0.5, 1, size = number_of_variables)
    pseudo_list.append(rt)
    population = np.zeros((population_size, number_of_variables))
    
    z, r_no, = 0,1
    
    if len(r) == 0:
        while True:
            g1, g2, g3 =0,0,0
            z += 1
            x = np.random.randint(variable_lower_bound, variable_upper_bound, size=number_of_variables)
            for j in range(number_of_variables):
                g1 += ((alpha[j]*pow(10,-5))*(-1000/m.log(rt[j]))**beta[j])*(x[j] + m.exp(x[j]/4))
                g2 += v[j]*(x[j])**2
                g3 += w[j]*(x[j] + m.exp(x[j]/4))
            
        
            
            
            if g1 <= C and g2 <= V and g3 <= W:
                r = rt
                print(f"r: {r}")
                break
            elif z > 10000:
                r_no += 1
                print(f"Changing Value of R for {r_no}th time")
                while True:
                    rt = np.random.uniform(0.5, 1, size=number_of_variables)
                    # Check if the array r is in pseudo_list
                    if not any(np.array_equal(r, arr) for arr in pseudo_list):
                        break
                pseudo_list.append(r)
                if r_no > 10000:
                    print("Unable to find a feasible solution after 20000 iterations")
                    exit(0)
                
                z = 0
            # clear_output(wait=True)
            # gc.collect()
            #print(f"Least value of G1 is = {g11}, G2 is = {g22}, G3 is = {g33}")
        
    for i in range(population_size):
        while True:
            x = np.random.randint(variable_lower_bound, variable_upper_bound, size=number_of_variables)
            value = constraint_handling(x, number_of_variables)
            if value == 1:
                break
        
        
        population[i, :] = x


    return population  # [[X1, X2, X3, ..... , Xn]]



def value_of_r():
    return r





# Function calculation of population
def Function_values(population):

    values = []
    #print(f"Value of r in Function_values_2: {r}")
    for i,x in enumerate(population):
        f1,f2 = 1,0
        for j in range(len(r)):
            
            f1 *= (1 - (1 - r[j])**x[j])
            f2 += ((alpha[j]*pow(10,-5))*(-1000/m.log(r[j]))**beta[j])*(x[j] + m.exp(x[j]/4))
            
        values.append([f1,f2])
    
    #print(values)

    return values   # [F1, F2]