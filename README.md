# Implementation of the Quixo board game
## Usage
It is recommended to use a virtual environment as shown below
```bash
git clone https://github.com/Elementrix08/quixo-ai.git
python3 -m venv .env
source .env/bin/activate
```
Install the required packages
```bash
pip install -r requirements.txt
```

Once these commands have been run the environment has been set up. Now run `main.py` with 
```python
python3 main.py
```
`main.py` will create a game via the `MatchManager` between you and the `Minimax` agent.

## User Interface
When playing via the GUI, the player simply has to hover any of the outer edge tiles which are their own shape or unturned and press one of the directional keys W, A, S, D which correspond to North, West, South, East respectively.

## Match Manager
Simply changing the object initialized to either agent1 or agent2 in `main.py` will match any two pairs of agents up together.

## Benchmarks
Within the stats folder, `benchmarks.py` runs a tournament between all currently implemented agents to get stats on the win, loss and draw rates of each agent.