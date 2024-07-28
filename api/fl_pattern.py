# patternNumber	-	int	Returns the current pattern number.	1
# patternCount	-	int	Returns the number of patterns.	1
# patternMax	-	int	Returns the maximum pattern number.	1
# getPatternName	int index	string	Returns the name of the pattern at "index".	1
# setPatternName	int index, string name	-	Changes the name of the pattern at "index" to "name".	1
# getPatternColor	int index	int	Returns the color of the pattern at "index".	1
# setPatternColor	int index, int color	-	Changes the color of the pattern at "index" to "color".	1
# getPatternLength	int index	int	Returns the length of the pattern at "index", in beats.	1
# getBlockSetStatus	int left, int top, int right, int bottom	int	Returns the status of the live block - Result is one of the LB_Status_Simplest option constants	1
# ensureValidNoteRecord	int index, (int playNow = 0)	-	Ensure valid note of the pattern at "index".	1
# jumpToPattern	int index	-	Jum to the pattern at "index"	1
# findFirstNextEmptyPat	int flags, (int x = -1), (int y = -1)	-	Find first empty pattern at position x, y	1
# Picker panel functions:
# isPatternSelected	int index	int	Returns True if patterns at "index" is selected in Picker panel.	2
# isPatternDefault	int index	int	Returns True if patterns at "index" is default (empty and unchanged by user).	23
# selectPattern	int index, (int value = -1), (int preview = 0)	-	Select pattern at "index" in Picker panel - value: -1 (toggle), 0 (deselect) 1 (select)
# preview: set to 1 to preview pattern	2
# clonePattern	(int index = -1)	-	Clone selected pattern(s), or clone panel specified by index (optional)	25
# selectAll	-	-	Select all patterns in Picker panel.	2
# deselectAll	-	-	Deselect all patterns in Picker panel.	2
# burnLoop	int index, (int storeUndo = 1), (int updateUi = 1)	-	Returns activity level for channel at "index" - Set Optional storeUndo to 0 to not store undo step.
# Set Optional updateUi to 0 to not update ui.
# 9
# Pattern groups:
# getActivePatternGroup		int	Returns the index of the currently selected pattern group.
# The default "All patterns" grouping has index -1. User-defined pattern groups have indexes starting from 0.	28
# getPatternGroupCount		int	Returns the number of user-defined pattern groups.
# The default "All patterns" grouping is not included.	28
# getPatternGroupName	index int	str	Returns the name of the pattern group at index.
# The default "All patterns" group's name cannot be accessed.	28
# getPatternsInGroup	int	tuple[int, ...]	Returns a tuple containing all the patterns in the group at index.
# The default "All patterns" group returns a tuple containing all the patterns that haven't been added to any other groups.


from dataclasses import dataclass
import patterns, channels
from fl_controller_framework.util.colors import ColorToRGB, BGRIntToRGB

@dataclass
class FLPattern:
    number: int
    name: str
    color: tuple[int, int, int]
    length: int

    @staticmethod
    def scroll_pattern(direction: int) -> "FLPattern":
        current_pattern = patterns.patternNumber()
        if direction > 0:
            if patterns.patternNumber() < patterns.patternMax():
                current_pattern = patterns.patternNumber() + 1
        elif direction < 0:
            if patterns.patternNumber() > 1:
                current_pattern = patterns.patternNumber() - 1
        patterns.jumpToPattern(current_pattern)
        return FLPattern.get_pattern(current_pattern)

    @staticmethod
    def get_pattern(pattern_number: int) -> 'FLPattern':
        return FLPattern(
            number=pattern_number,
            name=patterns.getPatternName(pattern_number),
            color=BGRIntToRGB(patterns.getPatternColor(pattern_number)),
            length=patterns.getPatternLength(pattern_number),
        )


