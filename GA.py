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
    
data = [[2.0,3.0,6.0], [3.0,4.0,12.0]]
arguments = ['a','b']
problem = Problem(data, arguments)

while(True):
  exp = generateExpression()
  try:
    error = problem.error1(exp)
  except:
    continue
  print error
  if error<1:
    print exp.printf()
    break