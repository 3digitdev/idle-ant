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



## TODOs

- Need an "info box" that can be used to display long text, better than a tooltip
- Need deprecation system laid out in code
- Need to add "Folding" system to deprecate old resources
- Need to give Upgrades more hierarchy
  - Upgrades that unlock new Producers should only be available after the other Upgrades are purchased


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
  Mining (unlocks `Miners` [Sticks + Stones + Land])
`Miners` gather Metal
Metal buys upgrades:
  Metal Tools (2x `Ants`/`Haulers`/`Miners` production [Food + Sticks + Metal])
  Metal Weapons (2x `Soldiers` production [Food + Sticks + Metal])
  Industrial Revolution (unlocks `Engineers` [Food + Land + Metal])
  ---
  Ore Processing (Folds `Haulers` into `Miners`)
`Engineers` gather Energy
Energy buys upgrades:
  Steam Power (2x `Soldiers` production [Food + Metal + Energy])
  ---
  Industrial Farming (Folds `Ants` into `Soldiers`)

## "Folding"
This is a way to deprecate old Resources/Producers.

You can purchase an Upgrade for a newer Producer.  This consumes all the Producers of the older
Resource to, and uses up all the old Resource they produced for a temporary boost to the new Producer

*NOTE:  If any upgrades remain with the old Resource in their cost, that resource is removed*

**TODO:** What rate do we convert old Resource to "Boosts" for?


- Popup toast message each time something is unlocked
  - Might need a queue of messages so a large group of unlocks doesn't spam the screen 
- "Prestige" is colonization of new planet.  Old planet(s) are "shipping" food to the new planet, providing the prestige multiplier


## Balance Notes

- Need land-based upgrade for Worker
- Less sticks cost for Quarry (3-4k)
- Swap costs of Wheel and Club
- Orange color for Producer names


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

Cost of first building:

Cursor: 15
Grandma: 100
Farm: 1100
Mine: 12000
Factory: 130000
Bank: 1400000
Temple: 20000000
Wizard Tower: 330000000
Shipment: 5100000000
Alchemy Lab: 75000000000
Portal: 1000000000000
Time Machine: 14000000000000
Antimatter Condenser: 170000000000000
Prism: 2100000000000000
Chancemaker: 26000000000000000
Fractal Engine: 310000000000000000
Javascript Console: 7100000000000000000
Idleverse: 120000000000000000000
