"""
This originally was a module for holding different ways to say 'Pants' and
'No Pants'. It has since expanded to handle all misc stuff that needs to be hard
coded
"""


Pants = {'en': ('No Pants', 'Pants'),
         'es': ('Pantalones', 'Sin Pantalones'),
         'fr': ('Pantalon', 'Pas De Pantalons'),
         'it': ('Pantaloni', 'Niente Pantaloni'),
         }


Genders = frozenset(['male',
                     'female', ])


Inclinations = frozenset(['warmer',
                          'neutral',
                          'cooler', ])
