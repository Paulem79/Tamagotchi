import random

malade = False

def maladie():
  if random.randint(0, 100)==0 :
    global malade
    malade = True

def guerrir():
  global malade
  malade = False