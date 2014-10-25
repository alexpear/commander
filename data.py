#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

# data dicts about game rules, unit stats, etc 

# alternate way of storing: as Wargear and Unit or UnitProfile objects, 
# constructed here at start. Positional constructors would mean not retyping 
# 'ld' each time. But less readable i suppose. 
# Make readable with well labeled columns?

wargear_stats = {
  'combat knife' : { 'type': 'hand weapon'},
  'autopistol': {
    's': 3, 'ap': 7, 'range': 2, 'type': 'pistol', 'shots': 1
  },
  'autogun': {
    's': 3, 'ap': 7, 'range': 4, 'type': 'rapid fire', 'shots': 1
  },
  'autocannon': {
    's': 7, 'ap': 4, 'range': 6, 'type': 'heavy', 'shots': 2
  },
  'shotgun': {
    's': 3, 'ap': 7, 'range': 2, 'type': 'assault', 'shots': 2
  },
  'laspistol': {
    's': 3, 'ap': 7, 'range': 2, 'type': 'pistol', 'shots': 1
  },
  'lasgun': {
    's': 3, 'ap': 7, 'range': 4, 'type': 'rapid fire', 'shots': 1
  },
  'lascannon': {
    's': 9, 'ap': 2, 'range': 8, 'type': 'heavy', 'shots': 1
  },
  'hellpistol': {
    's': 3, 'ap': 5, 'range': 2, 'type': 'pistol', 'shots': 1
  },
  'hellgun': {
    's': 3, 'ap': 5, 'range': 4, 'type': 'rapid fire', 'shots': 1
  },
  'bolt pistol': {
    's': 4, 'ap': 5, 'range': 2, 'type': 'pistol', 'shots': 1
  },
  'boltgun': {
    's': 4, 'ap': 5, 'range': 4, 'type': 'rapid fire', 'shots': 1
  },
  'storm bolter': {
    's': 4, 'ap': 5, 'range': 4, 'type': 'assault', 'shots': 2
  },
  'heavy bolter': {
    's': 5, 'ap': 4, 'range': 6, 'type': 'heavy', 'shots': 3
  },
  'frags': { 'type': 'grenade' },
  'frag missile': {
    's': 4, 'ap': 6, 'range': 8, 'type': 'heavy', 'shots': 1, 'special': ['blast']
  },
  'krak missile': {
    's': 6, 'ap': 3, 'range': 8, 'type': 'heavy', 'shots': 1
  },
  'plasma pistol': {
    's': 6, 'ap': 3, 'range': 2, 'type': 'pistol', 'shots': 1, 'special': ['gets hot!']
  },
  'plasma gun': {
    's': 6, 'ap': 3, 'range': 4, 'type': 'rapid fire', 'shots': 1, 'special': ['gets hot!']
  },
  'plasma cannon': {
    's': 6, 'ap': 3, 'range': 6, 'type': 'heavy', 'shots': 1, 'special': ['gets hot!', 'blast']
  },
  'meltagun': {
    's': 8, 'ap': 1, 'range': 4, 'type': 'rapid fire', 'shots': 1
  },
  'multi-melta': {
    's': 8, 'ap': 1, 'range': 4, 'type': 'rapid fire', 'shots': 1
  },

  
  # 'A1 assault rifle'


}

# grouped by army list / codex
unit_stats = {
  'space marines': {
    'tactical marines': {
      'short_name': 'tact',
      'ws':4, 'bs':4, 's':4, 't':4, 'w':1, 'i':4, 'a':1, 'ld':8, 'sv':3,
      'wargear': ['boltgun', 'bolt pistol', 'combat knife', 'frags'],
      'type': 'infantry',
      'pt':16,
      'quantity': 10
    }

  },
  'astra militarum': {

  },
  'covenant': {
    
  }
}