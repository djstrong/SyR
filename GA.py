from SyR import * 
from random import random, randint, choice, uniform
import copy

class Problem:
  def __init__(self, data, arguments):
    self.data=data
    self.arguments=arguments
    
  def error1(self, exp):
    error=0.0
    for line in self.data:
      d = {}
      for n,a in enumerate(self.arguments):
	d[a]=line[n]
      error+=(exp.evaluate(d)-line[-1])**2.0
    return error**0.5


class GA(object):
    step_count = 100
    size = 100
    
    def __init__(self):
        data = [[2.0,3.0,7.0], [3.0,4.0,13.0], [0.2, 5.0, 2.0]]
        self.arguments = ['a','b']
        
        self.problem = Problem(data, self.arguments)
        self.steps = [self.makeUnique, self.select,self.reproduce,self.mutate]
        
    def calculateErrors(self, population):
	newPopulation = []
        for exp in population:
	    try:
		exp.error = self.problem.error1(exp)
	    except:
		continue
	    newPopulation.append(exp)
	return newPopulation
	
    def addUniques(self, population):
	while (len(population)<self.size):
	    exp = generateExpression()
	    if exp not in population:
		population.append(exp)
	
    def makeUnique(self, population):
	newPopulation = []
	for exp in population:
	    if exp not in newPopulation:
		newPopulation.append(exp)
	self.addUniques(newPopulation)
	return newPopulation
	
    def select(self, population):
	population = self.calculateErrors(population)
	newPopulation = sorted(population, key=lambda exp: (len(str(exp)), exp.error))[:len(population)/4]
	newPopulation.extend(sorted(population, key=lambda exp: (exp.error, len(str(exp))))[:len(population)/4])
	return newPopulation
    
    def reproduce(self, population):
	newPopulation = []
	for exp in population:
	    newPopulation.append(exp)
	    
	    exp2 = choice(population)
	    expNew = copy.deepcopy(exp)
	    nodes2 = getNodeList(exp2)
	    nodes1 = getNodeListWithoutLeafs(expNew)
	    if not nodes2 or not nodes1:
		newPopulation.append(generateExpression())
		continue # zmneijsza sie ilosc, moze losowych dolozyc?
	    node2 = choice(nodes2)
	    node1 = choice(nodes1)
	    node1.children[randint(0,len(node1.children)-1)] = copy.deepcopy(node2)
	    newPopulation.append(expNew)
	    
        return newPopulation
    
    def mutate(self,population):
	for exp in population:
	    if random()<1.0:
		if isinstance(exp, Constant):
		    exp.value += uniform(-2.0, 2.0)
		elif isinstance(exp, Argument):
		    exp.argument = choice(self.arguments)
		else:
		    #mutacja operatorw
		    pass
		#mutacja
        return population
    
    def generate_population(self):
        return [generateExpression() for i in range(self.size)]
        
    def evolve(self):
        population = self.generate_population()
        
        for i in range(self.step_count):
            for step in self.steps:
                population = step(population)
	    
	    population = self.calculateErrors(population)
            #print [exp.error for exp in population]
            
        population = self.makeUnique(population)
        population = self.calculateErrors(population)
        population = sorted(population, key=lambda exp: exp.error)
        for exp in population:
	    print exp.error, exp
	    
	#print population[0]==population[1]
	#print population[0].printf()==population[1].printf()
        
    


if __name__=="__main__":    
    data = [[2.0,3.0,6.0], [3.0,4.0,12.0]]
    arguments = ['a','b']
    problem = Problem(data, arguments)

    ga = GA()
    ga.evolve()
    #while(True):
    #  exp = generateExpression()
    #  try:
    #    error = problem.error1(exp)
    #  except:
    #    continue
    #  print error
    #  if error < 1:
    #    print exp.printf()
    #    break
