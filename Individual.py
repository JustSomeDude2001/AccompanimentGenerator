from Chord import *
from Constant import *
import random


class Individual:
    # Constructor for individual requires different arguments depending on user intentions:
    #   type=random when need to generate a completely random individual
    #   type=splice when need to generate an individual via splicing 2 other individuals
    #       splicing_method=intersect to use the intersection splicing method, where
    #                       chords alternate between parents in origin
    #       parent_a, parent_b are the parents for splicing.
    def __init__(self, **kwargs):
        self.chords = []

        # Catching when type not specified
        if kwargs['type'] is None:
            raise Exception("No type of Individual class object constructor provided!")

        # Random individual
        if kwargs['type'] == 'random':
            for i in range(kwargs['size']):
                self.chords.append(Chord(random.randint(0, 12 - 1), random.choice(TRIADS)))

        # Spliced individual
        if kwargs['type'] == 'splice':
            parent_a: Individual = kwargs['parent_a']
            parent_b: Individual = kwargs['parent_b']

            if kwargs['splicing_method'] == 'intersect':
                for i in range(len(parent_a.chords)):
                    if i % 2 == 0:
                        self.chords.append(parent_a.chords[i])
                    else:
                        self.chords.append(parent_b.chords[i])

    # Mutation is required for a diverse population.
    # Magnitude determines how many chords in an individual are randomized.
    def mutate(self, magnitude):
        for i in range(magnitude):
            chord_index = random.randint(0, len(self.chords) - 1)
            self.chords[chord_index] = Chord(random.randint(0, 12 - 1), random.choice(TRIADS))
