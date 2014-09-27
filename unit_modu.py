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
    # TODO track allegiance as pointer to Army object, etc?
    self.allegiance = allegiance
    self.coord = [888,888]
    # most of these are pretty debug
    # later store wargear (or wargear stats), state, other stats from notes

  def printinfo(self):
    string = (
      "{coord} {name} x{quant}\n" +
      "    WS{ws} BS{bs} S{s} T{t} W{w} I{i} A{a} Ld{ld}, " +
      "{sv_type} save: {sv}, {pt} points each").format(
        coord=coordtostring(self.coord), name=self.name.capitalize(),
        quant=self.quantity, ws=self.ws, bs=self.bs, s=self.s, t=self.t,
        w=self.w, i=self.i, a=self.a, ld=self.ld,
        sv=save_to_string(self.sv), sv_type='armor', pt=self.pt)
    print string

  # TODO unused so far
  def sprite(self, charcount=3, colorkey='black'):
    return '\x1b[' + colordict[colorkey] + self.name[:charcount] + '\x1b[0m'  
    # untested

  # alternate way of storing: as Wargear and Unit or UnitProfile objects, 
  # constructed here at start. Positional constructors would mean not retyping 
  # 'ld' each time. But less readable i suppose.

def new(typename, allegiance='rebels'):
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