class PatternEditor:
    """
    Represents a pattern editor in FL Studio.

    Attributes:
    - pModule: The patterns module.
    - cModule: The channels module.
    - number: The current pattern number.
    - length: The length of the current pattern.
    - cycles: A list of functions representing different cycle operations.

    Methods:
    - get_current_pattern(): Retrieves the current pattern number and length.
    - get_pattern_steps(channel_index): Retrieves the grid bits for a specific channel in the current pattern.
    - set_grid_bit(channel_index, step_index, value): Sets the grid bit at a specific channel and step index.
    - get_grid_bit(channel_index, step_index): Retrieves the grid bit at a specific channel and step index.
    - toggle_grid_bit(channel_index, step_index): Toggles the grid bit at a specific channel and step index.
    - set_nth_grid_bit(channel_index, nth): Sets the grid bit at every nth step for a specific channel.
    - set_all_grid_bits(channel_index): Sets all grid bits to 1 for a specific channel.
    - erase_all_grid_bits(channel_index): Sets all grid bits to 0 for a specific channel.
    - set_2nd_grid_bit(channel_index): Sets the grid bit at every 2nd step for a specific channel.
    - set_3rd_grid_bit(channel_index): Sets the grid bit at every 3rd step for a specific channel.
    - set_4th_grid_bit(channel_index): Sets the grid bit at every 4th step for a specific channel.
    - set_8th_grid_bit(channel_index): Sets the grid bit at every 8th step for a specific channel.
    - set_6th_grid_bit(channel_index): Sets the grid bit at every 6th step for a specific channel.
    - cycle(channel_index, cycle_index): Performs a cycle operation on a specific channel.
    """

    def __init__(self) -> None:
        self.pModule = patterns
        self.cModule = channels
        self.get_current_pattern()
        self.cycle_index = 0
        self.cycles = [1, 2, 3, 4, 6, 8, 10, 12, 16, 0]

    def get_current_pattern(self) -> int:
        """
        Retrieves the current pattern number and its length.

        Returns:
            int: The current pattern number.
        """
        self.number = self.pModule.patternNumber()
        self.length = self.pModule.getPatternLength(self.number)

    def get_pattern_steps(self, channel_index: int) -> list[bool]:
        """
        Retrieves the pattern steps for a specific channel.

        Args:
            channel_index (int): The index of the channel.

        Returns:
            list[bool]: A list of boolean values representing the pattern steps.
        """
        self.get_current_pattern()
        pattern_steps = []
        for step_index in range(self.length):
            grid_bit = self.pModule.getGridBit(channel_index, step_index)
            pattern_steps.append(grid_bit)
        self.current_pattern_steps = pattern_steps
        return pattern_steps

    def set_grid_bit(self, channel_index: int, step_index: int, value: bool) -> None:
        """
        Sets the value of a grid bit in the current pattern.

        Args:
            channel_index (int): The index of the channel.
            step_index (int): The index of the step.
            value (bool): The value to set for the grid bit.

        Returns:
            None
        """
        self.get_current_pattern()
        self.cModule.setGridBit(channel_index, step_index, int(value))

    def get_grid_bit(self, channel_index: int, step_index: int) -> bool:
        """
        Retrieves the grid bit value at the specified channel and step index.

        Args:
            channel_index (int): The index of the channel.
            step_index (int): The index of the step.

        Returns:
            bool: The grid bit value at the specified channel and step index.
        """
        self.get_current_pattern()
        return self.cModule.getGridBit(channel_index, step_index)

    def toggle_grid_bit(self, channel_index: int, step_index: int) -> bool:
        """
        Toggles the grid bit at the specified channel and step index.

        Args:
            channel_index (int): The index of the channel.
            step_index (int): The index of the step.

        Returns:
            bool: The new value of the grid bit after toggling.
        """
        self.get_current_pattern()
        grid_bit = bool(self.get_grid_bit(channel_index, step_index))
        self.set_grid_bit(channel_index, step_index, int(not grid_bit))
        return not grid_bit

    def set_nth_grid_bit(self, channel_index: int, nth: int) -> None:
        """
        Sets the grid bit for every nth index in the pattern for a specific channel.

        Args:
            channel_index (int): The index of the channel.
            nth (int): The interval at which to set the grid bit.

        Returns:
            None
        """
        self.get_current_pattern()
        for i in range(self.length):
            if nth <= 0:
                self.set_grid_bit(channel_index, i, 0)
            else:
                if i % nth == 0:
                    self.set_grid_bit(channel_index, i, 1)
                else:
                    self.set_grid_bit(channel_index, i, 0)

    def clear(self, channel_index: int) -> None:
        """
        Clears the grid bit at the specified channel index.

        Parameters:
        - channel_index (int): The index of the channel to clear.

        Returns:
        - None
        """
        self.reset_cycle()
        self.set_nth_grid_bit(channel_index, 0)

    def cycle(self, channel_index: int) -> int:
        """
        Performs a cycle operation on a specific channel.

        Args:
            channel_index (int): The index of the channel.

        Returns:
            int: The nth value of the cycle operation.
        """
        nth = self.cycles[self.cycle_index]
        self.set_nth_grid_bit(channel_index, nth)
        self.cycle_index = (self.cycle_index + 1) % len(self.cycles)
        return nth
    
    def reset_cycle(self) -> None:
        """
        Performs a cycle operation on a specific channel.

        Returns:
            None
        """
        self.cycle_index = 0
