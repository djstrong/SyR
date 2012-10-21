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
    exp.error = (error/len(self.data))**0.5
    return exp.error
    

class GA(object):
    
    def __init__(self, data, arguments):
	self.step_count = 100
	self.size = 100
        #data = [[2.0,3.0,9.0], [3.0,4.0,15.0], [0.2, 5.0, 4.0]]
        self.data = data#[ [x,x+1,x*(x+1)+x+float(x)/(x+1)] for x in range(100) ]
        
        ys = []
        for line in data:
	  ys.append(line[-1])
        self.mini = min(ys)
        self.maxi = max(ys)
        
        self.arguments = arguments # ['a','b']
        
        self.problem = Problem(data, self.arguments)
        self.steps = [self.makeUnique, self.select,self.reproduce,self.calculateErrors,self.mutate]
        self.chart = []
        
    def calculateErrors(self, population):
	newPopulation = []
        for exp in population:
	    try:
		exp.error = self.problem.error1(exp)
	    except:
		continue
	    newPopulation.append(exp)
	
	d = self.maxi - self.mini
	for exp in newPopulation:
	  exp.error = exp.error/d
	    
	return newPopulation
	
    def addUniques(self, population):
	while (len(population)<self.size):
	    exp = generateExpression(self.problem)
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
	newPopulation = sorted(population, key=lambda exp: (len(getNodeList(exp)), exp.error))[:len(population)/4]
	newPopulation.extend(sorted(population, key=lambda exp: (exp.error, len(getNodeList(exp))))[:len(population)/4])
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
		newPopulation.append(generateExpression(self.problem))
		continue # zmneijsza sie ilosc, moze losowych dolozyc?
	    node2 = choice(nodes2)
	    node1 = choice(nodes1)
	    node1.children[randint(0,len(node1.children)-1)] = copy.deepcopy(node2)
	    newPopulation.append(expNew)
	    
        return newPopulation
    
    def mutate(self,population):
	for exp in population:
	    if random()<1.0:
		node = choice(getNodeListWithRoot(exp))
		if isinstance(node, Constant):
		    ds = [0.9, 1.1, -0.9, -1.1]
		    oldValue = node.value
		    newValue = node.value
		    evaluatedOld = self.problem.error1(exp)
		    
		    for d in ds:
		      node.value = oldValue*d
		      
		      if self.problem.error1(exp)<evaluatedOld:
			newValue = oldValue*d
			evaluatedOld = self.problem.error1(exp)
		    
		    node.value = newValue
		    
		elif isinstance(node, Argument):
		    exp.argument = choice(self.arguments)
		else:
		    #mutacja operatorw
		    pass
		#mutacja
        return population
    
    def generate_population(self):
        return [generateExpression(self.problem) for i in range(self.size)]
        
    def evolve(self):
        population = self.generate_population()
        
        for i in range(self.step_count):
            for step in self.steps:
                population = step(population)
	    
	    population = self.calculateErrors(population)
            #print [exp.error for exp in population]
            self.chart.append(min([exp.error for exp in population]))
            
        population = self.makeUnique(population)
        population = self.calculateErrors(population)
        population = sorted(population, key=lambda exp: exp.error)
        self.population = population
	    
	#print population[0]==population[1]
	#print population[0].printf()==population[1].printf()
        
    


if __name__=="__main__":    
    #data = [[2.0,3.0,6.0], [3.0,4.0,12.0]]
    #arguments = ['a','b']
    #problem = Problem(data, arguments)

    data = []
    for i in range(100):
      x=uniform(-1.0,1.0)
      data.append([x, 1.57 + (24.3*x)])
      #data.append([x, x**5.0-2.0*x**3.0+x])
      #data.append([x, x**6.0-2.0*x**4.0+x**2.0])

    arguments = ['x']
    
    charts = []
    bestExpressions = []
    for i in range(1):
	ga = GA(data, arguments)
	ga.evolve()
	for exp in ga.population:
	    print exp.error, exp
	charts.append(ga.chart)
	
    charts = zip(*charts)
    f = open('data', 'w')    
    for nr, line in enumerate(charts):
	print str(nr)+"\t"+str(sum(line)/len(line))+"\t"+str(min(line))+"\t"+str(max(line))
	f.write(str(nr)+"\t"+str(sum(line)/len(line))+"\t"+str(min(line))+"\t"+str(max(line))+"\n")
    
    #while(True):
    #  exp = generateExpression(self.problem)
    #  try:
    #    error = problem.error1(exp)
    #  except:
    #    continue
    #  print error
    #  if error < 1:
    #    print exp.printf()
    #    break
