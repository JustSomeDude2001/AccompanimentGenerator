from mido import MidiTrack, Message

from Chord import Chord
from Constant import *

class Scale:
    # Makes scale from a root and a template
    def __init__(self, root, scale_type):
        self.root = root % 12
        self.notes = list([root])

        note_last = root
        for x in scale_type:
            self.notes.append((note_last + x) % 12)
            note_last += x

        # Gathering all consonant chords using the circle of fifths.
        self.consonant_chords = []

        self.consonant_chords.append(Chord((root + 0) % 12, TRIAD_MAJOR)) # I
        self.consonant_chords.append(Chord((root + 2) % 12, TRIAD_MINOR)) # II
        self.consonant_chords.append(Chord((root + 4) % 12, TRIAD_MINOR)) # III
        self.consonant_chords.append(Chord((root + 5) % 12, TRIAD_MAJOR)) # IV
        self.consonant_chords.append(Chord((root + 7) % 12, TRIAD_MAJOR)) # V
        self.consonant_chords.append(Chord((root + 9) % 12, TRIAD_MINOR)) # VI
        self.consonant_chords.append(Chord((root + 11) % 12, TRIAD_DIM))  # VII

    # Get a scale of a track
    @classmethod
    def scale_from_track(cls, track):
        for i in range(12):
            cur_scale = Scale(i, MAJOR_SCALE)
            if cur_scale.has_melody(track):
                return cur_scale
        return None

    # Check if a scale has a chord, e.g. all notes in chord are in scale
    def has_chord(self, chord: Chord):
        for noteChord in chord.notes:
            cur_note_on_key = False
            for noteKey in self.notes:
                if (noteChord - noteKey) % 12 == 0:
                    cur_note_on_key = True
                    break
            if not cur_note_on_key:
                return False
        return True

    # Check if a scale has a melody, e.g. all notes in melody are in scale
    def has_melody(self, melody: MidiTrack):
        for message in melody:
            if message.is_meta:
                continue
            if message.type != 'note_on':
                continue
            cur_note_on_key = False
            for scale_note in self.notes:
                if (message.note - scale_note) % 12 == 0:
                    cur_note_on_key = True
                    break
            if not cur_note_on_key:
                return False
        return True

    # Get chords of scale that fit the note per COF
    def get_fitting_chords(self, note: int):
        result = []
        for chord in self.consonant_chords:
            if chord.notes.count(note % 12) > 0:
                result.append(chord)
        return result

    # Check if a chord aligns with the note's scale per COF
    def follows_cof(self, note, chord):
        chords = self.get_fitting_chords(note)
        for good_chord in chords:
            if chord == good_chord:
                return True
        return False
