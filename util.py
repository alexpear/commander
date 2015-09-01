# Utility / global functions for Commander/Wargame

import math
import random

# TODO standardize underscore_style to camelCaseStyle across this repo
# TODO put TODOs from notes.txt into a committed file

DEFAULT_HEIGHT = 8
DEFAULT_WIDTH = 12

def tiles(inches):
  return inches / 6.0
def inches(tiles):
  return tiles * 6

def dist_to_string(tiles):
  return '{sq}sq / {inch}"'.format(sq=tiles, inch=inches(tiles))

# TODO: Make class Coord. fields like .r and .c, etc.
def coordtostring(coord):
  return "{0},{1}".format(coord[0],coord[1])

# if coord is correctly formatted (eg '4,8' with no spaces) return as [4,8]
# else return None
def parsecoord(coordstring):
  # We allow either the 0th or 1st char to be digit,
  # because 0th char might be a '-' for a negative number
  if (type(coordstring) == 'str' and
      coordstring.find(',') != -1 and
      (coordstring[0].isdigit() or coordstring[1].isdigit()) and
      coordstring[-1].isdigit()):
    halves = coordstring.strip().split(',')
    coord = [int(halves[0]), int(halves[1])]
    return coord
  else:
    return None

def save_to_string(save_value):
  if save_value == 7:
    return '-'
  else:
    return '{val}+'.format(val=save_value)

# Takes a number
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

# All values inclusive for now, ie min and max allowable numbers.
def constrainCoord(coord, rMin=0, rMax=DEFAULT_HEIGHT-1, cMin=0, cMax=DEFAULT_WIDTH-1):
  if coord[0] < rMin:
    newR = rMin
  elif coord[0] > rMax:
    newR = rMax
  else:
    newR = coord[0]

  if coord[1] < cMin:
    newC = cMin
  elif coord[1] > cMax:
    newC = cMax
  else:
    newC = coord[1]

  return [newR, newC]

def isCoord(object):
  return (type(object) == list
    and len(object) == 2
    and type(object[0]) == int
    and type(object[1]) == int)

def coordOf(obj):
  if isCoord(obj):
    return obj
  elif hasattr(obj, 'coord'):
    return obj.coord
  else:
    return None

# needs work
# takes 2 coords or 2 Things
def distance(a, b):
  aCoord = coordOf(a)
  bCoord = coordOf(b)
  rowdiff = abs(aCoord[0] - bCoord[0])
  coldiff = abs(aCoord[1] - bCoord[1])
  return int(round(math.sqrt(rowdiff**2 + coldiff**2)))

def areAdjacent(a, b):
  return distance(a,b) <= 1.5

def coord_sum(a, b):
  return [a[0] + b[0], a[1] + b[1]]

# TODO: more rolls, for Ld, to-hit, diff terrain, etc?
# TODO type up example ways of calling this funct.
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

# This function is sometimes called sign()
def one_zero_minusone(x):
  if x > 0:
    return 1
  elif x == 0:
    return 0
  else:
    return -1

# returns coord of form [0, -1] or [-1, 1], etc suggesting
# the rough direction from coords a to b.
# Only returns integer coordinates, so 9 possible return values (inc 0,0).
# used for Gamestate.act(). Kindof hacky.
def direction_from(a, b):
  diff_coord = [b[0] - a[0], b[1] - a[1]]
  return [one_zero_minusone(diff_coord[0]),
          one_zero_minusone(diff_coord[1])]

def coords_in_radius(center, radius=1, board_height=8, board_width=12):
  nw_corner = [center[0] - radius, center[1] - radius]
  pass

def next_letter(letter):
  return chr(ord(letter) + 1)
