# Rocket Sim

This is a genetic algorithm simulation of autonomous agents (rockets) navigating a 2D environment. The goal is for the population to evolve a trajectory that avoids obstacles and reaches a target coordinate within a fixed timeframe.

## Implementation Details

The project is designed with a strict separation of concerns between physics, data management, and the evolutionary engine.

*   **Physics Engine**: Uses NumPy for vectorized position and velocity updates. 
*   **Genetic Algorithm**: Implements single-point crossover and vectorized mutation masks for efficiency.
*   **Scoring**: Handled via a decoupled fitness evaluator that maps rocket instances to performance scores without polluting the entity classes.
*   **Rendering**: Handled by Pygame, abstracted from the core simulation logic to allow for headless execution if required.

## Project Structure

*   `constants.py`: Centralized configuration for environment dimensions, colors, and simulation parameters.
*   `rocket.py`: Definition of the rocket entity and physics update logic.
*   `game.py`: Management of the population, fitness scoring, and generational transitions.
*   `obstacle.py / reward.py`: Static environmental entities.
*   `main.py`: The entry point and primary simulation loop.

## Requirements

*   Python 3.x
*   NumPy
*   Pygame

## Usage

Run the simulation from the root directory:

```bash
python main.py
```

The simulation will execute indefinitely. Statistics regarding the current generation and best fitness scores are output to the terminal. To adjust the simulation speed or population size, modify the values in `constants.py`.


## Demo

![Demo Image](images/first-image.png)
