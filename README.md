# Serious Game - Epidemiological Simulation

    ## Description

This project is a serious game simulating the spread of a virus across different cities. The player can introduce the virus into a city and then mutate it in an attempt to infect and kill as many people as possible. 

    ## Installation

1. Clone the project
'''bash
git clone https://github.com/guigsrzde/Projet_apprentissage.git
cd Serious game - From Simulation to Decision
'''

2. Create and activate a virtual environment
'''bash
python -m venv env
source env/bin/activate 
'''

3. Install dependencies
'''bash
pip install -r requirements.txt
'''

    ## Usage

To launch the simulation, run:

'''bash
python main.py
'''

    ## Features

- Simulation of virus spread within a city
- Simulation of virus spread between cities
- Impact of mutations and symptoms on contagion
- Management of health interventions: vaccination
- Data visualization with graphs
- Visualization of the infected cities with red circles that turn green when city is infected
- Random events influencing epidemic dynamics


# Project Structure

bash
Project/
│── .env/                 # Virtual environment
│── royaume_uni/          # Contains files related to the UK simulation
│   ├── cities.py         # Defines cities and their characteristics
│   ├── map.png           # Map used for displaying cities
│── __pycache__/          # Python cache files (to ignore)
│── .gitignore            # File to ignore certain files in Git
│── city.py               # City class representing a city
│── gamedata.py           # Manages game data (turns, cities, virus, events)
│── global_UI.py          # Main user interface for the game
│── main.py               # Main file to start the game
│── modele_propagation.py # Models virus spread
│── graph_tab.py          # Manages the graphs tab
│── main_tab.py           # Manages the main tab
│── parser.py             # Parses data files
│── propagation.py        # Logic for infection spread
│── virus.py              # Defines the virus and its mutations
│── visuals_graphs.py     # Generates visual graphs
│── visuals.py            # Manages game visuals
│── requirements.txt      # Project dependencies