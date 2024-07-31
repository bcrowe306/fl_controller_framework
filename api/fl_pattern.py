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
