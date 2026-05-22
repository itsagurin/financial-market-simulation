"""Punkt wejściowy dla aplikacji symulacji rynku finansowego."""

from simulation import Simulation


def main() -> None:
    """Uruchamia symulację rynku finansowego i eksportuje wyniki do pliku CSV."""
    sim = Simulation(total_epochs=20)
    sim.run()
    sim.export_csv("simulation_results.csv")


if __name__ == "__main__":
    main()

