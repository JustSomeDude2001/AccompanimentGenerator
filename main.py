# Important abbreviations:
# COF - Circle of fifths. When you see "cof" appear in code, assume circle of fifths.

import os.path
import platform
import sys

from mido import MidiFile
from os import listdir
from Scale import *
from MidiFileWrapper import MidiFileWrapper
from Constant import *
from Individual import *
from Environment import Environment
from Population import Population


# Get midifile via a specific name. Deprecated, as using wrapper.
def get_file(filename):
    file = MidiFile(filename, clip=True)

    return file


# Get names of files in the music directory.
def get_midi_file_names(directory):
    result = []
    for filename in listdir(directory):
        if filename.endswith(".mid"):
            result.append(filename)
    return result


def generate_accompaniment(input_filename, output_filename,
                           count_generations, generation_size,
                           explain=False):
    # Extracting melody and building environment based on it
    filewrapper = MidiFileWrapper(input_filename)
    environment = Environment(filewrapper)
    # Determining how many chords are to be played
    track_length = filewrapper.get_expected_length()
    expected_chord_length = filewrapper.default_chord_duration
    expected_chord_amount = track_length // expected_chord_length
    if track_length % expected_chord_length > 0:
        expected_chord_amount += 1
    # Creating initial population
    population = Population(generation_size, expected_chord_amount)
    # Running the evolutionary algorithm
    for i in range(count_generations):
        population.prune(environment, int(generation_size * 0.25))
        population.populate_offspring(generation_size, 'intersect')
        # Not mutating last generation to preserve good tracks.
        if i < count_generations - 1:
            population.mutate(1)
    population.prune(environment, 1)
    filewrapper.add_individual_as_accompaniment(population.individuals[0], velocity=40,
                                                octave=filewrapper.get_melody_octave() - 1)
    filewrapper.save(output_filename)

    # Debug info
    if explain:
        print("Best individual fitness: ", environment.get_fitness(population.individuals[0]))
        _, notes, timestamps = filewrapper.get_track(1)
        print("Notes: ", notes)
        print("Durations: ", timestamps)
        print("Chord length: ", expected_chord_length)
        for i in range(7):
            print(environment.scale.consonant_chords[i].notes)
        for i in range(expected_chord_amount):
            note = environment.get_note_on_time(i * expected_chord_length)
            print("Note: ", note)
            print("Appropriate chords: ", end=" ")
            for chord in environment.scale.get_fitting_chords(note):
                print(chord.notes, end=" ")
            print()
            print(f"Chose: {population.individuals[0].chords[i].notes}")
            print(f"Is good: {environment.scale.follows_cof(note, population.individuals[0].chords[i])}")


def main():
    # Making required directories
    if not os.path.exists(MUSIC_DIRECTORY):
        os.mkdir(MUSIC_DIRECTORY)
    if not os.path.exists(INPUT_DIRECTORY):
        os.mkdir(INPUT_DIRECTORY)
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)
    # Parsing all provided inputs
    filenames = get_midi_file_names(INPUT_DIRECTORY)
    # Generating accompaniment for all inputs provided
    for filename in filenames:
        generate_accompaniment(os.path.join(INPUT_DIRECTORY, filename),
                               os.path.join(OUTPUT_DIRECTORY, "Output" + filename),
                               500, 300)


if __name__ == "__main__":
    main()
