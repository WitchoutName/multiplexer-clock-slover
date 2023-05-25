from abc import ABC, abstractmethod


class IComponent(ABC):
    """Class defining the interface of components in the circuit."""
    @property
    @abstractmethod
    def output_pin(self) -> float:
        """In our current environment, every component should have exactly one data output pin"""
        pass


class Constant(IComponent):
    """A component representing a constant value. Can be used as an 'input pin' of the simulated circuit."""
    def __init__(self, value: float):
        self._value = value

    @property
    def output_pin(self) -> float:
        return self._value

    def __str__(self):
        return self.__class__.__name__


class AbstractComponent(IComponent):
    """Implementation of the IComponent interface. In our environment, all components have one general data
    input. (Multiplexer too has just one input, which it alters by its prescalers)"""
    def __init__(self, input_pin: IComponent = None):
        self._input_component = input_pin

    def set_input_component(self, input_component: IComponent):
        self._input_component = input_component

    def _output_logic(self):
        """Value returned by the output_pin method. Describes the functionality of the component."""
        return self._input_component.output_pin

    @property
    def output_pin(self) -> float:
        if not self._input_component:
            raise Exception(f"{self} doesn't have input_component set. Output invalid.")
        return self._output_logic()

    def __str__(self):
        return self.__class__.__name__


class Divider(AbstractComponent):
    """A component to be used as a prescaler for a multiplexer"""
    def __init__(self, divide_by: float, input_pin: IComponent = None):
        super().__init__(input_pin)
        self._divide_by = divide_by

    def _output_logic(self) -> float:
        return self._input_component.output_pin / self._divide_by


class Multiplexer(AbstractComponent):
    """A class representing a multiplexer with its prescaling components."""
    def __init__(self, prescalers: list[AbstractComponent], input_pin: IComponent = None):
        super().__init__(input_pin)
        self._prescalers = prescalers
        self._selected_index = 0

        self.setup_prescalers()

    def setup_prescalers(self):
        for prescaler in self._prescalers:
            prescaler.set_input_component(self._input_component)

    def select(self, index):
        self._selected_index = index

    def _output_logic(self) -> float:
        return self._prescalers[self._selected_index].output_pin

    @property
    def input_count(self):
        return len(self._prescalers)

    @classmethod
    def exponent_over_two(cls, n, input_component=None):
        """
        Factory method to create a multiplexer with prescalers values increasing exponentially.
        Example: n=4  ->  MUX with prescalers 1, 2, 4, 8
        """
        return cls([Divider(2**x) for x in range(n)], input_component)

    @classmethod
    def increment_one(cls, n, input_component=None):
        """
        Factory method to create a multiplexer with prescalers values increasing by one.
        Example: n=4  ->  MUX with prescalers 1, 2, 3, 4
        """
        return cls([Divider(x+1) for x in range(n)], input_component)
