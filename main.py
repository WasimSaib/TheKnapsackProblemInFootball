import random
from player import Player
import matplotlib.pyplot as plt
import pandas as pd
from bitarray import bitarray
from formation import Formation
from datetime import datetime

population_size = 100
gen_size = 200
mutation_rate = 0.3
budget = 1000000.0
lu = Formation(4,4,1,1)
# player object array
playa = []
# index
idx = 0
# position index
POS = ["GK","LB","CB","RB","RWB","CDM","LWB","CM","CAM","RW","LW", "LM","RM", "ST"]

# write players from CSV to objects
def players_to_object(pos):
     global idx
     dF = pd.read_csv(f"data/players/{pos}.csv")
     first_val = idx
     for index, row in dF.iterrows():
        a = Player(row['short_name'],idx, row['overall'], row['value_eur'], pos)
        playa.append(a)
        idx += 1
    #  print(f'{pos} obj created')

for i in range(len(POS)):
    players_to_object(POS[i])

PosRange = {'GK': (0,2124), 'LB': (2124,3482), 'CB': (3482,6803), 'RB': (6803,8141), 'RWB': (8141,8319), 'CDM': (8319,9977), 'LWB': (9977,10148), 'CM': (10148,12317), 'CAM': (12317,13461), 'RW': (13461,13956), 'LW': (13956,14386), 'LM': (14386,15398), 'RM': (15398,16424), 'ST': (16424,19023)}


def get_cost(chromosome:bitarray):  
    # Get total cost of team, so the weight
    weight = 0.0
    global idx
    c = idx+1
    for i in range(0,c):
        if i < len(chromosome) and chromosome[i] == 1:
            weight += playa[i]._value
         
    return weight

def check_valid_solution(chromosome:bitarray, formation: Formation):
    if len(chromosome) > 19024:
        return False

    # if there are more than eleven players
    if chromosome.count(1) == 11:
        return True
    else:
        return False

def valid_positional_counts(chromosome:bitarray, formation: Formation):
    global PosRange
    for Key in PosRange:
         lst = chromosome[PosRange[Key][0]:PosRange[Key][1]]
         if lst.count(1) < formation.PosDict[Key] or lst.count(1) > formation.PosDict[Key]:
             return False
         
    return True
def create_team(f:Formation):
    global PosRange
    # global idx
    ba = bitarray(19024) #to accomodate for 19024 players
    ba.setall(0) # initialize all to zero
    # Loop through  the positions
    for Key in PosRange:        
        a = f.PosDict[Key]
        c = 0 #counter var
        while c < a:
            random_player = random.randint(PosRange[Key][0], PosRange[Key][1]-1)
            if ba[random_player] == 0:
                 ba[random_player] ^= 1 #flip the bit to one to signify selection of that player
                 c+=1
            else:
                continue # if space already has 1 repeat loop        
    return ba          

def initial_population(p_size):
    global lu
    pop = []
    i = 0
    while i < p_size:
        t = create_team(lu)
        if check_valid_solution(t, lu) is True:
            if len(pop) == 0:
                pop.append(t)
                i+=1 
            else:
                pop.append(t)
                i+=1        
        else:
            continue
    return pop
    

# this calculates our team value
def fitness(chromosome:bitarray):
    global playa
    global budget
    global lu
    team_overall = 0.0
    team_val = get_cost(chromosome)
    
    for index, bit in enumerate(chromosome):
        if bit == 1:
            team_overall += playa[index]._overall
    #Ensure budget constraint
    if team_val > budget:
        return 1
    
    # Ensure positional constraint
    if valid_positional_counts(chromosome,lu) is False:
        return 0.5
    
    w = team_overall / 11
    
    return w 
            

def tournament_selection(pop):
    p1, p2 =random.sample(range(0,len(pop)-1), 2)
    # p2=random.randint(0,len(pop)-1)
    if fitness(pop[p1]) > fitness(pop[p2]):
        winner = pop[p1]
    else:
        winner = pop[p2]
    return winner
def roulette_selection(pop):
    # proportional selection: individual fitness: sum of population fitness
    # sum of all fitness in pop
    population_fitness = 0
    i = 0 # let i = 0
    for c in range(len(pop)):
        population_fitness += fitness(pop[c]) #calc sum of all fitness in population
    
    propotional_selection = fitness(pop[i])/ population_fitness
    ans = propotional_selection 

    r = random.uniform(0.0,1.0) # choose r ~ U(0,1)
    while ans < r:
        i += 1
        ans += fitness(pop[i])/ population_fitness
        
    return pop[i]
def crossover(p1:bitarray, p2:bitarray):
    global lu
    #generate a random point
    point = random.randint(0, random.randint(0,len(p1) - 1))
    
    # offspring 1
    part_one1 = p1[:point]
    part_two1 = p2[point:]
    # for offspring 2
    part_one2 = p2[:point]
    part_two2 = p1[point:]
    
    c1 = part_one1 + part_two1
    c2 = part_one2 + part_two2
   
    a = check_valid_solution(c1, lu)
    b = check_valid_solution(c2, lu)
    
    if a and b:
            if fitness(c1) > fitness(c2):
                return c1
            else:
                return c2
    else:
        return crossover(p1, p2)

