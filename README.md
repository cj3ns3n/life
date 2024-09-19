The game of life is a classic computer simulation application. It has fasinated me since I was young.  I took some time and implemented my own.  I also wanted to experiment with [PyGame](https://www.pygame.org/news) and this seemed like a good opportunity (though I did try to make it modular so a different display framework could be used). 

Note: there are probably better options than PyGame for this, but it was just an experiment.\

## Overview

### Entities and Cells
The simulation is made of individual living "entity".  Each entity is assigned to a "cell".  Each cell has a different level of nutrients for the entity.  Entities can move to other cells if they are not doing well enough at their current cell and there is room.  Entities can mate if there is room for a child and they are healthy and neighboring a healthy mate of the opposite sex.

### Engine
The entity_engine is a simple loop that goes through all entities and updates their state based on the rules of the simulation.

### Display
The simulation uses PyGame to display a grid where every pixel displays an entity where the color is an indicator of the state of the entity (age, health, etc).  Various stats are overlayed on the display.  Various keys can be used to show or hide the stats and control the color mapping of the entities.

The simulation also produces output to the shell using curses.  Various stats and state and control information is displayed and updates with each iteration of the simulation.

