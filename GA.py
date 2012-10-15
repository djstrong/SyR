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
    print error**0.5
    
data = [[2,3,6], [3,4,12]]
arguments = ['a','b']
problem = Problem(data, arguments)
problem.error1(generateExpression())