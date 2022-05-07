MUSIC_DIRECTORY = "./songs/"
INPUT_DIRECTORY = "./songs/input/"
OUTPUT_DIRECTORY = "./songs/output/"

# All triad chords.
TRIAD_MINOR = [+0, +3, +7]
TRIAD_MAJOR = [+0, +4, +7]
TRIAD_SUS2 = [+0, +2, +7]
TRIAD_SUS4 = [+0, +5, +7]
TRIAD_DIM = [+0, +3, +6]

TRIADS = [TRIAD_DIM, TRIAD_MAJOR, TRIAD_MINOR]#, TRIAD_SUS4, TRIAD_SUS2]

MAJOR_SCALE = [+2, +2, +1, +2, +2, +2, +1]
MINOR_SCALE = [+2, +1, +2, +2, +1, +2, +2]

CIRCLE_OF_FIFTHS = [[0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5],  # TRIAD_MAJOR
                    [9, 4, 11, 6, 1, 8, 3, 10, 5, 0, 7, 2],  # TRIAD_MINOR
                    [11, 6, 1, 8, 3, 10, 5, 0, 7, 2, 9, 4]]  # TRIAD_DIM

MELODY_TRACK_INDEX = 1 # Per examples, it is expected for all files provided to be the 2nd track in file.
ACCOMPANIMENT_TRACK_INDEX = 2

# All individuals are rewarded for fitness on the below characteristics
REWARD_ALIGNMENT_WITH_COF = 1.5
REWARD_LOCAL_VARIETY      = 0.1
REWARD_PROGRESSION        = 0.5

# Commonly used progressions are considered conventionally good-sounding. Hence, they are to be detected and rewarded.
CHORD_PROGRESSIONS = [[0, 4, 5, 3], #I - V - VI - IV   Popular
                      [1, 4, 0],    #II - V - I        Jazzy
                      [1, 6, 0],    #II - VII - I      Jazzy
                      [0, 3, 1, 4], #I - IV - II - V   Montgomery-Ward Bridge. Jazzy
                      [5, 1, 3, 0], #VI - II - V - I   Circle Progression. Popular
                      [2, 6, 0, 4], #III - VII - I - V Romanesca.
                      [0, 5, 1, 4], #I - VI - II - V   Popular.
                      [3, 4, 2, 5]  #IV - V - III - VI Royal Road progression. J-Pop
                     ]

