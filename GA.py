from SyR import * 
from random import random, randint, choice, uniform
import copy
from multiprocessing import Process, Queue
from multiprocessing import Pool
import pickle


class Problem:
  def __init__(self, data, arguments):
    self.data=data
    self.arguments=arguments
    ys = []
    for line in data:
      ys.append(line[-1])
    self.mini = min(ys)
    self.maxi = max(ys)
        
  def error1(self, exp):
    error=0.0
    for line in self.data:
      d = {}
      for n,a in enumerate(self.arguments):
	d[a]=line[n]
      error+=(exp.evaluate(d)-line[-1])**2.0
    exp.error = (error/len(self.data))**0.5
    return exp.error
    

def forPool(arg):
    problem, x = arg
    x.error = problem.error1(x)
    #print 'err', x.error
    return x.error

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
        self.steps = [self.select,self.reproduce,self.calculateErrors,self.mutate]
        self.chart = []

	#self.pool = Pool(processes=4)

    def calculateErrors(self, population):
	return population
	d = self.maxi - self.mini
        for exp in population:
	  #exp.evaluateProblem(self.problem)
	  exp.error = 0.0
	  for n in xrange(len(self.problem.data)):
	    exp.error+=(exp.evaluatedProblem[n]-self.problem.data[n][-1])**2.0
	  exp.error = (exp.error/len(self.problem.data))**0.5/d
	  
	return population
       
    def calculateErrors22(self, population):
        for exp in population:
	  exp.evaluateProblem(self.problem)
        
        results =  self.pool.map(forPool, [(self.problem, exp) for exp in population], 5)
        
	for n, exp in enumerate(population):
	    exp.error = results[n]
 
 	d = self.maxi - self.mini
	for exp in population:
	  exp.error = exp.error/d
	  
	return population
 
 
    def calculateErrors2(self, population):
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
	#newPopulation = sorted(population, key=lambda exp: (len(getNodeList(exp)), exp.error))[:len(population)/8]
	newPopulation = sorted(population, key=lambda exp: (exp.error, len(getNodeList(exp))))[:len(population)/2]
	return newPopulation
    
    def reproduce(self, population):
	newPopulation = list(population)
	while len(newPopulation)<self.size:
	  for exp in population:
	      if len(newPopulation)>=self.size: break
	      if (__debug__): print 'Reproduction'
	      #newPopulation.append(exp)
	      
	      exp2 = choice(population)
	      nodes2 = getNodeList(exp2)
	      if not nodes2: continue
	      
	      expNew = copy.deepcopy(exp)
	      nodes1 = getNodeListWithoutLeafs(expNew)

	      if not nodes1:
		  #newPopulation.append(generateExpression(self.problem))
		  continue # zmneijsza sie ilosc, moze losowych dolozyc?
	      node2 = choice(nodes2)
	      node1 = choice(nodes1)
	      
	      ran = randint(0,len(node1.children)-1)
	      node1.children[ran] = copy.deepcopy(node2)
	      node1.children[ran].parent = node1
	      node1.evaluateProblemUp(self.problem)
	      newPopulation.append(expNew)
	      
	    
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
            #population = sorted(population, key=lambda exp: (exp.error, len(getNodeList(exp))))
            #print [exp.error for exp in population]
            #print min([exp.error for exp in population])
            #print sorted(population, key=lambda exp: (exp.error, len(getNodeList(exp))))[:10]
            mini = min([exp.error for exp in population])
            print 'Iteration:', i, '\tPopulation:', len(population), '\tBest:', mini
            self.chart.append(mini)
            
        population = self.makeUnique(population)
        population = self.calculateErrors(population)
        population = sorted(population, key=lambda exp: exp.error)
        self.population = population
	    
	#print population[0]==population[1]
	#print population[0].printf()==population[1].printf()
        
    
def f(data, arguments, q, nr):
  ga = GA(data, arguments)
  ga.evolve()
  print 'nr = ', i
  for exp in ga.population:
      print exp.error, exp
  #charts.append(ga.chart)
  q.put(ga.chart)

if __name__=="__main__":    
    #data = [[2.0,3.0,6.0], [3.0,4.0,12.0]]
    #arguments = ['a','b']
    #problem = Problem(data, arguments)


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
    
    runs = 1
    ps = []
#    q = Queue()
#    for i in range(runs):
#      p = Process(target=f, args=(data, arguments, q, i, ))
#      ps.append(p)
#      p.start()
    
#    for p in ps:
#      p.join()
      
#    for i in range(runs):
#      charts.append(q.get())
    
    for i in range(1):
	ga = GA(data, arguments)
	ga.evolve()
#	for exp in ga.population:
#	    print exp.error, exp
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
