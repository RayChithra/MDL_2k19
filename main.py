import random

secret_key = '2dzlVRH49dDQBOb93DgZBXGcfrtqJqPNO8lUnN6V7JKKOeTd5L'
import numpy as np
import client
pop_num = 40

def cal_pop_fitness(vector):
    # Calculating the fitness value of each solution in the current population.
    for i in range(40):
        vector[i][0]=0
        temp = list( vector[i][1:] )
        err = client.get_errors( secret_key, temp )
        total_error = err[0]+err[1]
        vector[i][0] += total_error
        print( "query number:- ", i, err )
    return vector

def crossover(parents):
    offspring = np.empty( (20, 11) )

    crossover_point = random.randrange( 1, 9 )

    for k in range( 20 ):
        # Index of the first parent to mate.
        parent1_idx = k
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # Index of the second parent to mate.
        if(parent1_idx!=19):
            parent2_idx = parent1_idx+1
        else:
            parent2_idx=0
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


def mutate(val, start, stop,lim):
    temp = val * random.uniform( start, stop )
    if (temp < lim*-1):
        return mutate( val, -10 - val, stop,lim)
    if (temp > lim):
        return mutate( val, start, 10 - val,lim)
    return temp


def mutation(offspring, parents):
    for idx in range( 20 ):
        for g in range( 0, 11):
            offspring[idx][g] = mutate( offspring[idx][g], -2.0, 2.0,10)

    for idx in range(20):
        for g in range( 0, 11 ):
            parents[idx][g] = mutate( parents[idx][g], -2.0, 2.0,10 )
    return np.append( parents, offspring, axis=0 )


def initialize_population():  # load previous population as per status
    np.savetxt( './temp.txt', np.loadtxt( "./saved_populations.txt", delimiter=',' ), delimiter=',' )
    return np.loadtxt( "./saved_populations.txt", delimiter=',' )


def vector_to_file(f,a):
    for e in a:
        f.write(str(e.tolist()))
        f.write("\n")
    f.write("\n")

def add_line(f):
    f.write("\n")

def hash(f):
    f.write("###################################################################\n")


if __name__ == "__main__":

    vector = initialize_population()

    f=open("log.txt","a")
    hash(f)
    f.write("Code Starts : " +"\n")
    f.write("Initial vector : \n")

    vector_to_file(f,vector)
    add_line(f)
    
    itern=1
    f.write("Number of Itertion : "+str(itern)+"\n")
    
    for x in range( itern ):
        vector = initialize_population()
        print( "++++++++++++++AT EPOCH :- ", x, "+++++++++++++++++" )
        f.write("++++++++++++++AT EPOCH :- "+ str(x) + "+++++++++++++++++\n" )
       
        
        
        f.write("parents : \n")
        parents = vector[:20, 1:]
        vector_to_file(f,parents)
        add_line(f)

        offspring = crossover( parents )
        f.write("Crossover : \n")
        vector_to_file(f,offspring)
        add_line(f)

        
        
        temp = mutation( offspring, parents )
        f.write("Mutation : \n")
        vector_to_file(f,temp)
        add_line(f)
        print( "New population has been created" )

        new = np.append( np.zeros( (40, 1) ), temp, axis=1 )
        print( "Starting fitness measure now" )

        new=cal_pop_fitness( new )
        print( "Fitness measured" )
        f.write("End of Itr Population : \n")

        total_population = new.copy()
        total_population = total_population[total_population[:, 0].argsort()]
        final_population = total_population[:40, :]

        vector_to_file(f,final_population)
        add_line(f)
        add_line(f)
        np.savetxt( './saved_populations.txt', final_population, delimiter=',' )


    f.write("Code Ends : " +"\n")
    hash(f)
    