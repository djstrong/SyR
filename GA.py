from SyR import * 
from random import random, randint, choice, uniform, seed, shuffle
import copy
import pickle
import time
try:
  from multiprocessing import Process, Queue, Pool
  MULTIPROCESSING = True
except ImportError:
  MULTIPROCESSING = False

class Problem:
  def __init__(self, data, arguments):
    self.data=data
    self.arguments=arguments
    
    # for error calculation
    ys = []
    for line in data:
      ys.append(line[-1])
    self.d = max(ys) - min(ys)
        
def reproduction(arg):
    exp, exp2, problem = arg
    nodes2 = getNodeList(exp2)
    seed(len(nodes2))
    
    expNew = copy.deepcopy(exp)
    nodes1 = getNodeListWithoutLeafs(expNew)

    node2 = choice(nodes2)
    node1 = choice(nodes1)
    
    ran = randint(0,len(node1.children)-1)
    node1.children[ran] = copy.deepcopy(node2)
    node1.children[ran].parent = node1
    node1.evaluateProblemUp(problem)
    return expNew

class GA(object):
    
    def __init__(self, data, arguments):
	self.step_count = 100
	self.size = 100

        self.data = data
        self.arguments = arguments
        
        self.problem = Problem(data, self.arguments)
        self.steps = [self.select,self.reproduce,self.mutate]
        self.chart = []

	if MULTIPROCESSING: self.pool = Pool(processes=8)
       
    def select(self, population):
	#newPopulation = sorted(population, key=lambda exp: (len(getNodeList(exp)), exp.error))[:len(population)/8]
	newPopulation = sorted(population, key=lambda exp: (exp.error, len(getNodeList(exp))))[:len(population)/2]
	return newPopulation
    
    def reproduce(self, population):
	newPopulation = list(population)

	population1 = filter(lambda x: getNodeListWithoutLeafs(x), population)
	population2 = filter(lambda x: getNodeList(x), population)
	
	pairs = []
	for i in xrange(self.size - len(newPopulation)):
	  pairs.append( (choice(population1), choice(population2), self.problem) )

	if MULTIPROCESSING: results =  self.pool.map(reproduction, pairs)
        else: results =  map(reproduction, pairs)
        
	newPopulation.extend(results)
	return newPopulation
    
    def mutate(self,population):
	for exp in population:
	    if random()<1.0:
		node = choice(getNodeListWithRoot(exp))
		if isinstance(node, Constant):
		    if (__debug__): print 'Constant mutation'
		    es = [0.1, -0.1, 0.01, -0.01]
		    ds = [1.0, -1.0]
		    oldValue = node.value
		    newValue = node.value
		    evaluatedOld = exp.error
		    
		    for e in es:
		      for d in ds:
			node.value = oldValue*(d+e/node.notImprovedMutation)
			node.evaluateProblemUp(self.problem)
			
			if exp.error<evaluatedOld:
			  newValue = oldValue*(d+e/node.notImprovedMutation)
			  evaluatedOld = exp.error
		    
		    node.value = newValue

		    #if oldValue==newValue:
		    #  node.notImprovedMutation += 1 # przy kazdej zmianie wyrazenia trzeba by chyba "zerowac"?
		    node.evaluateProblemUp(self.problem)
		    
		elif isinstance(node, Argument):
		    if (__debug__): print 'Argument mutation'
		    #psuje najlepsze
		    #node.argument = choice(self.arguments)
		    #node.evaluateProblemUp(self.problem)
		else:
		    #mutacja operatorw
		    pass
        return population
    
    def generate_population(self):
        return [generateExpression(self.problem) for i in range(self.size)]
        
    def evolve(self):
        population = self.generate_population()
        
        for i in range(self.step_count):
            for step in self.steps:
                population = step(population)

            mini = min([exp.error for exp in population])
            print 'Iteration:', i, '\tPopulation:', len(population), '\tBest:', mini
            self.chart.append(mini)
            

        population = sorted(population, key=lambda exp: exp.error)
        self.population = population
        
    
def runGA(data, arguments, q, nr):
  ga = GA(data, arguments)
  ga.evolve()
  print 'nr = ', i
  for exp in ga.population:
      print exp.error, exp
  q.put(ga.chart)

if __name__=="__main__":    
    time = time.time()
    print 'Seed:', time
    seed(time)
    seed(0)
    
    data = []
    for i in range(100):
      x=uniform(-1.0,1.0)
      y=uniform(-1.0,1.0)
      z=uniform(-1.0,1.0)
      #ACCURACY IN SYMBOLIC REGRESSION
      #data.append([x, 1.57 + (24.3*x)]) #P1
      #data.append([x, 0.23 + (14.2*((y+x)/(3.0*z)))]) #P2
      #data.append([x, -2.3 + (0.13*math.sin(x))]) #P4
      
      #Improving Symbolic Regression with Interval Arithmetic and Linear Scaling
      #data.append([x, 0.3*x*math.sin(2.0*x)]) #(4)
      #data.append([x, y, 8.0/(2.0 + x**2 + y**2) ]) #(15)
      data.append([x, y, (x*x + y*y) ]) #(15)

      #data.append([x, x**5.0-2.0*x**3.0+x])
      #data.append([x, x**6.0-2.0*x**4.0+x**2.0])

    arguments = ['x','y']
    
    charts = []
    bestExpressions = []

    if MULTIPROCESSING:
      runs = 1
      ps = []
      q = Queue()
      for i in range(runs):
	p = Process(target=runGA, args=(data, arguments, q, i, ))
	ps.append(p)
	p.start()
      
      for p in ps:
	p.join()
	
      for i in range(runs):
	charts.append(q.get())
    else: # no MULTIPROCESSING
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
