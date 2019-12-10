#libraries
import numpy
import copy
import csv
import sys

#functions
#creating a function that calculates fitness
def Get_Fitness (Trait):
    return abs(100 - Trait)

#creating a lexicase selection function
def Lexicase_Select (Trait_Order,Population):
    Candidates = []
    #creating a for loop that establishes the first candidate in the population as the best score
    for Trait_Id in Trait_Order:
        Best_Score = Population[0]['Trait Scores'][Trait_Id]
        Current_Best = []
        #next for loop checks to see if the next candidate has a better trait score (If trait scores are the same both get appended)
        for Pop_Id in range(len(Population)):
            Score = Population[Pop_Id]['Trait Scores'][Trait_Id]
            if Score == Best_Score:
                Current_Best.append(Pop_Id)
            elif Score < Best_Score:
                Best_Score = Score
                Current_Best = [Pop_Id]
            #setting candidates to Current best and then randomly choosing candidates if two or more are identical
        Candidates = Current_Best
    return numpy.random.choice(Candidates)

#creating a function that determines the minimum error for each trait 
def Minimum_Error(Population,Number_Of_Traits):
    Minimum_Err = [100]* Number_Of_Traits
    #next loop sets the current min to zero
    for Trait_Id in range(Number_Of_Traits):
        Current_Min = 100
        #next loop looks at a trait for everyone in the population to see if any traits are better than 100
        for Pop_Id in range(len(Population)):
            Score = Population[Pop_Id]['Trait Scores'][Trait_Id]
            if Score < Current_Min:
                Current_Min = Score
            #the minimum_err list is updated to the current min
        Minimum_Err[Trait_Id] = Current_Min

    return Minimum_Err

#creating a function that finds the average error for every single trait 
def Avg_Error(Population,Number_Of_Traits):
    Avg_Error = [0]*Number_Of_Traits
    #for loop creates a new list every cycle
    for Trait in range(Number_Of_Traits):
        Box = 0
        #this for loop adds puts a specific trait for the entire population in a list
        for Pop in range(len(Population)):
            Box += Population[Pop]['Trait Scores'][Trait]
        #this next section sums all of the traits in the list and divides that number by the size of the population
        Average_Err = Box/len(Population)
        Avg_Error[Trait] = Average_Err
    return Avg_Error

#creating a function that counts the number of individuals in the population that have a solution (Pass the win threshold)
def Sol_Count(Population, Number_Of_Traits, Threshold_Pass_Rate):
    Sol_Count = [0]*Number_Of_Traits
    #these for loops ensure that every single trait and every single person in the population is examined
    for Trait in range(Number_Of_Traits):
        for Pop in range(len(Population)):
            Candidate = Population[Pop]['Trait Scores'][Trait]
            #checking to see if any candidates meet the solution threshold for the trait being examined
            if Candidate <= 100 - Threshold_Pass_Rate:
                #adding 1 to the sol_count for every single individual that exceeds the solution threshold for a specific trait
                Sol_Count[Trait]+=1
    return Sol_Count

#creating a function that adds up all the error and divides it by the length of the population
def Avg_Err_Total(Population, Number_Of_Traits):
    #this section creates a list and a box that will store values
    Avg_Total_Err = []
    Box = 0
    #these for loops add up all of the error for every single trait for everyone in the population
    for Pop in range(len(Population)):
        for Traits in range(Number_Of_Traits):
            Box += Population[Pop]['Trait Scores'][Traits]
    #this last section takes the sum of all error and divides it by the length of the population
    Avg_Total_Err = Box/len(Population)
    return [Avg_Total_Err]

#This function will keep track of unique genomes
def Unique_Genomes(Population):
    return [len({tuple(Population[i]['Trait Scores']) for i in range(len(Population))})]

#This function will keep track of the best organism
def Best_Organism(Population, Number_Of_Traits, Target):
    Current_Min = Number_Of_Traits*Target
    for Pop in range(len(Population)):
        Box = 0
        for Traits in range(Number_Of_Traits):
            Box += Population[Pop]['Trait Scores'][Traits]
        if Box < Current_Min:
            Current_Min = Box
    return [Current_Min]

#parameters
Population_Size = 1000
Number_Of_Traits = 100
Target = 100
Number_Of_Generations = 1
Mutation_Rate = .009
Threshold_Pass_Rate = 99

#argument list
Arg_List = sys.argv
Directory = str(Arg_List[1])
Seed = int(Arg_List[2])
Population_Size = int(Arg_List[3])
Number_Of_Traits = int(Arg_List[4])
Number_Of_Generations = int(Arg_List[5])
numpy.random.seed(Seed)


#Creating a trait id that will be shuffled latter on and used to determine the order of lexicase selection
Trait_Id = [id for id in range(Number_Of_Traits)]
#Creating an empty list that will be used to hold the first generation of candidate solutions and will be updated with the offspring for every generation
Current_Population = []

print('start')

