#!/usr/bin/python
# -*- coding: utf-8 -*-
# ? 

# data dicts about game rules, unit stats, etc 

wargear_stats = {
  'bolt pistol': {
    's': 4, 'ap': 5, 'range': 2, 'type': 'pistol', 'shots': 1
  },
  'boltgun': {
    's': 4, 'ap': 5, 'range': 4, 'type': 'rapid fire', 'shots': 1
  }
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

  }
}