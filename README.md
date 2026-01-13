The game of life is a classic computer simulation application. It has fasinated me since I was young.  I took some time and implemented my own.  I also wanted to experiment with graphics frameworks and this seemed like a good opportunity (I made it modular so different display frameworks could be used). 

This implementation uses [Pyglet](https://pyglet.org/) for efficient OpenGL-based rendering.

![simulation screenshot](https://raw.githubusercontent.com/cj3ns3n/life/main/life-0001830.jpg)

## Overview

### Entities and Cells
The simulation is made of individual living "entity".  Each entity is assigned to a "cell".  Each cell has a different level of nutrients for the entity.  Entities can move to other cells if they are not doing well enough at their current cell and there is room.  Entities can mate if there is room for a child and they are healthy and neighboring a healthy mate of the opposite sex.

### Engine
The entity_engine is a simple loop that goes through all entities and updates their state based on the rules of the simulation.

### Display
The simulation uses Pyglet to display a grid where every pixel displays an entity where the color is an indicator of the state of the entity (age, health, etc).  Various stats are overlayed on the display.  Various keys can be used to show or hide the stats and control the color mapping of the entities.

The simulation also produces output to the shell using curses.  Various stats and state and control information is displayed and updates with each iteration of the simulation.
