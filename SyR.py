import math

class Node:
  children=[]
  
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
    self.children.append(l)
    if r is not None:
      self.children.append(r)
      
# moze zamiast osobnych klas operacji zrobic jakiegos switcha w operation?
class OpPlus(Operation):
  operation='+'
  
  def evaluate(self, tab):
    print 'OpPlus', self.operation, self.left(), self.right()
    return self.left().evaluate(tab)+self.right().evaluate(tab)
  
class OpMultiply(Operation):
  operation='*'
  
  def evaluate(self, tab):
    print 'OpMultiply', self.operation, self.left(), self.right()
    return self.left().evaluate(tab)*self.right().evaluate(tab)
  
class OpSinus(Operation):
  operation='sin'
  
  def evaluate(self, tab):
    return math.sin(self.left().evaluate(tab))
  
  
class Argument(Node): #variable?
  argument=''
  
  def __init__(self, argument):
    self.argument=argument
    
  def evaluate(self, tab):
    print 'Argument', tab[self.argument], self.left()
    return tab[self.argument]
  
  
class Constant(Node): #Number?
  value=0.0
  
  def __init__(self, value):
    self.value=value
  
  def evaluate(self, tab):
    print 'Constant', self.value, self.left()
    return self.value
  
  
def generateExpression():
  pass

exp=OpMultiply(OpPlus(Constant(1.0),Constant(2.0)),Argument('b'))
print exp.evaluate({})
print OpPlus(Constant(1.0),Argument('b')).evaluate({})
print OpMultiply(Constant(1.0),Argument(2.0)).evaluate({})
print Argument('b').evaluate({'b':1})