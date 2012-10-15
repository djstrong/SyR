import math
from random import random, choice

class Node(object):
  def __init__(self):
    self.children=[]

  def left(self):
    return self.children[0]

  def right(self):
    return self.children[1]
    
  def evaluate(self, tab):
    pass
  
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
      
# moze zamiast osobnych klas operacji zrobic jakiegos switcha w operation?
class OpPlus(Operation):
  operation='+'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)+self.right().evaluate(tab)

class OpMinus(Operation):
  operation='-'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)-self.right().evaluate(tab)
    
class OpMultiply(Operation):
  operation='*'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)*self.right().evaluate(tab)
  
#co z dzieleniem przez zero
class OpDivide(Operation):
  operation='/'
  
  def evaluate(self, tab):
    return self.left().evaluate(tab)/self.right().evaluate(tab)
  
class OpSinus(Operation):
  operation='sin'
  
  def evaluate(self, tab):
    return math.sin(self.left().evaluate(tab))
  
  def printf(self):
    return self.operation+'('+self.left().printf()+')'

  def __repr__(self):
    return self.operation+'('+self.left().printf()+')'
  
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
  
  
class Constant(Node): #Number?
  
  def __init__(self, value):
    #Node.__init__(self)
    self.value=value
  
  def evaluate(self, tab):
    return self.value

  def printf(self):
    return str(self.value)

  def __repr__(self):
    return str(self.value)
    
def generateExpression():
  ops1arg = [OpSinus]
  ops2arg = [OpPlus,OpMinus,OpMultiply,OpDivide]
  args=['a','b']
  
  p = random()
  if p<0.3:
    op = choice(ops2arg)
    left = generateExpression()
    right = generateExpression()
    return op(left, right)
  elif p<0.5:
    op = choice(ops1arg)
    left = generateExpression()
    return op(left)
  elif p<0.8:
    return Argument(choice(args))
  else:
    return Constant(random())

exp = generateExpression()
print exp
print '=', exp.evaluate({'a':1.2,'b':1})

#exp=OpMultiply(OpPlus(Constant(1.0),Constant(2.0)),Argument('b'))
#print exp.evaluate({'b':1})
#print OpPlus(Constant(1.0),Argument('b')).evaluate({'b':1})
#print OpSinus(Argument('b')).evaluate({'b':1})