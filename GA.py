from SyR import * 

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
    step_count = 1
    
    
    def __init__(self):
        data = [[2.0,3.0,6.0], [3.0,4.0,12.0]]
        arguments = ['a','b']
        
        self.problem = Problem(data, arguments)
        self.steps = [self.select,self.reproduce,self.mutate]
        
    def select(self, population):
        return population
    
    def reproduce(self, population):
        return population
    
    def mutate(self,population):
        return population
    
    def generate_population(self):
        return [generateExpression() for i in range(10)]
        
    def evolve(self):
        population = self.generate_population()
        for i in range(self.step_count):
            for step in self.steps:
                population = step(population)
            print [self.problem.error1(exp) for exp in population]
        
    


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