#Creating Population List
#this for loop creates empty libraries with traits and trait scores for every single candidate solution in the population
for Pop_ID in range(Population_Size):
    Candidate_Solution = {'Traits':[],'Trait Scores':[]}
    #this for loop fills all of the traits libraries with zeros and uses the the get fitness function to fill up the trait scores library for each candidate solution
    for Trait_ID in range(Number_Of_Traits):
        Trait_Val = 0
        Candidate_Solution['Traits'].append(Trait_Val)
        Candidate_Solution['Trait Scores'].append(Get_Fitness(Trait_Val))
        #After the for loop all of the candidate solutions containing libraries are appended to the empty current population list on line 87 and a message is printed signalling the end of the population creation
    Current_Population.append(Candidate_Solution)
print('Finished creating pop')

#this for loop creates all of the column names for each trait and will be used for creating csv files
Col_Names = []
for Col_Name in range(Number_Of_Traits):
    Name = 'Val-'+str(Col_Name)
    Col_Names.append(Name)


#csv writing for mininimum error
f = open(Directory+'Min_Err.csv','w')
writer1 = csv.writer(f)
Col = ['Generations']+Col_Names
writer1.writerow(Col)


#csv writing for average error
e = open(Directory+'Avg_Err.csv','w')
writer2 = csv.writer(e)
Col = ['Generations']+Col_Names
writer2.writerow(Col)


#csv writing for solution count
g = open(Directory+'Sol_Cnt.csv','w')
writer3 = csv.writer(g)
Col = ['Generations']+Col_Names
writer3.writerow(Col)

#total average error
h = open(Directory+'Tot_Avg.csv','w')
writer4 = csv.writer(h)
Col = ['Generations']+['Total Avg Err']
writer4.writerow(Col)

#Unique Genomes
i = open(Directory+'Unique_Genomes.csv','w')
writer5 = csv.writer(i)
Col = ['Generations']+['Unique Genomes']
writer5.writerow(Col)

#Best Score
j = open(Directory+'Best_Candidate.csv','w')
writer6 = csv.writer(j)
Col = ['Generations']+['Best Aggregate Fitness']
writer6.writerow(Col)



#this outer for loop represents generations 
for Generations in range(Number_Of_Generations):
    
    print('Gen=', Generations)
    
    #minimum error (This line writes a row for the minimum error csv containing all the values from the minimum error function)
    writer1.writerow([Generations] + Minimum_Error(Current_Population,Number_Of_Traits))
    
    #average error (This line writes a row for the average error csv containing all the values from the average error function)
    writer2.writerow([Generations] + Avg_Error(Current_Population,Number_Of_Traits))

    #Solution count (This line writes a row for the solution count csv containing all the values from the solution function)
    writer3.writerow([Generations] + Sol_Count(Current_Population,Number_Of_Traits,Threshold_Pass_Rate))

    #Total Average Error (This line writes a row for the total average error csv containing all the values from the total average errorfunction)
    writer4.writerow([Generations] + Avg_Err_Total(Current_Population,Number_Of_Traits))

    #Unique Genomes (This line writes a row for the Unique Genomes)
    writer5.writerow([Generations] + Unique_Genomes(Current_Population))

    #Best Candidate average Fitness
    writer6.writerow([Generations] + Best_Organism(Current_Population, Number_Of_Traits, Target))

    #offspring pop is created as an empty list and will be used to store the offspring from selected parents and will eventually be set equal to the current population list
    Offspring_Pop = []
    for Pop_Size in range(Population_Size):
        #this shuffle randomly orders the trait id which affects the order of lexicase selection
        numpy.random.shuffle(Trait_Id)
        #Selected_Organism_Id is a variable that will hold the selected organism Id from the lexicase selection function
        Selected_Organism_Id = Lexicase_Select(Trait_Id,Current_Population)
        #A deep copy of of the candidate solution with the organism Id that matches the selected Id will be coppied into the offspring list
        Offspring_Pop.append(copy.deepcopy(Current_Population[Selected_Organism_Id]))
        #Mutation
        for Mutation in range(Number_Of_Traits):
            #if a random uniform number is lower than the mutation rate, a random number on a gaussian distribution will be added/subtracted to a trait
            if numpy.random.uniform(0,1.0) <= Mutation_Rate: 
                Offspring_Pop[Pop_Size]['Traits'][Mutation] += numpy.random.normal(0.0,2.0) 
                if Offspring_Pop[Pop_Size]['Traits'][Mutation] < 0:
                    Offspring_Pop[Pop_Size]['Traits'][Mutation] = 0
                if Offspring_Pop[Pop_Size]['Traits'][Mutation] > Target:
                    Offspring_Pop[Pop_Size]['Traits'][Mutation] = Target


    #after mutation update scores
    Current_Population = Offspring_Pop
    for P in range(Population_Size):
        #these for loops look at the trait scores for each trait for every indivudal and updates them with the get fitness function
        for T in range(Number_Of_Traits):
            Current_Population[P]['Trait Scores'][T] = Get_Fitness(Current_Population[P]['Traits'][T]) 
        

#closes the csv writers
f.close()
e.close()
g.close()
h.close()
i.close()
j.close()