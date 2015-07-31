#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

import unit_modu
import util
import math

'''
turn based strategy wargame
6"x6" grid instead of continuous space.
eventually graphical
prototype
simple stats
first shooting-only, then melee
'''

legend = '''-1,-1  -1,0  -1,1

 0,-1         0,1

 1,-1   1,0   1,1'''

cardinal_directions = {
  'northwest': [-1,-1], 'north': [-1,0], 'northeast': [-1,1],
  'west' :  [0,-1], 'centre':  [0,0], 'east' :  [0,1],
  'southwest':  [1,-1], 'south':  [1,0], 'southeast':  [1,1]
  # 'nw': [-1,-1], 'n': [-1,0], 'ne': [-1,1],
  # 'w' :  [0,-1], 'x':  [0,0], 'e' :  [0,1],
  # 'sw':  [1,-1], 's':  [1,0], 'se':  [1,1],
}

WIDTH = 12
HEIGHT = 8

# doesn't really do anything in this build but whatever
# maybe useful for terrain/cover later
# alt names: Tile Square Space Spot Location
class Square:
  def __init__(self):
    self.terrain = None

# a shot or attack in shooting or assault.
# Can also become a hit, wound, unsaved wound at various times.
class Attack:
  def __init__(self, s, ap=7, specials=[]):
    self.s = s
    self.ap = ap
    self.specials = specials
    self.active = True

# TODO: make a class Util

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

