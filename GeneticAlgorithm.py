import random

class SimpleGeneticAlgorithm:
    generation_count=0
    tournament_size=5
    uniform_rate=0.5
    mutation_rate=0.015
    elitism=True
    elitism_offset=0

    def __init__(self, target_solution, population_size):
        self.solution=target_solution
        self.population_size=population_size

    def run_algorithm(self):
        my_pop=Population(self.population_size, self.solution, initialize=True)
        
        while my_pop.get_fittest().get_fitness() < len(self.solution):
            print(f"Generation: {SimpleGeneticAlgorithm.generation_count} Correct genes found: {my_pop.get_fittest().get_fitness()} Genes: {my_pop.get_fittest()}")

            my_pop=self.evolve_population(my_pop)
            SimpleGeneticAlgorithm.generation_count+=1

        print("Solution found!")
        print(f"Generation: {SimpleGeneticAlgorithm.generation_count}")
        print(f"Genes: {my_pop.get_fittest()}")

    def evolve_population(self, pop):
        new_population = Population(pop.size(), self.solution, initialize=False)
        
        SimpleGeneticAlgorithm.elitism_offset= 1 if SimpleGeneticAlgorithm.elitism else 0

        if SimpleGeneticAlgorithm.elitism:
            new_population.individuals.append(pop.get_fittest().clone())

        for _ in range(SimpleGeneticAlgorithm.elitism_offset, pop.size()):
            indiv1 = self.tournament_selection(pop)
            indiv2 = self.tournament_selection(pop)
            new_indiv=self.crossover(indiv1, indiv2)
            new_population.individuals.append(new_indiv)

        for i in range(SimpleGeneticAlgorithm.elitism_offset, len(new_population.individuals)):
            self.mutate(new_population.individuals[i])
        
        return new_population

    def tournament_selection(self, pop):
        tournament = Population(SimpleGeneticAlgorithm.tournament_size, self.solution, initialize=False)
        random_gen=random.Random()

        for _ in range(SimpleGeneticAlgorithm.tournament_size):
            random_id=random_gen.randint(0, pop.size()-1)
            tournament.individuals.append(pop.get_individual(random_id))

        return tournament.get_fittest()
    
    def crossover(self, indiv1, indiv2):
        new_sol=Individual(self.solution)
        random_gen=random.Random()

        for i in range(new_sol.default_gene_length()):
            if random_gen.random()<SimpleGeneticAlgorithm.uniform_rate:
                new_sol.set_single_gene(i, indiv1.get_single_gene(i))
            else:
                new_sol.set_single_gene(i, indiv2.get_single_gene(i))

        return new_sol
    
    def mutate(self, indiv):
        random_gen=random.Random()

        for i in range(indiv.default_gene_length()):
            if random_gen.random()<=SimpleGeneticAlgorithm.mutation_rate:
                gene=1-indiv.get_single_gene(i) #flip the bit
                indiv.set_single_gene(i, gene)



class Population:
    def __init__(self, population_size, target_solution, initialize=True):

        self.individuals=[]
        self.solution=target_solution

        if initialize:
            for _ in range(population_size):
                self.individuals.append(Individual(self.solution))
        
    def size(self):
        return len(self.individuals)
        
    def get_individuals(self):
        return self.individuals
        
    def get_individual(self,index):
        return self.individuals[index]
        
    def get_fittest(self):
        return max(self.individuals, key=lambda ind: ind.get_fitness())

        
       
class Individual:
    def __init__(self, target_solution):
        self.solution=target_solution
        self.genes=[random.randint(0,1) for _ in range(len(self.solution))]
        self.fitness=0

    def get_single_gene(self, index):
        return self.genes[index]

    def set_single_gene(self, index, value):
        self.genes[index]=value
        self.fitness=0

    def default_gene_length(self):
        return len(self.genes)
    
    def get_fitness(self):
        if self.fitness==0:
            self.fitness=sum(1 for i in range(len(self.genes)) if self.genes[i]==int(self.solution[i]))
        
        return self.fitness

    def __str__(self):
        return "".join(str(gene) for gene in self.genes)
    
    def clone(self):
        clone=Individual(self.solution)
        clone.genes=list(self.genes)
        clone.fitness=self.fitness
        return clone
    

if __name__=="__main__":
    population_size=50
    solution="1011000100000100010000100000100111001000000100000100000000001111"
    ga=SimpleGeneticAlgorithm(solution, population_size)
    ga.run_algorithm()
    
        
            

        

           
            

            
       