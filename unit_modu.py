#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

import data

# TODO probably should be in some global string utilities file
# or unit's printinfo() should be in Game
def coordtostring(coord):
  return "{0},{1}".format(coord[0],coord[1])

def save_to_string(save_value):
  if save_value == 7:
    return '-'
  else:
    return '{val}+'.format(val=save_value)

class Thing(object):
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
  # deprecated. Instead read from data.py dicts 
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
    self.wounds_taken = 0
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
    # TODO track allegiance as pointer to Army object, etc?
    self.allegiance = allegiance
    self.coord = [888,888]
    # most of these are pretty debug
    # later store wargear (or wargear stats), state, other stats from notes

  def printinfo(self):
    alleg = 'PRO'
    if self.allegiance == 'rebels':
      alleg = 'REB'

    string = (
      "{coord} {name} ({sprite}) x{quant} {allegiance}\n" +
      "    WS{ws} BS{bs} S{s} T{t} W{w} I{i} A{a} Ld{ld}, " +
      "{sv_type} save: {sv}, {pt} points each\n").format(
        coord=coordtostring(self.coord), name=self.name.capitalize(),
        sprite=self.sprite, quant=self.quantity, allegiance=alleg, ws=self.ws, bs=self.bs,
        s=self.s, t=self.t, w=self.w, i=self.i, a=self.a, ld=self.ld,
        sv=save_to_string(self.sv), sv_type='armor', pt=self.pt)
    print string

  # TODO ability to refer to them by shortcuts while being 2-3 letters long
  def get_sprite(self, charcount=1, colorkey='red'):
    if self.allegiance.startswith('rebel'):
      colorkey = 'red'
    else:
      colorkey = 'blue'
    # return '\x1b[' + data.colordict[colorkey] + self.name[:charcount].capitalize() + '\x1b[0m'  
    return '\x1b[' + data.colordict[colorkey] + self.sprite + '\x1b[0m'  

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
    # new_unit = Unit(typename, 4, 4, 4, 4, 1, 4, 1, 8, sv=3, 
    #   shootstr=4, ap=5, rng=2, weaponshots=2,
    #   quantity=10, move=1, pt=16)
  # # Assault Marines
  # elif lowercasename.startswith('assault'):
  #   new_unit = Unit(typename, 4, 4, 4, 4, 1, 4, 2, 8, sv=3, 
  #     shootstr=4, ap=5, rng=2, quantity=10, move=2, pt=22)
  # # Devastator Squad of 4, w/ lascannons:
  # elif lowercasename.startswith('devastator'):
  #   new_unit = Unit(typename, 4, 4, 4, 4, 1, 4, 1, 8, sv=3, 
  #     shootstr=9, ap=2, rng=8, quantity=4, move=1, pt=26)
  # # Siege/Sapper Imperial Guard troops
  # elif lowercasename.startswith('siege'):
  #   new_unit = Unit(typename, 3, 3, 3, 3, 1, 3, 1, 6, sv=6, 
  #     shootstr=3, ap=7, rng=2, weaponshots=2,
  #     quantity=20, move=1, pt=9)
  # # Cadia-esque cadets, also Ender's G, that one Halo series
  # elif lowercasename.startswith('cadet'):
  #   new_unit = Unit(typename, 2, 2, 3, 2, 1, 3, 1, 5, sv=7,
  #     shootstr=3, ap=7, rng=3, weaponshots=2,
  #     quantity=15, move=1, pt=6)
  # else:
  #   print 'error, i did not recognize Unit typename. im giving it default stats.'
  #   new_unit = Unit(typename)
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
