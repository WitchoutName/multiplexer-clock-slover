# Clock Solver
This code provides a clock solver that helps find the best configuration for a circuit composed of multiplexers to achieve a specific target clock frequency. The solver uses a combination of prescalers and multiplexers to generate different output frequencies.
## Usage
To use the clock solver, you can create an instance of ClockSolver with the desired parameters and call the solve() method. The example below demonstrates how to use the solver:

```python
from components import Multiplexer
from solver import ClockSolver

def main():
    clock_bus = 16
    required_clock = 1

    solver = ClockSolver(clock_bus, required_clock, [
        Multiplexer.exponent_over_two(5),
        Multiplexer.increment_one(5),
    ])

    result = solver.solve()
    print(result)

if __name__ == '__main__':
    main()
```
In this example, the input clock frequency is set to 16, and the target clock frequency is set to 1. The solver is configured with two multiplexers: one with prescalers doubling the input frequency (exponent over two) and the other with prescalers incrementing by one. The solve() method is called to find the best configuration, and the result is printed.

