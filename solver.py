import itertools
from dataclasses import dataclass
from components import Constant, Multiplexer


@dataclass
class MultiplexerEvaluation:
    """Class representing an evaluation of given configuration (selected indexes) of multiplexers"""
    multiplexers_config: tuple[int]  # a list of selected index of each multiplexer
    config_output: float  # the output value of the last MUX of the current configuration

    def get_delta(self, required_clock: float) -> float:
        """the difference between the required_clock and the output value of the last MUX"""
        return abs(required_clock - self.config_output)

    def __str__(self):
        res = ""
        for i, active_index in enumerate(self.multiplexers_config):
            res += f"Multiplexer {i+1} active input {active_index+1}\n"
        res += f"Achieved frequency: {self.config_output}\n"
        return res


@dataclass
class ClockSolver:
    clock_bus: float  # input clock frequency
    required_clock: float  # target clock frequency
    multiplexers: list[Multiplexer]  # list of multiplexers in the circuit

    def __post_init__(self):
        # set up of internal computing variables
        self.evaluations: list[MultiplexerEvaluation] = []
        self.initial_clock = Constant(self.clock_bus)

        self.setup_multiplexers()

    def setup_multiplexers(self):
        """Set the correct input component to each of the multiplexers."""
        for i, mux in enumerate(self.multiplexers):
            mux.set_input_component(self.multiplexers[i-1] if i > 0 else self.initial_clock)
            mux.setup_prescalers()

    def generate_configurations(self) -> list[tuple[int]]:
        # list of lists containing all indexes of given MUX
        all_mux_indexes = [list(range(mux.input_count)) for mux in self.multiplexers]
        # generate all possible combinations of MUX indexes -> configurations
        return list(itertools.product(*all_mux_indexes))

    def get_config_evaluation(self, config: tuple[int]) -> MultiplexerEvaluation:
        """Select the MUX inputs defined in the configuration and evaluate the resulting frequency"""
        for i, mux in enumerate(self.multiplexers):
            mux.select(config[i])
        return MultiplexerEvaluation(config, self.multiplexers[-1].output_pin)

    def solve(self) -> MultiplexerEvaluation:
        """Generate all possible combinations of MUX selected inputs, sord them based on their evaluation and return
         the best one."""
        configs = self.generate_configurations()
        for config in configs:
            # evaluate the configuration of multiplexers and save the result
            self.evaluations.append(self.get_config_evaluation(config))

        # sort the evaluations based on the similarity with the required clock
        sorted_evals = sorted(self.evaluations, key=lambda x: x.get_delta(self.required_clock))
        return sorted_evals[0]