class Gamestate:
  # a 'sprite' here is an ascii-graphics character
  def sprite_is_taken(self, sprite):
    for thing in self.things:
      if thing.sprite == sprite:
        return True
    return False

  def choose_sprite(self, thing):
    # TODO later might be 'if thing.name in exception_list', terrain_names, etc
    if thing.name == 'chasm':
      return thing.sprite

    # If not taken, return first letter of its name, ideally lowercase.
    new_sprite = thing.name[0].lower()
    while self.sprite_is_taken(new_sprite):
      # Next try uppercase version
      new_sprite = new_sprite.upper()
      if not self.sprite_is_taken(new_sprite):
        return new_sprite
      # Failing that, resort to the next free letter in the alphabet
      new_sprite = next_letter(new_sprite).lower()

    return new_sprite

  def add_thing(self, newthing):
    newthing.sprite = self.choose_sprite(newthing)
    self.things.append(newthing)

  # Called when a unit takes wounds
  def damage(self, unit, wounds):
    unit.wounds_taken += wounds
    if unit.wounds_taken >= unit.w:
      # The floors could be overkill idk.
      casualties = math.floor(unit.wounds_taken) / math.floor(unit.w)
      # Maintain int type.
      unit.quantity -= int(casualties)
      if unit.quantity <= 0:
        self.things.remove(unit)
        # TODO call this with more fanfare and ceremony?
    # TODO once turns are implemented, track casualties per turn
    # because of 25% thing, etc

  def zone_of_control_blocks(self, coord, mover):
    for other_thing in self.things:
      if (other_thing.ws > 0 and
          other_thing.allegiance != mover.allegiance and
          util.distance(coord, other_thing.coord) <= 1 and
          other_thing.quantity > 0):
        return True
    return False

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
  
    if thing not in self.things:
      self.add_thing(thing)
    thing.coord = destinationcoord

  # Use this to move units
  def move(self, thing, destinationcoord):
    # assuming the Thing is a Unit
    dist = util.distance(thing.coord, destinationcoord)
    if thing.move < dist:
      print(
        'Sorry, unit cant move that far ({real}sq / {realin}", but move ' +
        'is {max}sq / {maxin}")').format(
          real=dist, realin=util.inches(dist),
          max=thing.move, maxin=util.inches(thing.move))
      return

    elif self.thingat(destinationcoord):
      print('Sorry, unit cant move to occupied coord')
      return

    if self.zone_of_control_blocks(destinationcoord, thing):
      print('Sorry, unit cant move within 1 sq of an enemy unit')
      return

    # TODO: other checks, asserts
    self.debug_move(thing, destinationcoord)

  def shoot(self, shooter, target):
    if target.quantity <= 0 or shooter.quantity <= 0:
      print 'error, one unit is empty / wiped out'
      return
    elif target.allegiance == shooter.allegiance:
      print('(was gonna shoot but didnt because both units are from same army)')
      return
    # more asserts? TODO

    print shooter.name_with_sprite() + ' is shooting at ' + target.name_with_sprite()
    dist = util.distance(shooter.coord, target.coord)
    if shooter.rng < dist:
      print(
        'Sorry, target is out of range ({real}sq / {realin}", ' +
        'range: {max}sq / {maxin}")').format(
          real=dist, realin=util.inches(dist),
          max=shooter.rng, maxin=util.inches(shooter.rng))
      return

    print ' ' + util.conjugateplural(shooter.quantity, "shooter") + "..."

    totalshotcount = shooter.shotspercreature * shooter.quantity
    attacks = []
    for i in range(totalshotcount):
      attacks.append(Attack(shooter.shootstr, shooter.ap))

    print ' ' + util.conjugateplural(len(attacks), "shot") + "..."

    # To Hit
    for attack in attacks:
      if not attack.active:
        continue
      need_to_roll = 7 - shooter.bs
      need_to_roll = util.constrain(need_to_roll, 2, 6)
      result = util.roll(
        'Shooting to-hit roll, shooter needs a {goal}+'.format(goal = need_to_roll),
        successif = (lambda n: n>=need_to_roll))
      if result < need_to_roll:
        attack.active = False

    # Attacks that do not hit, wound, etc are marked .active = False
    # And then removed. Might be clumsy.
    hits = [a for a in attacks if a.active]
    print ' ' + util.conjugateplural(len(hits), "hit") + "..."

    # To Wound
    for attack in hits:
      need_to_roll = target.t - shooter.shootstr + 4
      need_to_roll = util.constrain(need_to_roll, 2, 6)
      result = util.roll(
        'Shooting to-wound roll, shooter needs a {goal}+'.format(goal = need_to_roll), 
        successif = (lambda n: n>=need_to_roll))
      if result < need_to_roll:
        attack.active = False

    wounds = [a for a in hits if a.active]
    print ' ' + util.conjugateplural(len(wounds), "pre-saving wound") + "..."

    # Saves
    for attack in wounds:
      # TODO: invulnerable saves, cover saves
      if target.sv >= 7 or target.sv >= attack.ap:
        break
      need_to_roll = target.sv
      result = util.roll(
        'Shooting armor save, target saves on a {goal}+'.format(goal = need_to_roll))
      if result >= need_to_roll:
        attack.active = False

    unsaved_wounds = [a for a in wounds if a.active]
    # print final results summary
    print ' {n} casualties...'.format(n=len(unsaved_wounds))
  
    if len(unsaved_wounds) > 0:
      self.damage(target, len(unsaved_wounds))
      print ' Now target has ' + str(target.quantity) + ' creatures left in it.'

  # TODO could unify this and spawn_thing
  def spawn_unit(self, faction, coord, allegiance='rebels'):
    unit = unit_modu.random_from_faction(faction, allegiance)
    self.add_thing(unit)
    self.debug_move(unit, coord)

  def spawn_thing(self, name, coord):
    thing = unit_modu.Thing(name=name, coord=coord)

    # Cascade for populating special traits eg terrain:
    if name == 'chasm':
      thing.sprite = '0'

    self.add_thing(thing)

  def spawndebugunits(self):
    # todo could invest in specifying scenario by grid of chars.
    self.spawn_thing('chasm', [1,1])

    self.spawn_unit("unsc", [0,3], 'protectorate')

    self.spawn_thing('chasm', [0,6])
    self.spawn_thing('chasm', [1,6])

    self.spawn_unit("unsc", [0,8], 'protectorate')

    self.spawn_thing('chasm', [2,3])
    self.spawn_thing('chasm', [3,3])
    self.spawn_thing('chasm', [2,4])

    self.spawn_thing('chasm', [4,6])
    self.spawn_thing('chasm', [4,7])
    self.spawn_thing('chasm', [4,8])
    self.spawn_thing('chasm', [4,9])

    self.spawn_unit("unsc", [7,2], 'rebels')

    self.spawn_thing('chasm', [7,5])
    self.spawn_thing('chasm', [7,6])

    self.spawn_unit("unsc", [7,9], 'rebels')

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
          print thing.get_sprite(),
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
        print util.distance([0,0], [r,c]) % 10,
      print '| ' + str(r)
    print '    - - - - - - - - - - - -'
    print '    0 1 2 3 4 5 6 7 8 9 X E'
    print ''

  # simple AI method. Unit does what it thinks best action would be.
  # TODO improve. Currently moves toward and shoots closest foe.
  def act(self, acting_unit):
    # First chooses closest foe as target:
    chosen_target = None
    shortest_so_far = 999 # shortest distance of a foe so far
    for other_unit in self.things:
      if (other_unit.allegiance == 'gaia' or
          other_unit.allegiance == acting_unit.allegiance or
          other_unit.quantity <= 0):
        continue  # invalid unit, not a foe
      dist = util.distance(other_unit.coord, acting_unit.coord)
      if dist < shortest_so_far:
        shortest_so_far = dist
        chosen_target = other_unit

    if chosen_target == None:
      return

    # Now moves toward target:
    # really hacky:
    cur = acting_unit.coord
    self.move(
      acting_unit,
      util.coord_sum(
        cur,
        direction_from(cur, chosen_target.coord)))
    self.printgrid()

    # Now shoots target:
    self.shoot(acting_unit, chosen_target)


