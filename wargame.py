#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

import math
import random

'''
my 'wargame' is cool, but /this/ copy of the file 
is being slowly converted into a simplified 40k rules game. 
6"x6" grid instead of continuous space. 
'''

'''
  turn based strategy wargame
  roughly 40k style
  eventually graphical
  prototype
  simple stats
  first shooting-only, then melee
  '''

# global methods, maybe clumsy:

colordict = {
  'black': '1;37;40m',
  'red': '1;37;41m',
  'green': '1;30;42m',
  'yellow': '1;30;43m',
  'blue': '1;37;44m',
  'purple': '1;37;45m',
  'cyan': '1;30;46m',
  'grey': '1;30;47m'
}

def tiles(inches):
  return inches / 6.0
def inches(tiles):
  return tiles * 6

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

WIDTH = 12
HEIGHT = 8

# doesn't really do anything in this build but whatever
# maybe useful for terrain/cover later
# alt names: Tile Square Space Spot Location
class Square:
  def __init__(self):
    self.terrain = None

class Thing:
  def __init__(self):
    self.name = 'traitless thing'
    self.coord = [999,999]

# for now, forget about being made up of Models / Creatures and Components
# Units have stats directly
# including a quantity stat
# only one (ranged) weapon each (for now)
# Units assumed homogenous for this prototype
# Color is the terminal display color
class Unit(Thing):
  def __init__(self, name='?', ws=3, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7, sv=7, 
      shootstr=3, ap=7, rng=2, weapontype='rapidfire', weaponshots=1,
      quantity=10, move=1, pt=10, color=32, allegiance='rebels'):
    self.name = name
    self.sprite = '?' # until Gamestate's add_thing() is called
    self.move = move
    self.ws = ws
    self.bs = bs
    self.s = s
    self.t = t
    self.w = w
    self.i = i
    self.a = a
    self.ld = ld
    self.sv = sv
    self.shootstr = shootstr
    self.ap = ap
    self.rng = rng
    self.weapontype = weapontype
    self.shotspercreature = weaponshots # to remove
    self.pt = pt
    self.move_left = self.move
    self.size = 20
    self.quantity = quantity
    self.allegiance = allegiance
    self.coord = [888,888]
    # most of these are pretty debug
    # later store wargear (or wargear stats), state, other stats from notes

  def printinfo(self):
    string = (
	    "{coord} {name} x{quant}, " +
      "WS{ws} BS{bs} S{s} T{t} W{w} I{i} A{a} Ld{ld} Sv{sv}+ Pt{pt}").format(
	      coord=Game.coordtostring(self.coord), name=self.name.capitalize(),
	      quant=self.quantity, ws=self.ws, bs=self.bs, s=self.s, t=self.t,
	      w=self.w, i=self.i, a=self.a, ld=self.ld,
	      sv=self.sv, pt=self.pt)
    print string

  # TODO unused so far
  def sprite(self, charcount=3, colorkey='black'):
    return '\x1b[' + colordict[colorkey] + self.name[:charcount] + '\x1b[0m'  
    # untested

  # types = {'space marine' : }

  @classmethod
  def new(cls, typename, allegiance='rebels'):
    # later, use types list above
    lowercasename = typename.lower()
    # Tactical Squad
    if lowercasename.startswith('tactical'):
      new_unit = Unit(typename, 4, 4, 4, 4, 1, 4, 1, 8, sv=3, 
        shootstr=4, ap=5, rng=2, weaponshots=2,
        quantity=10, move=1, pt=16)
    # Assault Marines
    elif lowercasename.startswith('assault'):
      new_unit = Unit(typename, 4, 4, 4, 4, 1, 4, 2, 8, sv=3, 
        shootstr=4, ap=5, rng=2, quantity=10, move=2, pt=22)
    # Devastator Squad of 4, w/ lascannons:
    elif lowercasename.startswith('devastator'):
      new_unit = Unit(typename, 4, 4, 4, 4, 1, 4, 1, 8, sv=3, 
        shootstr=9, ap=2, rng=8, quantity=4, move=1, pt=26)
    # Siege/Sapper Imperial Guard troops
    elif lowercasename.startswith('siege'):
      new_unit = Unit(typename, 3, 3, 3, 3, 1, 3, 1, 6, sv=6, 
        shootstr=3, ap=7, rng=2, weaponshots=2,
        quantity=20, move=1, pt=9)
    # Cadia-esque cadets, also Ender's G, that one Halo series
    elif lowercasename.startswith('cadet'):
      new_unit = Unit(typename, 2, 2, 3, 2, 1, 3, 1, 5, sv=7,
        shootstr=3, ap=7, rng=3, weaponshots=2,
        quantity=15, move=1, pt=6)
    else:
      print 'error, i did not recognize Unit typename. im giving it default stats.'
      new_unit = Unit(typename)

    new_unit.allegiance = allegiance
    return new_unit

