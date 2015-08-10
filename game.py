#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

import math

import gamestate
import unit_modu
import util

'''
turn based strategy wargame
6"x6" grid instead of continuous space.
eventually graphical
prototype
simple stats
first shooting-only, then melee
'''

# Could move these to data.py
legend = '''-1,-1  -1,0  -1,1

 0,-1         0,1

 1,-1   1,0   1,1'''

cardinal_directions = {
  'northwest': [-1,-1], 'north': [-1,0], 'northeast': [-1,1],
  'west' :      [0,-1], 'centre': [0,0], 'east' :      [0,1],
  'southwest':  [1,-1], 'south':  [1,0], 'southeast':  [1,1],
  # You can also refer to them with 2-letter abbreviations:
  'nw': [-1,-1], 'nn': [-1,0], 'ne': [-1,1],
  'ww' : [0,-1], 'cc':  [0,0], 'ee' : [0,1],
  'sw':  [1,-1], 'ss':  [1,0], 'se':  [1,1],
}

class Game:
  def __init__(self):
    self.gamestate = gamestate.Gamestate()
    self.turn_faction = 'protectorate'

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
  # eg, methodize a lot
  def parseinput(self, rawstring):
    if rawstring == '':
      return
    print ''
    cmd = rawstring.lower().strip()
    words = rawstring.lower().split()

    # TODO functionize these commands
    # Make Player objects?
    if words[0] in ('draw', 'look', 'grid', 'board', 'map', 'ls'):
      if len(words) == 1:
        # draw
        self.gamestate.printgrid()
        return
      else:
        # draw 3,2
        if (not words[1][0].isdigit()) or len(words) > 2:
          print 'Error, i can\'t understand this draw command'
          return
        targetcoord = Game.parsecoord(words[1])
        if targetcoord:
          thing = self.gamestate.thingat(targetcoord)
          if thing:
            print(thing.verbose_info())
            return
        print('Error, i dont know what you want to look at in given coord')
        return

    # units command, format 'squads', 'units', etc
    # prints detailed summary of all units, models etc
    elif words[0] in ['squads', 'units']:
      if len(words) != 1:
        print 'Error, i can\'t understand this units command'
        return
      for thing in self.gamestate.things:
        # Don't print info about terrain pieces, etc
        if thing.is_unit:
          print(thing.verbose_info())
      return

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
      return

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
      return

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
      return

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
          # TODO flip this branch: put more relevant block first
          if target is None:
            # alternately see if last word is in coord format
            # NOTE: assume relative not absolute coord
            # TODO: methodize, similar to 'go NW' syntax below
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
                # TODO flip this branch
                pass # TODO use target
            # Alternately see if fits format 'V southwest', telling unit V to move one square southwest
            elif (len(words) == 2 and
                words[-1].lower() in cardinal_directions.keys()):
              direction_coord = cardinal_directions[words[-1].lower()]
              # TODO methodize; this will be same as the block above
              absolute_destination = util.coord_sum(unit.coord, direction_coord)
              # TODO could check if they want to shoot, same as above
              self.gamestate.move(unit, absolute_destination)
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
            return
      else:
        print('error: at first i thought you were giving a unit-specific '
            + 'command, but i cant find a unit with that initial')
        return

    elif cmd == 'legend' or cmd == 'directions' or cmd == 'rose':
      print(legend)
      return

    # TODO: differentiate the two players' turns
    elif cmd in ('rebels', 'go', 'enemies', 'enemy turn', 'end turn', 'endturn', 'end', 'done'):
      # todo methodize as start_turn() run_turn() etc
      self.turn_faction = 'rebels'
      self.gamestate.refresh_army('rebels')
      for unit in self.gamestate.things:
        if unit.allegiance == 'rebels':
          print('\n {unit} is acting:'.format(
            unit=unit.name_with_sprite()))
          self.gamestate.act(unit)

      self.turn_faction = 'protectorate'
      self.gamestate.refresh_army('protectorate')
      return
    # TODO also ability to make the _protectorate_ auto-take its turn

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
    print 'Farewell.\n'
    return

g = Game()
g.gamestate.printgrid()
g.run()
