import math
from random import random, choice, uniform

class Node(object):
  def __init__(self):
    self.children=[]

  def left(self):
    return self.children[0]

  def right(self):
    return self.children[1]
    
  def evaluate(self, tab):
    pass
  
  def evaluateProblem(self, problem):
    pass
  
  def calcError(self, problem):
    if (__debug__): print 'Error calculation'
    d = problem.d

    self.error = 0.0
    for n in xrange(len(problem.data)):
      self.error+=(self.evaluatedProblem[n]-problem.data[n][-1])**2.0
    self.error = (self.error/len(problem.data))**0.5/d
    
  
  def printf(self):
    pass
    
class Operation(Node):
  operation=''
  
  def __init__(self, l, r=None):
    Node.__init__(self)
    self.children.append(l)
    if r is not None:
      self.children.append(r)
  
  def printf(self):
    return '('+self.left().printf()+self.operation+self.right().printf()+')'

  def __repr__(self):
    return '('+self.left().printf()+self.operation+self.right().printf()+')'

  def __eq__(self,other):	
    if isinstance(other,self.__class__):
      if hasattr(self, 'children')==hasattr(other, 'children') and len(self.children)==len(other.children):	
	for nr, child in enumerate(self.children):
	  if not (child==other.children[nr]):
	    return False  
	return True
    return False
    
# moze zamiast osobnych klas operacji zrobic jakiegos switcha w operation?
class OpPlus(Operation):
  operation='+'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)+self.right().evaluate(tab)

  def evaluateProblem(self, problem):
    self.left().evaluateProblem(problem)
    self.right().evaluateProblem(problem)
    
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      self.evaluatedProblem.append(self.left().evaluatedProblem[i]+self.right().evaluatedProblem[i])

  def evaluateProblemUp(self, problem):
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      self.evaluatedProblem.append(self.left().evaluatedProblem[i]+self.right().evaluatedProblem[i])
      
    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)

class OpMinus(Operation):
  operation='-'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)-self.right().evaluate(tab)

  def evaluateProblem(self, problem):
    self.left().evaluateProblem(problem)
    self.right().evaluateProblem(problem)
    
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      self.evaluatedProblem.append(self.left().evaluatedProblem[i]-self.right().evaluatedProblem[i])
      
  def evaluateProblemUp(self, problem):
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      self.evaluatedProblem.append(self.left().evaluatedProblem[i]-self.right().evaluatedProblem[i])
      
    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)
      
class OpMultiply(Operation):
  operation='*'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)*self.right().evaluate(tab)
  
  def evaluateProblem(self, problem):
    self.left().evaluateProblem(problem)
    self.right().evaluateProblem(problem)
    
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      self.evaluatedProblem.append(self.left().evaluatedProblem[i]*self.right().evaluatedProblem[i])

  def evaluateProblemUp(self, problem):
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      self.evaluatedProblem.append(self.left().evaluatedProblem[i]*self.right().evaluatedProblem[i])

    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)
	
class OpDivide(Operation):
  operation='/'
  
  def evaluate(self, tab):
    denominator = self.right().evaluate(tab)
    if denominator==0.0:
      return 1.0
    else:
      return self.left().evaluate(tab)/denominator

  def evaluateProblem(self, problem):
    self.left().evaluateProblem(problem)
    self.right().evaluateProblem(problem)
    
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      denominator = self.right().evaluatedProblem[i]
      if denominator==0.0:
	self.evaluatedProblem.append(1.0)
      else:
	self.evaluatedProblem.append(self.left().evaluatedProblem[i]/denominator)

  def evaluateProblemUp(self, problem):
    self.evaluatedProblem = []
    for i in xrange(len(self.left().evaluatedProblem)):
      denominator = self.right().evaluatedProblem[i]
      if denominator==0.0:
	self.evaluatedProblem.append(1.0)
      else:
	self.evaluatedProblem.append(self.left().evaluatedProblem[i]/denominator)
    
    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)
    