# a shot or attack in shooting or assault. 
# Can also become a hit, wound, unsaved wound at various times. 
class Attack:
  def __init__(self, s, ap=7, specials=[]):
    self.s = s
    self.ap = ap
    self.specials = specials
    self.active = True

# returns coord of form [0, -1] or [-1, 1], etc suggesting
# the rough direction from coords a to b.
# Only returns integer coordinates, so 9 possible return values (inc 0,0).
# used for Gamestate.act(). Kindof hacky.
def direction_from(a, b):
  diff_coord = [b[0] - a[0], b[1] - a[1]]
  def one_zero_minusone(x):
    if x > 0:
      return 1
    elif x == 0:
      return 0
    else:
      return -1
  return [one_zero_minusone(diff_coord[0]),
          one_zero_minusone(diff_coord[1])]

class Gamestate:
  def add_thing(self, newthing):
    # choose sprite for newthing
    # first choice, lower sprite. upper if necessary. (lower is easier to type)
    lower_sprite = newthing.name[0].lower()
    upper_sprite = newthing.name[0].upper()
    lower_name_collision = False
    for oldthing in self.things:
      if oldthing.sprite == upper_sprite:
        print('cant add ' + newthing.name +
              ' because we already have this uppercase sprite')
        return
      if oldthing.sprite == lower_sprite:
        lower_name_collision = True
    if lower_name_collision:
      newthing.sprite = upper_sprite
    else:
      newthing.sprite = lower_sprite
    # add newthing to the list
    self.things.append(newthing)

  # called when a unit takes wounds
  def damage(self, unit, wounds):
    # TODO: multiwound model support
    unit.quantity -= wounds
    if unit.quantity <= 0:
      self.things.remove(unit)
      # TODO call this with more fanfare and ceremony?
    # TODO once turns are implemented, track casualties per turn
    # because of 25% thing, etc

  # Has less restrictions than move()
  def debug_move(self, thing, destinationcoord):
    if thing==None:
      print 'error, move() is asked to move a pointer to None'
      return

    # TODO: might need exception later for transport vehicles? 
    # If something is occupying the destination:
    if self.thingat(destinationcoord):
      print 'error, destination {r},{c} is already occupied'.format(
        r=destinationcoord[0], c=destinationcoord[1])
  
    # TODO? if not in self.things, add to self.things
    thing.coord = destinationcoord

  # Use this to move units
  def move(self, thing, destinationcoord):
    # assuming the Thing is a Unit (or Model maybe?)
    dist = distance(thing.coord, destinationcoord)
    if thing.move < dist:
      print(
      	'Sorry, unit cant move that far ({real}sq / {realin}", but move ' +
      	'is {max}sq / {maxin}")').format(
		      real=dist, realin=inches(dist), 
		      max=thing.move, maxin=inches(thing.move))
      return
    elif self.thingat(destinationcoord):
      print('Sorry, unit cant move to occupied coord')
      return

    # TODO: other checks, asserts
    self.debug_move(thing, destinationcoord)

  def shoot(self, shooter, target):
    # asserts TODO
    if target.quantity <= 0 or shooter.quantity <= 0:
      print 'error, one unit is empty / wiped out'
      return
    elif target.allegiance == shooter.allegiance:
      print('(was gonna shoot but didnt because both units are from same army)')
      return
    # print stuff TODO

    print shooter.name + ' is shooting at ' + target.name
    dist = distance(shooter.coord, target.coord)
    if shooter.rng < dist:
      print(
      	'Sorry, target is out of range ({real}sq / {realin}", ' +
      	'range: {max}sq / {maxin}")').format(
		      real=dist, realin=inches(dist),
	      	max=shooter.rng, maxin=inches(shooter.rng))
      return

    print ' ' + conjugateplural(shooter.quantity, "shooter") + "..."

    totalshotcount = shooter.shotspercreature * shooter.quantity
    attacks = []
    for i in range(totalshotcount):
      attacks.append(Attack(shooter.shootstr, shooter.ap))

    print ' ' + conjugateplural(len(attacks), "shot") + "..."

    # To Hit
    for attack in attacks:
      if not attack.active:
        continue
      need_to_roll = 7 - shooter.bs
      need_to_roll = constrain(need_to_roll, 2, 6)
      result = roll(
        'Shooting to-hit roll, shooter needs a {goal}+'.format(goal = need_to_roll),
        successif = (lambda n: n>=need_to_roll))
      if result < need_to_roll:
        attack.active = False

    # Attacks that do not hit, wound, etc are marked .active = False
    # And then removed. Might be clumsy. 
    hits = [a for a in attacks if a.active]
    print ' ' + conjugateplural(len(hits), "hit") + "..."

    # To Wound
    for attack in hits:
      need_to_roll = target.t - shooter.shootstr + 4
      need_to_roll = constrain(need_to_roll, 2, 6)
      result = roll(
        'Shooting to-wound roll, shooter needs a {goal}+'.format(goal = need_to_roll), 
        successif = (lambda n: n>=need_to_roll))
      if result < need_to_roll:
        attack.active = False

    wounds = [a for a in hits if a.active]
    print ' ' + conjugateplural(len(wounds), "pre-saving wound") + "..."

    # Saves
    for attack in wounds:
      # TODO: invulnerable saves, cover saves
      if target.sv >= 7 or target.sv >= attack.ap:
        break
      need_to_roll = target.sv
      result = roll(
        'Shooting armor save, target saves on a {goal}+'.format(goal = need_to_roll))
      if result >= need_to_roll:
        attack.active = False

    unsaved_wounds = [a for a in wounds if a.active]
    # print final results summary
    print ' {n} casualties...'.format(n=len(unsaved_wounds))
  
    if len(unsaved_wounds) > 0:
      self.damage(target, len(unsaved_wounds))
      print ' Now target has ' + str(target.quantity) + ' creatures left in it.'

  def spawn_unit(self, typename, coord, allegiance='rebels'):
    unit = Unit.new(typename, allegiance)
    self.add_thing(unit)
    self.debug_move(unit, coord)

  def spawndebugunits(self):
    # protectorate side (north)
    self.spawn_unit("Devastator squad", [1,7], 'protectorate')
    self.spawn_unit("Assault marines", [1,4], 'protectorate')

    # rebels side (south)
    self.spawn_unit("Cadets", [7,2], 'rebels')
    self.spawn_unit("Tactical squad", [6,5], 'rebels')
    self.spawn_unit("Cadets", [7,9], 'rebels')

  # tag Gamestate init gamestate __init__()
  def __init__(self):
    self.grid = [[Square() for c in range(WIDTH)] for r in range(HEIGHT)]
    self.things = []  # all things
    self.spawndebugunits()

  def width(self):
    return len(self.grid)

  def height(self):
    return len(self.grid[0])

  def thingat(self, coord):
    for thing in self.things:
      if thing.coord == coord:
        return thing
    else:
      return None

  def unit_from_sprite(self, sprite):
    for thing in self.things:
      if thing.sprite == sprite:
        return thing
    else:
      return None

  def printgrid(self):
    print ''
    print '  c 0 1 2 3 4 5 6 7 8 9 X E'
    print 'r   - - - - - - - - - - - -'
    for r in range(self.width()):
      print str(r) + ' |',
      for c in range(self.height()):
        thing = self.thingat([r,c])
        if thing == None:
          print ' ',
        else:
          print thing.sprite,
      print '| ' + str(r)
    print '    - - - - - - - - - - - -'
    print '    0 1 2 3 4 5 6 7 8 9 X E'
    print ''

  # debug
  def distancetest(self):
    print ''
    print '  c 0 1 2 3 4 5 6 7 8 9 X E'
    print 'r   - - - - - - - - - - - -'
    for r in range(self.width()):
      print str(r) + ' |',
      for c in range(self.height()):
        print distance([0,0], [r,c]) % 10,
      print '| ' + str(r)
    print '    - - - - - - - - - - - -'
    print '    0 1 2 3 4 5 6 7 8 9 X E'
    print ''

  # simple AI method. Unit does what it thinks best action would be.
  # TODO improve. Currently moves toward and shoots closest foe.
  def act(self, acting_unit):
    # First chooses closest foe as target:
    chosen_target = self.things[0]
    shortest_so_far = 999 # shortest distance of a foe so far
    for other_unit in self.things:
      if (other_unit.allegiance == acting_unit.allegiance or
          other_unit.quantity <= 0):
        continue  # invalid unit, not a foe
      dist = distance(other_unit.coord, acting_unit.coord)
      if dist < shortest_so_far:
        shortest_so_far = dist
        chosen_target = other_unit

    # Now moves toward target:
    # really hacky:
    cur = acting_unit.coord
    self.move(
      acting_unit,
      coord_sum(
        cur,
        direction_from(cur, chosen_target.coord)))
    self.printgrid()

    # Now shoots target:
    self.shoot(acting_unit, chosen_target)