class Game:
  def __init__(self):
    self.gamestate = Gamestate()

  # if coord is correctly formatted (eg '4,8' with no spaces) return as [4,8]
  # else return None
  @classmethod
  def parsecoord(cls, coordstring):
    # We allow either the 0th or 1st char to be digit,
    # because 0th char might be a '-' for a negative number
    if (coordstring.find(',') is not -1 and
        (coordstring[0].isdigit() or coordstring[1].isdigit()) and
        coordstring[-1].isdigit()):
      halves = coordstring.strip().split(',')
      coord = [int(halves[0]), int(halves[1])]
      # commented this check out because doesn't apply to relative coord inputs
      # if coord[0] < 0 or coord[0] >= HEIGHT or coord[1] < 0 or coord[1] >= WIDTH:
        # print 'BTW: parsed coordinate not on board'
      return coord
    else:
      return None

  # todo low priority: make this cascade into something neater
  def parseinput(self, rawstring):
    if rawstring == '':
      return
    print ''
    cmd = rawstring.lower().strip()
    words = rawstring.lower().split()

    if words[0] in ('draw', 'look', 'grid', 'board', 'map', 'ls'):
      if len(words) == 1:
        # draw
        self.gamestate.printgrid()
      else:
        # draw 3,2
        if (not words[1][0].isdigit()) or len(words) > 2:
          print 'Error, i can\'t understand this draw command'
          return
        targetcoord = Game.parsecoord(words[1])
        if targetcoord:
          thing = self.gamestate.thingat(targetcoord)
          if thing:
            thing.verbose_info()
            return
        print('Error, i dont know what you want to look at in given coord')

    # units command, format 'squads', 'units', etc
    # prints detailed summary of all units, models etc
    elif words[0] in ['squads', 'units']:
      if len(words) != 1:
        print 'Error, i can\'t understand this units command'
        return
      for thing in self.gamestate.things:
        print thing.verbose_info()

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
      if not spawncoord or (
          spawncoord[0] < 0 or spawncoord[0] >= HEIGHT or 
          spawncoord[1] < 0 or spawncoord[1] >= WIDTH):
        print('Error, new command out of bounds or otherwise invalid')
        return
      newunit = unit_modu.new(words[1])
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
            # NOTE: assume relative not absolute coord
            rel_coord = Game.parsecoord(words[-1])
            if rel_coord:
              abs_coord = util.coord_sum(unit.coord, rel_coord)
              target = self.gamestate.thingat(abs_coord)
              if target is None:
                # they want to move
                self.gamestate.move(unit, abs_coord)
                self.gamestate.printgrid()
                return
            else:
              print('error, couldnt parse context sensitive unit command')
              return
          else:
            # they want to shoot at target (or assault TODO)
            # TODO check if both friendlies,
            # then if so move first towards the second.
            self.gamestate.shoot(unit, target)
      else:
        print('error: at first i thought you were giving a unit-specific '
            + 'command, but i cant find a unit with that initial')

    elif cmd == 'legend' or cmd == 'directions' or cmd == 'rose':
      print(legend)

    elif cmd in ('rebels', 'go', 'enemies', 'enemy turn'):
      for unit in self.gamestate.things:
        if unit.allegiance == 'rebels':
          print('\n {unit} is acting:'.format(
            unit=unit.name_with_sprite()))
          self.gamestate.act(unit)
    # TODO also ability to make protectorate auto-take its turn

    # elif cmd in ('newgame', 'new game', 'start over', 'reset'):      
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
