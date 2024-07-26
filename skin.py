from abc import ABC, abstractmethod

class SkinColor(ABC):
  """
  Abstract base class for defining skin colors.

  Subclasses of `SkinColor` should implement the `draw` method to define how the control should be drawn with the
  specific color scheme.

  Attributes:
    None

  Methods:
    draw: Abstract method that should be implemented by subclasses to draw the control with the specific color scheme.
  """

  @abstractmethod
  def draw(self, control) -> None:
    """
    Abstract method that should be implemented by subclasses to draw the control with the specific color scheme.

    Args:
      control: The control object to be drawn.

    Returns:
      None
    """
    pass