from SyR import * 
from random import random, randint, choice
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
    size = 10
    
    def __init__(self):
        data = [[2.0,3.0,6.0], [3.0,4.0,12.0]]
        arguments = ['a','b']
        
        self.problem = Problem(data, arguments)
        self.steps = [self.select,self.reproduce,self.mutate]
        
    def calculateErrors(self, population):
	newPopulation = []
        for exp in population:
	    try:
		exp.error = self.problem.error1(exp)
	    except:
		continue
	    newPopulation.append(exp)
	return newPopulation
	    
    def select(self, population):
	population = self.calculateErrors(population)
	return sorted(population, key=lambda exp: exp.error)[:len(population)/2]
    
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
	    if random()<0.1:
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
            print [exp.error for exp in population]
            
        population = self.calculateErrors(population)
        for exp in sorted(population, key=lambda exp: exp.error):
	    print exp.error, exp
        
    


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
