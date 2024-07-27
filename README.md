# idle-ant
Idle Clicker TUI Game.  With Ants.


## INSTALLATION/USAGE

- **Requires Python 3.12**  Can get with `brew install python@3.12` on mac
- Create a virtual environment: `python3.12 -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `python -m pip install -r requirements.txt`
- Run the game: `textual run src/main.py`

## DEBUG SPEED-INCREASE

- In `src/game/game_state.py`, change the `DEBUG_MULTIPLIER` variable to a number greater than 1.0 to speed up the game
- This is useful for testing the game without waiting for the slow production rates
- **This will also multiply how many resources each click gets you**


## IDEAS

Click food
Food buys `Ants`
`Ants` gather food
First upgrade: Queen (unlocks `Workers` [Food], 2x `Ants` production)
`Workers` gather Sticks
Sticks buy upgrades:
  Stilts (unlocks `Haulers [Food + Sticks]`)
  Pack Frame (2x `Ants`/`Workers` production [Sticks])
Stilts unlock purchasing `Haulers` (Food + Sticks)
`Haulers` gather Stones
Stones buy upgrades:
  Wheels (2x `Workers`/`Haulers` production [Food + Sticks + Stones]) -- EXPENSIVE
  Clubs (unlocks `Soldiers [Food + Sticks + Stones]` [Sticks + Stones])
`Soldiers` gather Land (mm of land)
Land buys upgrades:
  Farming (2x `Ants` production [Food + Land])
  Quarry  (2x `Haulers` production [Sticks + Stones + Land])
  Outposts (2x `Soldiers` production [Food + Sticks + Land])
TODO:  WHAT NEXT?

- Popup toast message each time something is unlocked
  - Might need a queue of messages so a large group of unlocks doesn't spam the screen 
- "Prestige" is colonization of new planet.  Old planet(s) are "shipping" food to the new planet, providing the prestige multiplier


## Cookie Clicker Notes

0.15x scaling on costs
Upgrade scaling 1->5->10->100

Clicker: 0.1 cps
Grandma: 1 cps
Farm: 8 cps
Mine: 47 cps
Factory: 260 cps
Bank: 1400 cps
Temple: 7800 cps
Wizard Tower: 44000 cps
Shipment: 260000 cps
Alchemy Lab: 1600000 cps
Portal: 10000000 cps
Time Machine: 65000000 cps
Antimatter Condenser: 430000000 cps
Prism: 2900000000 cps
Chancemaker: 21000000000 cps
Fractal Engine: 150000000000 cps
Javascript Console: 1100000000000 cps
Idleverse: 8300000000000 cps

:)