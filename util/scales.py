from .functions import limit_range
class Scales:
    chromatic: list[int] =[0,1,2,3,4,5,6,7,8,9,10,11]
    major: list[int] =[0,2,4,5,7,9,11]
    minor: list[int] = [0, 2, 3, 5, 7, 8, 10]
    melodic: list[int] = [0, 2, 3, 5, 7, 9, 11]
    harmonic: list[int] = [0, 2, 3, 5, 7, 8, 11]
    arabic: list[int] = [0, 2, 4, 5, 6, 8, 10]
    pentatonic: list[int] = [0, 2, 4, 7, 9]
    scale_strings: list[str] =  [
            "chromatic",
            "major",
            "minor",
            "melodic",
            "harmonic",
            "arabic",
            "pentatonic"
        ]
    notes_sharp: list[str] = [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ]

    notes_flat: list[str] = [
        "C",
        "Db",
        "D",
        "Eb",
        "E",
        "F",
        "Gb",
        "G",
        "Ab",
        "A",
        "Bb",
        "B",
    ]
    midi_octaves_length: int = 9

    def getMidiNote(octave_index: int, scale_degree: int) -> int:
        """
            Returns the midi_note: int, given an octave: int [0-10] and scale_degree: int [0-11]
        """
        octave_index = limit_range(octave_index, 0, Scales.midi_octaves_length)
        # scale_degree = limit_range(scale_degree, 0, 12)
        midiNote = (octave_index * 12) + scale_degree
        return  limit_range(midiNote, 0, 127)
    
    def getNoteIndexByNameSharp(key_name: str) -> int:
        return Scales.notes_sharp.index(key_name)

    def getNoteIndexByNameFlat(key_name: str) -> int:
        return Scales.notes_flat.index(key_name)

    def asList() -> list[list]:
        return [
            Scales.chromatic,
            Scales.major,
            Scales.minor,
            Scales.melodic,
            Scales.harmonic,
            Scales.arabic,
            Scales.pentatonic
        ]
    
    def getFromIndex(index: int) -> str:
        """
        Retrieves the scale string from the given index.

        Parameters:
        index (int): The index of the scale string to retrieve.

        Returns:
        str: The scale string at the given index.
        """
        return Scales.scale_strings[index]


class Chords:
    major: list[int] = [0, 4, 7]
    minor: list[int] = [0, 3, 7]
    diminished: list[int] = [0, 3, 6]
    augmented: list[int] = [0, 4, 8]
    sus2: list[int] = [0, 2, 7]
    sus4: list[int] = [0, 5, 7]
    major7: list[int] = [0, 4, 7, 11]
    minor7: list[int] = [0,3,7,10]
    dominant7: list[int] = [0, 4, 7, 10]
    diminished7: list[int] = [0, 3, 6, 9]
    augmented7: list[int] = [0, 4, 8, 10]
    major6: list[int] = [0, 4, 7, 9]
    minor6: list[int] = [0, 3, 7, 9]
    major9: list[int] = [0, 4, 7, 11, 14]
    minor9: list[int] = [0, 3, 7, 10, 14]
    dominant9: list[int] = [0, 4, 7, 10, 14]
    diminished9: list[int] = [0, 3, 6, 9, 14]
    augmented9: list[int] = [0, 4, 8, 10, 14]
    major11: list[int] = [0, 4, 7, 11, 14, 17]
    minor11: list[int] = [0, 3, 7, 10, 14, 17]
    dominant11: list[int] = [0, 4, 7, 10, 14, 17]
    diminished11: list[int] = [0, 3, 6, 9, 14, 17]
    augmented11: list[int] = [0, 4, 8, 10, 14, 17]
    major13: list[int] = [0, 4, 7, 11, 14, 17, 21]

    chords_strings: list[str] = [
        "major",
        "minor",
        "diminished",
        "augmented",
        "sus2",
        "sus4",
        "major7",
        "minor7",
        "dominant7",
        "diminished7",
        "augmented7",
        "major6",
        "minor6",
        "major9",
        "minor9",
        "dominant9",
        "diminished9",
        "augmented9",
        "major11",
        "minor11",
        "dominant11",
        "diminished11",
        "augmented11",
        "major13",
    ]
    @staticmethod
    def asList() -> list[list]:
        return [
            Chords.major,
            Chords.minor,
            Chords.diminished,
            Chords.augmented,
            Chords.sus2,
            Chords.sus4,
            Chords.major7,
            Chords.minor7,
            Chords.dominant7,
            Chords.diminished7,
            Chords.augmented7,
            Chords.major6,
            Chords.minor6,
            Chords.major9,
            Chords.minor9,
            Chords.dominant9,
            Chords.diminished9,
            Chords.augmented9,
            Chords.major11,
            Chords.minor11,
            Chords.dominant11,
            Chords.diminished11,
            Chords.augmented11,
            Chords.major13,
        ]

    @staticmethod
    def getFromIndex(index: int) -> str:
        """
        Retrieves the chord string from the given index.

        Parameters:
        index (int): The index of the chord string to retrieve.

        Returns:
        str: The chord string at the given index.
        """
        return Chords.chords_strings[index]
    @staticmethod
    def invertChord(chord: list[int], inversion: int) -> list[int]:
        """
        Inverts the given chord by the given inversion.

        Parameters:
        chord (list[int]): The chord to invert.
        inversion (int): The inversion to apply to the chord.

        Returns:
        list[int]: The inverted chord.
        """
        inversion = limit_range(inversion, 0, len(chord))
        for i, _ in enumerate(chord):
            if i < inversion:
                chord[i] += 12
        return chord

    @staticmethod
    def shift_chord(chord: list[int], shift: int = 0, inversion: int = 0) -> list[int]:
        """
        Shifts the given chord by the given shift.

        Parameters:
        chord (list[int]): The chord to shift.
        shift (int): The shift to apply to the chord.

        Returns:
        list[int]: The shifted chord.
        """
        new_chord = [note + shift for note in chord]
        new_chord = Chords.invertChord(new_chord, inversion)
        return new_chord
    @staticmethod
    def add_2(input_chord: list[int]) -> list[int]:
        new_chord = []
        for note in input_chord:
            new_chord.append(note)
        new_chord.append(2)
        return new_chord