def two_point_crossover(p1:bitarray, p2:bitarray):
    global lu 
    pt1, pt2 =  random.sample(range(0, len(p1)), 2)
    #assert pt1 < pt2 
    pt1_1 = p1[:pt1]
    seg_1 = p2[pt1:pt2] 
    pt1_2 = p1[pt2:] 
    
    pt2_1 = p2[:pt1]
    seg_2 = p1[pt1:pt2] 
    pt2_2 = p2[pt2:] 
    
    c1 = pt1_1 + seg_1 + pt1_2
    c2 = pt2_1 + seg_2 + pt2_2
    
    a = check_valid_solution(c1, lu)
    b = check_valid_solution(c2, lu)
    
    if a and b:
            if fitness(c1) > fitness(c2):
                return c1
            else:
                return c2
    else:
        return two_point_crossover(p1, p2) 

def get_pos_from_index(index)->str:
    global PosRange
    for key in PosRange:
        if PosRange[key][0] <= index < PosRange[key][1]:
            return key    
# Returns list of indexes that are already selected
def getPlayersFromPosition(index:int, ba: bitarray):
    global PosRange
    key = get_pos_from_index(index)
    lst = [] 
    for index, bit in enumerate(ba):
    
        if PosRange[key][0] <= index < PosRange[key][1]:
            if bit == 1:
                lst.append(index)
    return lst


def mutation(ch:bitarray, f:Formation):
    global idx 
    temp = ch
    point = random.randint(0, idx)
    pos =  get_pos_from_index(point) # get the position based on index

    lst = getPlayersFromPosition(point,temp)

    if temp[point] == 0: #if not selected
        # to ensure we fit the positional constraint
        if len(lst) == 1:
            temp[lst[0]] ^= 1 #flip the bit to zero, remove the one 
            temp[point] ^= 1 #flip bit to one
        elif len(lst) == 2:
            p1 = random.randint(0,1)
            temp[lst[p1]] ^= 1 #flip that to 0
            temp[point] ^= 1 #flip this to one
    elif temp[point] == 1:
        #Case: Lose the one, Add the one
        a = f.PosDict[pos]
        b = a - 1  
        temp[point] ^= 1 #Becomes 0
        while b < a:
            #randomise a value where we are going to add
            p2 = random.randint(PosRange[pos][0], PosRange[pos][1]-1)
            if temp[p2] == 1:
                continue #if our randomised point is one then ignore and go to next iteration of loop
            else:
                temp[p2] ^= 1  #if its 0, flip to 1
                b +=1 
                
    if check_valid_solution(temp, f) is True:
        return temp #ret mutated child
    else:
        return mutation(ch, f) #mutate again
 
def best_team(pop):
    best = best_solution(pop)
    index = findByIndex(best, pop)
    team = pop[index]
    global playa
    for i in range(len(team)):
        if team[i] == 1:
            print(f'{playa[i]._pos}: {playa[i]._name}   {playa[i]._overall} \n') 
    print(f'Budget: {get_cost(team)}')
def findByIndex(value, pop) -> int:
    # index=0
    for i in range(len(pop)):
        if i < len(pop) and fitness(pop[i]) == value:
            index = i

    return index    
def elitism(pop, mut_rate):
    # find the fittest solution and exclude it
        best= best_solution(pop)
        index = findByIndex(best, pop)

        next_gen = []
        next_gen.append(pop[index])
        # print('best added')
        # remove best from current list
        remove_best = pop.pop(index)
        c = 0 #counter
        while c < len(pop):
            #select parents using tournament selection
            # p1 = tournament_selection(pop)
            # p2 = tournament_selection(pop)
            p1 = roulette_selection(pop)
            p2 = roulette_selection(pop)

            # child = crossover(p1, p2)            
            child = two_point_crossover(p1, p2)
            
            
            if random.random() < mut_rate:
                child = mutation(child,lu)
            next_gen.append(child)
            c+=1
        return next_gen
def create_generation(pop, mutation_rate):
    next_gen = []
    global lu
    i = 0 
        
    for i in range(0, len(pop)):
        p1 = roulette_selection(pop) 
        p2 = roulette_selection(pop)
        # p1= tournament_selection(pop) 
        # p2 = tournament_selection(pop)
        
        # child = crossover(p1, p2)
        child = two_point_crossover(p1,p2)        

        if random.random() < mutation_rate:
            child = mutation(child,lu)
        
        next_gen.append(child)
        
    # print('created gen')
    return next_gen

def best_solution(pop):
    best = 0
    for i in range(0, len(pop)):
        temp = fitness(pop[i])
        if temp > best:
            best = temp
    return best
    
solutions_best = []

def GA(p_size, g_size, mut_rate):
    print('lets go')
    print('initialize population')
    t1 = datetime.now()
    pop = initial_population(p_size)
    t2 = datetime.now()
    print(f'population initialized in {t2-t1}')

    t3 = datetime.now()
    for i in range(0, g_size):
         #pop = create_generation(pop, mut_rate)
         pop = elitism(pop, mut_rate)
         solutions_best.append(best_solution(pop))
         print(f'Generation {i} --> best solution: {best_solution(pop)}')
        
    t4 = datetime.now()
    print(f'time taken: {t4-t3}')
    return pop, solutions_best
    
latest_pop, solutions_best = GA(population_size, gen_size , mutation_rate)



print(best_solution(latest_pop))
best_team(latest_pop)

plt.plot(solutions_best)
plt.xlabel('generations')
plt.ylabel('Team Averages over Generations')
plt.title("The best solutions over the generations")
plt.show()  