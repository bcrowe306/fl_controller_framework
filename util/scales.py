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
        
    
