import sys




# Function to Create a good Diversity between the solutions

def Crowding_distance_calculation(pareto_optimal_fronts):
    
    max_int = sys.maxsize
    
    distances_values = []
    
    for front in pareto_optimal_fronts: 
                                        # front contains [[F1, F2], [F1, F2], [F1, F2],... ]
        dis = []
        sorted_front = sorted(front, key=lambda l:l[0]) # Sorting the Fronts based in function F1
        
        dis.append(max_int)   # Giving the Extreme point a Maximum Value
        
        if len(sorted_front) > 1:
            for i in range(1, len(sorted_front) - 1):
                
                val = (abs(sorted_front[i+1][0] - sorted_front[i-1][0]))/(max(sorted_front[0]) - min(sorted_front[0]))
                
                dis.append(val)
            
            dis.append(max_int)   # Giving the Extreme point a Maximum Value
            
        
            sorted_front = sorted(front, key=lambda l:l[1]) # Sorting the Fronts based in function F2
                
            dis[0] = max_int
                        
            for i in range(1, len(sorted_front) - 1):
                    
                val = (abs(sorted_front[i+1][1] - sorted_front[i-1][1]))/(max(sorted_front[1]) - min(sorted_front[1]))
                    
                dis[i] += val
                
            dis[len(sorted_front)-1] = max_int
        
        distances_values.append(dis)
        
    return distances_values  # [[D1, D2, D3,..]-> Front1, [D1, D2, D3,...]-> Front2, ...]