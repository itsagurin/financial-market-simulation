"""Entry point for the financial market simulation application."""

from simulation import Simulation


def main() -> None:
    """Runs the financial market simulation and exports results to CSV."""
    sim = Simulation(total_epochs=20)
    sim.run()
    sim.export_csv("simulation_results.csv")


if __name__ == "__main__":
    main()