class Progressions:
    # 1

    major_scale: list[list] = [
        Chords.major,
        Chords.shift_chord(Chords.minor, 2),
        Chords.shift_chord(Chords.minor, 4),
        Chords.shift_chord(Chords.major, 5),
        Chords.shift_chord(Chords.major, 7),
        Chords.shift_chord(Chords.minor, 9),
        Chords.shift_chord(Chords.diminished, 11),
    ]
    minor_scale: list[list] = [
        Chords.minor,
        Chords.shift_chord(Chords.diminished, 2),
        Chords.shift_chord(Chords.major, 3),
        Chords.shift_chord(Chords.minor, 5),
        Chords.shift_chord(Chords.minor, 7),
        Chords.shift_chord(Chords.major, 8),
        Chords.shift_chord(Chords.major, 10),
    ]   

    major_7th: list[list] = [ 
        Chords.major7,
        Chords.shift_chord(Chords.minor7, 2),
        Chords.shift_chord(Chords.minor7, 4),
        Chords.shift_chord(Chords.major7, 5),
        Chords.shift_chord(Chords.dominant7, 7),
        Chords.shift_chord(Chords.minor7, 9),
        Chords.shift_chord(Chords.diminished7, 11),
    ]
    major_musical = [
        (Chords.major),
        Chords.shift_chord(Chords.minor7, -10, inversion=3),
        Chords.shift_chord(Chords.major, inversion=1),
        Chords.shift_chord(Chords.add_2(Chords.major), 5),
        Chords.shift_chord((Chords.major), -5, inversion=2),
        Chords.shift_chord(Chords.minor7, -3, inversion=2),
        Chords.shift_chord(Chords.add_2(Chords.major), 7),
    ]

    minor_7th: list[list] = [
        Chords.minor7,
        Chords.shift_chord(Chords.diminished7, 2),
        Chords.shift_chord(Chords.major7, 3),
        Chords.shift_chord(Chords.minor7, 5),
        Chords.shift_chord(Chords.minor7, 7),
        Chords.shift_chord(Chords.major7, 8),
        Chords.shift_chord(Chords.dominant7, 10),
    ]
    pop_1: list[list] = [
        Chords.major,
        Chords.shift_chord(Chords.major, -5),
        Chords.shift_chord(Chords.minor, -3),
        Chords.shift_chord(Chords.major, -7),
    ]
    pop_1_7th: list[list] = [
        Chords.major7,
        Chords.shift_chord(Chords.add_2(Chords.major), -5, 1),
        Chords.shift_chord(Chords.minor7, -3),
        Chords.shift_chord(Chords.add_2(Chords.major7), -7),
    ]
    pop_2: list[list] = [
        Chords.shift_chord(Chords.minor7, -3),
        Chords.shift_chord(Chords.add_2(Chords.major9), -7),
        Chords.shift_chord((Chords.major),-12, inversion=3),
        Chords.shift_chord(Chords.add_2(Chords.major), shift=-5, inversion=1),
    ]
    pop_3: list[list] = [
        Chords.shift_chord(Chords.add_2(Chords.major), -7),
        Chords.shift_chord((Chords.major), -17, inversion=2),
        Chords.shift_chord(Chords.minor7, -15, inversion=2),
        Chords.shift_chord(Chords.add_2(Chords.major), shift=-12, inversion=1),
    ]
    pop_4: list[list] = [
        Chords.shift_chord(Chords.add_2(Chords.major), -5),
        Chords.shift_chord(Chords.minor7, -15, 2),
        Chords.shift_chord(Chords.add_2(Chords.major7), -7),
        Chords.shift_chord(Chords.add_2(Chords.major), shift=-12, inversion=2),
    ]
    pop_5: list[list] = [
        Chords.shift_chord(Chords.add_2(Chords.major7), -7),
        Chords.shift_chord(Chords.add_2(Chords.major), -5),
        Chords.shift_chord(Chords.minor7, -15, 2),
        Chords.shift_chord(Chords.add_2(Chords.major), -12, inversion=3),
       
    ]
    rb_1: list[list] = [
        [0, -7, 9, 4],
        [12, 7, -3, 4],
        [11, 2, -5],
        [0, -8, 2, 7],
        [-10, -3, 5],
        [-12, 4, -5],
        [-13, 2, -3, -5],
    ]
    rb_2: list[list] = [
        [-7, 0, 12, 9, 4, 19],
        [11, 12, 19],
        [19, 9, 2, -5],
        [19, -3, 4, 12, 7],
        [0, 19, 7, 12, 14],
    ]
    rb_3: list[list] = [
        [12, -3, 7, 4],
        [2, -5, 11],
        [-7, 0, 9],
        [-12, -5, 4],
        [-5, -13, 2],
    ]
    rb_4: list[list] = [
        [2, 5, 12, 16, 9],
        [-3, 11, 4, 7],
        [11, -1, -8, 7, 2],
        [0, -7, 4, 9],
    ]
    rb_5: list[list] = [
        [7, -8, 14, -1, 11],
        [-7, 0, 12, 7, 9, 16],
        [-1, 14, 7, 11, -8],
        [14, 11, 7, -3, 4],
        [-5, 2, 14, 10, 5],
    ]
    rb_6: list[list] = [
        [3, 0, -7, 12, 8, 7],
        [14, 5, 10, -5, 2],
        [0, 12, -4, 3, 7],
        [10, -12, 2, -5, 5],
    ]
    rb_7: list[list] = [
        [-7, 0, 12, 8, 3],
        [2, -5, 10, 14, 5],
        [-5, 10, 3, 14, 5, 0],
        [-9, 10, -2, 2, 7],
        [-8, 10, 13, 0, 4, 7],
    ]
    rb_8: list[list] = [
        [-1, 7, -12, -5, 4],
        [-7, 3, 0, 7, -4],
        [-4, 0, 3, 7],
        [10, -2, -5, 2, 5],
    ]
    rock_1: list[list] = [
        [0, 16, 4, 7, 12],
        [17, 2, 12, 9, 5],
        [-3, 7, 16, 4, 12],
        [0, 7, -7, 9, 12],
    ]
    rock_2: list[list] = [
        [-12, -5, 4, 7, 16],
        [-8, 16, -1, 7, 11],
        [-3, 16, 9, 12, 4],
        [-7, 16, 0, 7, 9, 12],
    ]
    rock_3: list[list] = [
        [-1, 4, -8, 11, 16, 7],
        [-7, 16, 9, 0, 12],
        [-5, 16, 2, 7, 11],
        [16, 12, 9, -3, 4],
    ]
    rock_4: list[list] = [
        [0, 4, 16, 7, 12],
        [-1, 2, 19, 11, 14, 7],
        [-2, 17, 5, 10, 14, 2],
        [-7, 0, 12, 7, 9, 5],
    ]
    rock_5: list[list] = [
        [-5, -12, 0, 12, 4, 7],
        [12, -2, 2, 5],
        [-10, 0, 9, 12, 5, -3],
        [-7, 0, 12, 5, 7, -3],
    ]
    rock_6: list[list] = [
        [-7, 0, 7, 12, 9, 5],
        [-12, -5, 4, 7, 12],
        [11, 2, -5, 7, -1],
        [-3, 0, 12, 7, 4],
        [11, -5, 2, 7, -1],
    ]
    rock_7: list[list] = [
        [0, 5, 12, 9, -7],
        [-5, -12, 12, 4, 7],
        [-3, 0, 12, 4, 7],
        [2, 7, 11, -1, -5],
    ]
    rock_8: list[list] = [
        [-3, 0, 4, 19, 7, 12],
        [19, 2, 11, -1, -5, 7],
        [-3, 19, 9, -7, 0, 12],
        [7, 12, 16, 0, 4],
        [-1, 2, 7, 11, 14],
    ]
    trap_1: list[list] = [
        [0, 15, 19, 12, 7],
        [0, 8, 7, 17, 14],
        [0, 15, 7, 12],
        [0, 8, 14, 5],
    ]
    trap_2: list[list] = [
        [3, 7, -4, 12, 15, 19],
        [10, -5, 2, 14, 19],
        [19, 0, 7, 14],
        [0, 8, 5, 17, 14],
    ]
    trap_3: list[list] = [
        [12, -7, 8, 0, 7],
        [0, 12, -5, 2, 7],
        [8, 5, 12, -7, 7, 0],
        [12, -5, 2, 7, -12],
    ]
    trap_4: list[list] = [
        [-4, 3, 12, 19],
        [-7, 0, 20, 14],
        [0, 2, 7, 19, 12],
        [5, -2, 22, 14],
    ]
    trap_5: list[list] = [
        [0, 12, 19, 15, 7],
        [0, 8, 17, 7, 14],
        [3, 0, 15, 7, 12],
        [-2, 2, 10, 5, 14],
        [-4, 3, 15, 19, 12],
        [-4, 3, 17, 10, 14],
        [-4, 15, 3, 12, 7],
        [14, 8, 5, -7, 0],
    ]
    trap_6: list[list] = [
        [-4, 3, 15, 12, 19],
        [-7, 7, 0, 12],
        [2, 17, 5, 12],
        [15, 7, 12, 0],
        [-2, 15, 10, 5],
    ]
    trap_7: list[list] = [
        [19, 10, 7, -5, 2],
        [3, -4, 19, 7, 12],
        [10, 2, -5, 19, 7],
        [-4, 3, 19, 12, 7],
        [10, -2, 17, 14, 5],
        [19, 10, 0, 7, 14],
    ]
    trap_8: list[list] = [
        [12, 7, 0, 24],
        [10, 2, 17, 24, 14, 5],
        [3, 8, 24, 15, 12, 19],
        [2, 24, 7, 14, 12, 19],
        [5, 24, 12, 19],
        [3, 15, 10, 24, 19],
        [2, 8, 20, 24, 14],
        [1, 24, 8, 17],
    ]

    progression_strings: list[str] = [
        "major_scale",
        "minor_scale",
        "major_7th",
        "major_musical",
        "minor_7th",
        "pop_1",
        "pop_1_7th",
        "pop_2",
        "pop_3",
        "pop_4",
        "pop_5",
        "rb_1",
        "rb_2",
        "rb_3",
        "rb_4",
        "rb_5",
        "rb_6",
        "rb_7",
        "rb_8",
        "rock_1",
        "rock_2",
        "rock_3",
        "rock_4",
        "rock_5",
        "rock_6",
        "rock_7",
        "rock_8",
        "trap_1",
        "trap_2",
        "trap_3",
        "trap_4",
        "trap_5",
        "trap_6",
        "trap_7",
        "trap_8",
    ]
    @staticmethod
    def asList() -> list[list]:
        return [
            Progressions.major_scale,
            Progressions.minor_scale,
            Progressions.major_7th,
            Progressions.major_musical,
            Progressions.minor_7th,
            Progressions.pop_1,
            Progressions.pop_1_7th,
            Progressions.pop_2,
            Progressions.pop_3,
            Progressions.pop_4,
            Progressions.pop_5,
            Progressions.rb_1,
            Progressions.rb_2,
            Progressions.rb_3,
            Progressions.rb_4,
            Progressions.rb_5,
            Progressions.rb_6,
            Progressions.rb_7,
            Progressions.rb_8,
            Progressions.rock_1,
            Progressions.rock_2,
            Progressions.rock_3,
            Progressions.rock_4,
            Progressions.rock_5,
            Progressions.rock_6,
            Progressions.rock_7,
            Progressions.rock_8,
            Progressions.trap_1,
            Progressions.trap_2,
            Progressions.trap_3,
            Progressions.trap_4,
            Progressions.trap_5,
            Progressions.trap_6,
            Progressions.trap_7,
            Progressions.trap_8,
        ]

    @staticmethod
    def getFromIndex(index: int) -> str:
        """
        Retrieves the progression string from the given index.

        Parameters:
        index (int): The index of the progression string to retrieve.

        Returns:
        str: The progression string at the given index.
        """
        return Progressions.progression_strings[index]
