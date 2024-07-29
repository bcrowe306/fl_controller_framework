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
