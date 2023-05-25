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
