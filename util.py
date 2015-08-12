# Utility / global functions for Commander/Wargame

import math
import random

def tiles(inches):
  return inches / 6.0
def inches(tiles):
  return tiles * 6

def dist_to_string(tiles):
  return '{sq}sq / {inch}"'.format(sq=tiles, inch=inches(tiles))

def coordtostring(coord):
  return "{0},{1}".format(coord[0],coord[1])

def save_to_string(save_value):
  if save_value == 7:
    return '-'
  else:
    return '{val}+'.format(val=save_value)

def constrain(n, minimum, maximum):
  if minimum > maximum:
    temp = maximum
    maximum = minimum
    minimum = temp
  if n < minimum:
    return minimum
  elif n > maximum:
    return maximum
  else:
    return n

# needs work
# takes 2 coords now
def distance(a, b):
  rowdiff = abs(a[0] - b[0])
  coldiff = abs(a[1] - b[1])
  return int(round(math.sqrt(rowdiff**2 + coldiff**2)))

def coord_sum(a, b):
  return [a[0] + b[0], a[1] + b[1]]

# TODO: more rolls, for Ld, to-hit, diff terrain, etc?
def roll(logtext='Rolling', diecount=1, goal=None, wanthigh=True):
  if diecount <= 0:
    print 'roll 0 dice? nonsense!'
    return

  total = 0
  results = []
  for die in range(diecount):
    result = random.randint(1,6)
    results.append(result)
    total += result
  # TODO: branch if more than one diecount so can say total then
  logtext += ' ... got: {n}'.format(n=results[0])
  # mention the further dice if there are more than 1:
  for i in range(len(results)-1):
    logtext += ', {n}'.format(n=results[i])

  if goal:
    logtext += '...want {g}'.format(g=goal)
    if wanthigh:
      success = total >= goal
    else:
      success = total <= goal
    if success:
      logtext += '...Success!'
    else:
      logtext += '...Failure.'
  print logtext
  return result

# TODO: refactor so doesn't require use of lambdas. Return int,bool pair? 
def roll(logtext = 'Rolling', diecount=1, successif=None):
  # diecount not yet implemented
  result = random.randint(1,6)
  logtext += ' ... got a {n}.'.format(n=result)
  if successif != None:
    if successif(result):
      logtext += ' Success!'
    else:
      logtext += ' Failed.'
  print logtext
  return result

def conjugateplural(quantity, singularword):
  if quantity == 1:
    return "1 " + singularword
  else:
    return str(quantity) + " " + singularword + "s"

# returns coord of form [0, -1] or [-1, 1], etc suggesting
# the rough direction from coords a to b.
# Only returns integer coordinates, so 9 possible return values (inc 0,0).
# used for Gamestate.act(). Kindof hacky.
def direction_from(a, b):
  diff_coord = [b[0] - a[0], b[1] - a[1]]
  # This function is sometimes called sign()
  def one_zero_minusone(x):
    if x > 0:
      return 1
    elif x == 0:
      return 0
    else:
      return -1
  return [one_zero_minusone(diff_coord[0]),
          one_zero_minusone(diff_coord[1])]

def next_letter(letter):
  return chr(ord(letter) + 1)
