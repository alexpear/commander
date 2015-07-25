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

  'a1 assault rifle': {
    's': 3, 'ap': 6, 'range': 3, 'type': 'rapid fire', 'shots': 1
  },
  'a3 assault rifle': {
    's': 3, 'ap': 7, 'range': 2, 'type': 'assault', 'shots': 2
  },
  'smg': {
    's': 3, 'ap': 7, 'range': 2, 'type': 'assault', 'shots': 2
  },
  'silenced smg': {
    's': 3, 'ap': 7, 'range': 3, 'type': 'rapid fire', 'shots': 1
  },
  'heavy pistol': {
    's': 4, 'ap': 5, 'range': 2, 'type': 'pistol', 'shots': 1
  },
  'battle rifle': {
    's': 4, 'ap': 5, 'range': 4, 'type': 'assault', 'shots': 1
  },
  'dmr': {
    's': 4, 'ap': 5, 'range': 4, 'type': 'assault', 'shots': 1
  },
  'shotgun': {
    's': 4, 'ap': 4, 'range': 2, 'type': 'assault', 'shots': 2
  },
  'saw': {
    's': 4, 'ap': 6, 'range': 3, 'type': 'assault', 'shots': 3
  },
  'sniper rifle': {
    's': 4, 'ap': 6, 'range': 2, 'type': 'heavy', 'shots': 1, 'special': ['sniper', 'pinning']
  },
  'lascannon': {
    's': 9, 'ap': 2, 'range': 8, 'type': 'heavy', 'shots': 1
  },
  'grenade launcher': {
    's': 5, 'ap': 4, 'range': 5, 'type': 'assault', 'shots': 1, 'special': ['blast']
  }

  

}

# grouped by army list / codex
unit_stats = {
  'space marines': {
    'tactical marines': {
      'short_name': 'tac',
      'ws':4, 'bs':4, 's':4, 't':4, 'w':1, 'i':4, 'a':1, 'ld':8, 'sv':3,
      'wargear': ['boltgun', 'bolt pistol', 'combat knife', 'frags'],
      'type': 'infantry',
      'pt':16,
      'quantity': 10
    },
    'assault marines': {
      'short_name': 'ass',
      'ws':4, 'bs':4, 's':4, 't':4, 'w':1, 'i':4, 'a':1, 'ld':8, 'sv':3,
      'wargear': ['bolt pistol', 'chainsword', 'combat knife', 'frags'],
      'type': 'jump infantry',
      'pt':22,
      'quantity': 10
    },
    'devastator marines': {
      'short_name': 'dev',
      'ws':4, 'bs':4, 's':4, 't':4, 'w':1, 'i':4, 'a':1, 'ld':8, 'sv':3,
      'wargear': ['lascannon', 'boltgun', 'combat knife', 'frags'],
      'type': 'infantry',
      'pt':26,
      'quantity': 4
    }
  },
  'astra militarum': {
    'cadets': {
      'short_name': 'cade',
      'ws':3, 'bs':3, 's':3, 't':3, 'w':1, 'i':3, 'a':1, 'ld':6, 'sv':6,
      'wargear': ['lasgun'],
      'type': 'infantry',
      'pt':6,
      'quantity': 20
    }
  },
  'unsc': {
    'marine platoon': {
      'short_name': 'marine',
      'ws':3, 'bs':3, 's':3, 't':3, 'w':1, 'i':3, 'a':1, 'ld':7, 'sv':5,
      'wargear': ['a3 assault rifle'],
      'type': 'infantry',
      'pt':7,
      'quantity': 10
    },
    'odst squad': {
      'short_name': 'odst',
      'ws':3, 'bs':4, 's':3, 't':3, 'w':1, 'i':3, 'a':1, 'ld':8, 'sv':4,
      'wargear': ['battle rifle'],
      'type': 'infantry',
      'pt':7,
      'quantity': 10
    }
  }
  # 'covenant': {
    
  # }
}