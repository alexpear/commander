#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

import data
import util

import random

class Thing(object):
  def __init__(self, name='traitless thing', coord=[999,999], sprite='?'):
    self.name = name
    self.coord = coord
    self.sprite = sprite
    self.allegiance = 'gaia'
    self.quantity = 0
    self.ws = 0
    self.is_unit = False

  def get_sprite(self):
    return self.sprite

  def name_with_sprite(self):
    return self.name.capitalize() + ' (' + self.get_sprite() + ')'

  # TODO bug, sprites can show up as lowercase here when they shouldnt
  def verbose_info(self):
    string = (
      "{coord} {name}\n").format(
        coord=util.coordtostring(self.coord), name=self.name_with_sprite())
    return string

# for now, forget about being made up of Models / Creatures and Components
# Units have stats directly
# including a quantity stat
# only one (ranged) weapon each (for now)
# Units assumed homogenous for this prototype
# Color is the terminal display color
class Unit(Thing):
  # deprecated. Instead read from data.py dicts
  def __init__(self, name='?', ws=3, bs=3, s=3, t=3, w=1, i=3, a=1, ld=7, sv=7, 
      shootstr=3, ap=7, rng=2, weapontype='rapidfire', weaponshots=1,
      quantity=10, move_max=1, pt=10, color=32, allegiance='rebels'):
    self.is_unit = True  # TODO or thing.__class__.__name__ == 'Unit', alternately.
    self.name = name
    self.sprite = '?' # until Gamestate's add_thing() is called
    self.ws = ws
    self.bs = bs
    self.s = s
    self.t = t
    self.w = w
    self.wounds_taken = 0  # todo rename to floating_wounds?
    self.i = i
    self.a = a
    self.ld = ld
    self.sv = sv
    self.shootstr = shootstr
    self.ap = ap
    self.rng = rng
    self.weapontype = weapontype
    self.shotspercreature = weaponshots # to remove
    self.can_shoot = True
    self.can_assault = True
    self.casualties_this_phase = 0
    self.pt = pt
    self.move_max = move_max
    self.move_left = move_max
    self.size = 20
    self.quantity = quantity
    self.starting_quantity = quantity
    # TODO track allegiance as pointer to Army object, etc?
    self.allegiance = allegiance
    self.coord = [888,888]
    # most of these are pretty debug
    # later store wargear (or wargear stats), state, other stats from notes

  def verbose_info(self):
    abbreviatedAllegiance = self.allegiance[0:3].upper()

    # btw {foo:>2} means enforce 2-char width and right justify
    string = (
      'WS BS  S  T  W  I  A Ld Sv Pts Qty Total Army Float Coord Name\n' +
      '{ws:>2} {bs:>2} {s:>2} {t:>2} {w:>2} {i:>2} {a:>2} {ld:>2} {sv:<2}' +
      ' {pts:^3}  {qty:^2}  {total:^3}  {allegiance}    {fw}   {coord:^5} {name}\n').format(
        coord=util.coordtostring(self.coord), name=self.name_with_sprite(),
        qty=self.quantity, allegiance=abbreviatedAllegiance, ws=self.ws, bs=self.bs,
        s=self.s, t=self.t, w=self.w, i=self.i, a=self.a, ld=self.ld,
        sv=util.save_to_string(self.sv), pts=self.pt,
        total=self.pt * self.quantity, fw=self.wounds_taken)
    return string

  # TODO ability to refer to them by shortcuts while being 2-3 letters long
  def get_sprite(self, charcount=1, colorkey='red'):
    if self.allegiance.startswith('reb'):
      colorkey = 'red'
    else:
      colorkey = 'blue'
    # return '\x1b[' + data.colordict[colorkey] + self.name[:charcount].capitalize() + '\x1b[0m'
    return '\x1b[' + data.colordict[colorkey] + self.sprite + '\x1b[0m'

  def start_turn(self):
    self.move_left = self.move_max
    self.can_shoot = True
    # TODO: Change this logic for units that can never assault, etc
    self.can_assault = True
    self.casualties_this_phase = 0
    # TODO this field will need to be reset on end/start of phases later.

# TODO later just move this __dict__.update(stats from data.py) code to Unit()
def unit_from_stats_entry(stats_dict):
  new_unit = Unit()
  new_unit.__dict__.update(stats_dict)
  # TODO: wargear / weapons
  return new_unit

# TODO: or should we have short_name be the unit key in the dict?
def unit_from_short_name(type_name):
  for faction in data.unit_stats.itervalues():
    for unit_dict in faction.itervalues():
      if type_name.startswith(unit_dict['short_name']):
        # we have found it
        unit = unit_from_stats_entry(unit_dict)
        unit.name = type_name
        return unit
  return None

def new(typename, allegiance='rebels'):
  # later, use types list above
  lowercasename = typename.lower()
  new_unit = unit_from_short_name(lowercasename)
  new_unit.allegiance = allegiance
  return new_unit

def random_from_faction(faction, allegiance='rebels'):
  # get list of avail unit types (typenames)
  types = data.unit_stats[faction].keys()
  if len(types) <= 0:
    return new('mari', allegiance)
  # and get a random of the typenames
  # and call new with it
  else:
    return new(random.choice(types), allegiance)
