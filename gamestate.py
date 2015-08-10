import math
import random
from random import randrange

import unit_modu
import util

WIDTH = 12
HEIGHT = 8

TERRAIN_FREQUENCY = 0.25

# doesn't really do anything in this build but whatever
# maybe useful for terrain/cover later
# alt names: Tile Space Spot Location
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

class Gamestate:
  def refresh_army(self, allegiance='all'):
    for thing in self.things:
      if not thing.is_unit:
        continue
      if thing.allegiance.startswith(allegiance) or allegiance=='all':
        thing.start_turn()

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
      new_sprite = util.next_letter(new_sprite).lower()

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
      print 'error, move() is asked to move a pointer that evaluates to None'
      return

    # TODO: might need exception later for transport vehicles
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
    if thing.move_left < 1:
      print('Sorry, unit cannot move (any further) right now.')
      return

    elif thing.move_left < dist:
      print(
        'Sorry, unit cant move that far ({real}sq / {realin}", but move remaining ' +
        'is {move}sq / {movein}")').format(
          real=dist, realin=util.inches(dist),
          move=thing.move_left, movein=util.inches(thing.move_left))
      return

    elif self.thingat(destinationcoord):
      print('Sorry, unit cant move to occupied coord.')
      return

    elif self.zone_of_control_blocks(destinationcoord, thing):
      print('Sorry, unit cant move within 1 sq of an enemy unit.')
      return

    elif (destinationcoord[0] < 0 or destinationcoord[0] >= HEIGHT or
        destinationcoord[1] < 0 or destinationcoord[1] >= WIDTH):
      print('Error, unit cannot move out of bounds.')
      return

    # TODO: other checks, asserts
    self.debug_move(thing, destinationcoord)
    self.printgrid()

    # Mark that this unit has moved.
    thing.move_left -= dist

  def shoot(self, shooter, target):
    if not shooter.can_shoot:
      print('unit is not permitted to shoot right now')
      return
    elif target.quantity <= 0 or shooter.quantity <= 0:
      print 'error, one unit is empty / wiped out'
      return
    elif target.allegiance == shooter.allegiance:
      print('(was gonna shoot but didnt because both units are from same army)')
      return
    # more asserts? TODO

    dist = util.distance(shooter.coord, target.coord)
    if shooter.rng < dist:
      print(
        'Tried to shoot but target is out of range ({real}sq / {realin}", ' +
        'range: {max}sq / {maxin}")').format(
          real=dist, realin=util.inches(dist),
          max=shooter.rng, maxin=util.inches(shooter.rng))
      return

    print shooter.name_with_sprite() + ' is shooting at ' + target.name_with_sprite()

    shooter.can_shoot = False

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
      # TODO bug, 1 unsaved wound led to multiple lost models. seen once 2015 aug 9.
      self.damage(target, len(unsaved_wounds))
      print ' Now target has ' + str(target.quantity) + ' creatures left in it.'

  # TODO could unify this and spawn_thing
  def spawn_unit(self, faction, coord, allegiance='rebels'):
    if self.thingat(coord):
      print('Cant spawn unit on occupied square')
      return

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
    # todo do allegiance by enum or objs, not just strings
    self.spawn_unit("unsc", [randrange(0,2), randrange(0,WIDTH)], 'rebels')
    self.spawn_unit("unsc", [randrange(0,2), randrange(0,WIDTH)], 'rebels')

    self.spawn_unit("unsc", [randrange(HEIGHT-2,HEIGHT), randrange(0,WIDTH)], 'protectorate')
    self.spawn_unit("unsc", [randrange(HEIGHT-2,HEIGHT), randrange(0,WIDTH)], 'protectorate')

  def spawn_random_terrain(self):
    for r in range(HEIGHT):
      for c in range(WIDTH):
        coord = [r,c]
        if not self.thingat(coord):
          if random.random() < (TERRAIN_FREQUENCY):
            # Just chasms for now
            self.spawn_thing('chasm', coord)

  # tag Gamestate init gamestate __init__()
  def __init__(self):
    self.grid = [[Square() for c in range(WIDTH)] for r in range(HEIGHT)]
    self.things = []  # all things
    self.spawndebugunits()
    self.spawn_random_terrain()

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
        util.direction_from(cur, chosen_target.coord)))

    # Now shoots target:
    self.shoot(acting_unit, chosen_target)
