# Wildfire Propagation Modeling with Cellular Automata

This project was developed for the "Optimització" course in the Bachelor’s Degree in Artificial Intelligence at FIB (UPC). It explores the power of Cellular Automata (CA) to simulate complex natural phenomena, specifically the spread of wildfires in Mediterranean landscapes.

The project transitions from the theoretical foundations of 1D elementary automata to a high-fidelity 2D simulation that incorporates environmental heuristics and active suppression agents.

Key Features
- Wolfram Elementary CA: Implementation of 1D rules (e.g., Rule 30, 90, 110) to study emergent patterns.
- Multilayered Architectures: Systems where multiple rules interact via weighted combinations to model complex state transitions.
- Wildfire Simulation (Heuristic-based):
    * **Environmental Variables:** Integration of digital elevation models (slope), vegetation types (fuel), and humidity levels.
    * **Dynamic Propagation:** Fire spread probabilities based on wind and terrain.
    * **Active Agents:** Simulation of water bombers (airplanes) as active heuristics to mitigate fire spread.

The project is implemented in **Python** using a modular approach:
* `automata.py`: Core logic for 1D Wolfram automata.
* `automata2.py`: Implementation of multilayered and combined rule systems.
* `automata3.py`: The integrated simulation environment, including I/O functions for IDRISI spatial data files.
* `informe.pdf`: Full technical documentation, including the mathematical definition of heuristics and simulation analysis.

The model uses a grid-based approach where each cell $(i, j)$ transitions through states (Healthy, On Fire, Burnt, Water/Inert) based on:
1.  **Neighborhood State:** Influence of the 8 surrounding cells (Moore neighborhood).
2.  **Terrain Slope:** Fire spreads faster uphill.
3.  **Fuel Quality:** Different vegetation types have different ignition thresholds.
4.  **Suppression:** Active intervention by aerial units that "extinguish" cells based on priority heuristics.
├── docs/
│   └── final_report.pdf  # Detailed methodology and results
└── README.md
