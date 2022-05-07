from MidiFileWrapper import *
from Scale import *
from Individual import *


class Environment:
    def __init__(self, midifile_wrapper: MidiFileWrapper):
        self.file: MidiFileWrapper = midifile_wrapper
        self.track, self.melody, self.timestamps = self.file.get_track(MELODY_TRACK_INDEX)
        self.scale = Scale.scale_from_track(self.track)
        self.ticks_per_beat = midifile_wrapper.file.ticks_per_beat

    # Obtain note at a specific time.
    def get_note_on_time(self, time: int):
        for i in range(len(self.melody)):
            if self.timestamps[i][0] <= time <= self.timestamps[i][1]:
                return self.melody[i]
        return None

    # Check if note-chord combination follows COF
    def follows_cof(self, chord: Chord, time: int):
        note = self.get_note_on_time(time)
        return self.scale.follows_cof(note, chord)

    # Obtain fitness of individual
    def get_fitness(self, individual: Individual):
        fitness = float(0)
        is_cof_aligned = []
        # Metric 1: alignment with circle of fifths
        for i in range(len(individual.chords)):
            # Noting whether each chord is COF compliant
            if self.follows_cof(individual.chords[i], i * self.file.default_chord_duration):
                fitness += REWARD_ALIGNMENT_WITH_COF
                is_cof_aligned.append(True)
            else:
                is_cof_aligned.append(False)

        # Metric 2: local chord variation - discouraging monotone repetitiveness
        # Note that there is no reward in case of non COF aligned chords
        for i in range(len(individual.chords) - 1):
            if not is_cof_aligned[i] or not is_cof_aligned[i + 1]:
                continue
            cur_chord = individual.chords[i]
            next_chord = individual.chords[i + 1]
            if cur_chord != next_chord:
                fitness += REWARD_LOCAL_VARIETY

        # Metric 3: Tonics. There are specific chord progressions that are considered "good".
        # Let's detect them on COF compliant series of chords.
        for i in range(len(individual.chords)):
            for progression in CHORD_PROGRESSIONS:
                # Check that we can finish progression within track
                if i + len(progression) >= len(individual.chords):
                    continue

                # Check if all chords are COF aligned
                cof_aligned = True
                for j in range(i, i + len(progression)):
                    if not is_cof_aligned[j]:
                        cof_aligned = False
                        break
                if not cof_aligned:
                    continue

                # Check if chords fit the progression
                fits_progression = True
                for j in range(i, i + len(progression)):
                    chord = individual.chords[j]
                    if chord != self.scale.consonant_chords[progression[j - i]]:
                        fits_progression = False
                        break
                if fits_progression:
                    fitness += REWARD_PROGRESSION

        return fitness
