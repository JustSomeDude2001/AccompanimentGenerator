from mido import MidiFile, MidiTrack, Message

from Chord import Chord
from Constant import *
from Individual import Individual


# A wrapper class for mido MidiFile.
class MidiFileWrapper:
    # Constructor only based on name of file.
    # Other constructors deprecated
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                self.filename = args[0]
                self.file = MidiFile(filename=self.filename, clip=True)
        self.file.type = 1
        # Double ticks_per_beat was determined as optimal for chord length of most songs.
        self.default_chord_duration = self.file.ticks_per_beat * 2

    # Obtains the lowest octave in the melody - so that it is easier to choose octave for accompaniment
    def get_melody_octave(self):
        _, melody, _ = self.get_track(MELODY_TRACK_INDEX)
        result = 1000
        for note in melody:
            octave = note // 12
            if octave < result:
                result = octave
        return result

    # Obtains expected length of accompaniment in milliseconds.
    def get_expected_length(self):
        length = 0
        track = self.file.tracks[MELODY_TRACK_INDEX]
        for i in range(len(track)):
            if not track[i].is_meta:
                length += track[i].time
        return length

    # Get track, melody, and timestamps of a specific MidiTrack in MidiFile
    def get_track(self, track_index: int):
        track: MidiTrack = self.file.tracks[track_index]
        notes = []
        start_times = []
        end_times = []
        time_counter = 0
        for message in track:
            time_counter += message.time
            if not message.is_meta:
                if message.type == 'note_on':
                    notes.append(message.note)
                    start_times.append(time_counter)
                elif message.type == 'note_off':
                    end_times.append(time_counter)
        timestamps = [[start_times[i], end_times[i]] for i in range(len(start_times))]
        # Normalizing timestamps for melody notes so that it is easier for evolutionary algorithm to handle.
        # Helps handle empty spaces in melody - chord is chosen as if chosen for the first playing note
        # after silence ends.
        timestamps[0][0] = 0
        for i in range(1, len(timestamps)):
            timestamps[i][0] = timestamps[i - 1][1]
            timestamps[i - 1][1] -= 1
        return track.copy(), notes, timestamps

    # Method adds track to midi file
    def add_track(self, track: MidiTrack):
        self.file.tracks.append(track)

    # Adds an Individual as an accompaniment track. Can take octave and volume(velocity) as optional arguments
    def add_individual_as_accompaniment(self, individual: Individual, velocity: int = 100, octave: int = 3):
        track = MidiTrack()
        self.add_track(track)
        for chord in individual.chords:
            self.add_chord(chord.on_octave(octave), velocity=velocity, track_index=ACCOMPANIMENT_TRACK_INDEX)

    # Add chord to the end of a track.
    def add_chord(self, chord: Chord, velocity=100, duration=-1, channel=0, track_index=ACCOMPANIMENT_TRACK_INDEX):
        # if duration is set to default, then default chord duration is used.
        if duration == -1:
            duration = self.default_chord_duration
        # Add tracks until desired index is reached
        while track_index >= len(self.file.tracks):
            self.file.tracks.append(MidiTrack())

        # Get reference for track
        track: MidiTrack = self.file.tracks[track_index]

        # Add simultaneous push of all keys in chord
        for note in chord.notes:
            track.append(Message('note_on', note=note, velocity=velocity, time=0, channel=channel))

        # Add the first release of a key after a specified chord duration
        track.append(Message('note_off', note=chord.notes[0], velocity=velocity, time=duration, channel=channel))

        # Add the other key releases right after the first one to make them simultaneous.
        for i in range(1, len(chord.notes)):
            track.append(Message('note_off', note=chord.notes[i], velocity=velocity, time=0, channel=channel))

    # Save file in the wrapper to a specified filename
    def save(self, filename: str):
        self.file.save(filename=filename)