class OpSinus(Operation):
  operation='sin'
  
  def evaluate(self, tab):
    return math.sin(self.left().evaluate(tab))
  
  def printf(self):
    return self.operation+'('+self.left().printf()+')'

  def __repr__(self):
    return self.operation+'('+self.left().printf()+')'
  
  def evaluateProblem(self, problem):
    self.left().evaluateProblem(problem)

    self.evaluatedProblem = [math.sin(val) for val in self.left().evaluatedProblem]
    
  def evaluateProblemUp(self, problem):
    self.evaluatedProblem = [math.sin(val) for val in self.left().evaluatedProblem]
    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)
  
class Argument(Node): #variable?
 
  def __init__(self, argument):
    #Node.__init__(self)
    self.argument=argument
    
  def evaluate(self, tab):
    return tab[self.argument]
    
  def printf(self):
    return self.argument

  def __repr__(self):
    return self.argument
  
  def __eq__(self,other):	
    if isinstance(other,self.__class__):
      if self.argument==other.argument:
	return True
    return False

  def evaluateProblem(self, problem):
    n = problem.arguments.index(self.argument)
    self.evaluatedProblem = [row[n] for row in problem.data]

  def evaluateProblemUp(self, problem):
    n = problem.arguments.index(self.argument)
    self.evaluatedProblem = [row[n] for row in problem.data]
    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)
    
class Constant(Node): #Number?
  
  def __init__(self, value):
    #Node.__init__(self)
    self.value=value
    self.notImprovedMutation = 1 #
  
  def evaluate(self, tab):
    return self.value

  def printf(self):
    return str(self.value)

  def __repr__(self):
    return str(self.value)

  def __eq__(self,other):	
    if isinstance(other,self.__class__):
      if self.value==other.value:
	return True
    
    return False

  def evaluateProblem(self, problem):
    self.evaluatedProblem = [self.value for i in xrange(len(problem.data))]

  def evaluateProblemUp(self, problem):
    self.evaluatedProblem = [self.value for i in xrange(len(problem.data))]
    if hasattr(self, 'parent'): self.parent.evaluateProblemUp(problem)
    else: self.calcError(problem)
    
def generateExpression(problem):    
  if (__debug__): print 'New expression generation'
  exp = generateExpression2(problem)
  exp.evaluateProblem(problem)
  exp.calcError(problem)
  return exp
  
def generateExpression2(problem):
  ops1arg = [OpSinus]
  ops2arg = [OpPlus,OpMinus,OpMultiply,OpDivide]
  args=problem.arguments
  
  p = random()
  if p<0.4:
    op = choice(ops2arg)
    left = generateExpression(problem)
    right = generateExpression(problem)
    ex = op(left, right)
    left.parent = ex
    right.parent = ex
    return ex
  elif p<0.5:
    op = choice(ops1arg)
    left = generateExpression(problem)
    ex = op(left)
    left.parent = ex
    return ex
  elif p<0.9:
    return Argument(choice(args))
  else:
    return Constant(uniform(-1.0, 1.0))
 
def getNodeListWithRoot(exp):
  nodes = [exp]
  nodes.extend(getNodeList(exp))
  return nodes
  
def getNodeList(exp):
  nodes=[]
  if hasattr(exp, 'children'):
    for child in exp.children:
      nodes.append(child)
      nodes.extend(getNodeList(child))
  return nodes
    
def getNodeListWithoutLeafs(exp):
  nodes=[]
  if hasattr(exp, 'children'):
    for child in exp.children:
      if hasattr(child, 'children'):
	nodes.append(child)
      nodes.extend(getNodeListWithoutLeafs(child))
  return nodes
    
if __name__=="__main__":
    exp = generateExpression()
    print exp
    print '=', exp.evaluate({'a':1.2,'b':1})
#exp=OpMultiply(OpPlus(Constant(1.0),Constant(2.0)),Argument('b'))
#print exp.evaluate({'b':1})
#print OpPlus(Constant(1.0),Argument('b')).evaluate({'b':1})
#print OpSinus(Argument('b')).evaluate({'b':1})