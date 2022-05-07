class Chord:
    def __init__(self, *args):
        # A chord is initialized from a single list of notes. For Debug.
        if len(args) == 1:
            if isinstance(args[0], list):
                self.notes = args[0]
        # A chord is initialized using a root note and a chord template (list of offsets for root note)
        if len(args) == 2:
            if isinstance(args[0], int) and isinstance(args[1], list):
                self.root = (args[0] % 12)
                self.notes = [(args[0] + x) % 12 for x in args[1]]

    def __eq__(self, other):
        if len(self.notes) != len(other.notes):
            return False
        for i in range(len(self.notes)):
            if self.notes[i] % 12 != other.notes[i] % 12:
                return False
        return True

    def on_octave(self, octave):
        result = Chord([12 * octave + note for note in self.notes])
        result.root = self.root
        return result