class Game:
  def __init__(self):
    self.gamestate = Gamestate()

  @classmethod
  def coordtostring(cls, coord):
    return "{0},{1}".format(coord[0],coord[1])

  # if coord is correctly formatted (eg '4,8' with no spaces) return as [4,8]
  # else return None
  @classmethod
  def parsecoord(cls, coordstring):
    if (coordstring.find(',') is not -1 and
        coordstring[0].isdigit() and
        coordstring[-1].isdigit()):
      halves = coordstring.strip().split(',')
      coord = [int(halves[0]), int(halves[1])]
      if coord[0] < 0 or coord[0] >= HEIGHT or coord[1] < 0 or coord[1] >= WIDTH:
        print 'BTW: parsed coordinate not on board'
      return coord
    else:
      return None

  def parseinput(self, rawstring):
    if rawstring == '':
      return
    print ''
    cmd = rawstring.lower().strip()
    words = rawstring.lower().split()

    if words[0] in ('draw', 'look', 'grid', 'board', 'map'):
      if len(words) == 1:
        # draw
        self.gamestate.printgrid()
      else:
        # draw 3,2
        if (not words[1][0].isdigit()) or len(words) > 2:
          print 'Error, i can\'t understand this draw command'
          return
        targetcoord = Game.parsecoord(words[1])
        # call a method to print detailed summary of targetcoord +++ TODO
        pass
    # units command, format 'squads', 'units', etc
    # prints detailed summary of all units, models etc
    elif words[0] in ['squads', 'units']:
      if len(words) != 1:
        print 'Error, i can\'t understand this units command'
        return
      for thing in self.gamestate.things:
        thing.printinfo()

    # TODO: formats like 'move 2,3 2,4', 'shoot 0,1 0,9' etc
    # move command, format 'move 2,3 to 4,1' or 'move 2,3 4,1' for now
    elif words[0]=='move':
      if len(words) < 3 or (not words[1][0].isdigit()) or (not words[-1][0].isdigit()):
        print 'error, badly formed move command'
        return
      startcoord = Game.parsecoord(words[1])
      mover = self.gamestate.thingat(startcoord)
      if mover==None:
        print 'error, there is nothing here to move'
        return
      destinationcoord = Game.parsecoord(words[-1])
      self.gamestate.move(mover, destinationcoord)
      self.gamestate.printgrid()
    # shoot command, format 'shoot 2,3 at 4,1' or without the 'at'.
    elif words[0] in ('shoot', 'attack', 'fire'):
      if len(words) < 3 or (not words[1][0].isdigit()) or (not words[-1][0].isdigit()):
        print 'error, badly formed shoot command'
        return
      shootercoord = Game.parsecoord(words[1])
      targetcoord = Game.parsecoord(words[-1])
      shooter = self.gamestate.thingat(shootercoord)
      target = self.gamestate.thingat(targetcoord)
      if shooter == None:
        print 'error, shooter coord {r},{c} is empty'.format(
          r=shootercoord[0], c=shootercoord[1])
        return
      if target == None:
        print 'error, no target found at {r},{c}'.format(
          r=targetcoord[0], c=targetcoord[1])
        return
      self.gamestate.shoot(shooter, target)
    # new Unit command, format 'new strider 3,2' for now
    elif words[0]=='new':
      if (len(words) != 3) or (not words[2][0].isdigit()):
        print 'error, badly formed \'new\' command'
        return
      # check for out of bounds TODO
      spawncoord = Game.parsecoord(words[2])
      newunit = Unit.new(words[1])
      self.gamestate.add_thing(newunit)
      self.gamestate.debug_move(newunit, spawncoord)
      self.gamestate.printgrid()
    elif cmd.startswith('quit') or cmd.startswith('exit'):
      return True
    # context-sensitive command for a unit: TODO: clean up logic
    elif (self.gamestate.unit_from_sprite(rawstring.split()[0])):
      # how to do this without code duplication?
      rawwords = rawstring.split()
      unit = self.gamestate.unit_from_sprite(rawwords[0]) 
      if unit:
        # singleword version. calls act() on unit (bot behavior)
        if len(words) == 1:
          self.gamestate.act(unit)
        # multiword version: [unit] [do something]
        elif len(words) >= 2:
          # first see if last word describes a unit
          target = self.gamestate.unit_from_sprite(rawwords[-1])
          if target is None:
            # alternately see if last word is in coord format
            coord = Game.parsecoord(words[-1])
            if coord:
              target = self.gamestate.thingat(coord)
              if target is None:
                # they want to move
                self.gamestate.move(unit, coord)
                self.gamestate.printgrid()
                return
            else:
              print('error, couldnt parse context sensitive unit command')
          # they want to shoot at target (or assault later)
          # TODO check if both friendlies, then move first towards the second.
          self.gamestate.shoot(unit, target)
      # TODO command that asks for info about a specific sprite 
      else:
        print('error: at first i thought you were giving a unit-specific '
            + 'command, but i cant find a unit with that initial')
    else:
      print ''
      print 'Sorry, i don\'t know what you\'re trying to say.'
      print ''

  def run(self):
    print ''
    done = False
    while not done:
      print ''
      rawinput = raw_input('> ')
      print ''
      done = self.parseinput(rawinput)
    print 'Farewell.'
    return


g = Game()
g.gamestate.printgrid()
g.run()


'''
TODO: 
-move some conceptual sections out into separate files/modules
-unique sprites
 -s and S
 -max 2 of each of same unit for now  
  -later can add ' / prime notation, for 4 repeats
-each unit having an army alignment
-basic act() behavior for a bot-controlled unit
-rapid fire, heavy etc rules
 -track moved, shot per unit
-spawn random units 
 -prereq?: store unit stats as dict? 
-simple assault, obv
-printinfo command for a specific unit?     
-clean up tabs and end-of-line whitespace in files
-relative move instead of absolute-coord move





'''
