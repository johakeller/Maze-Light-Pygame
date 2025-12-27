# Maze-Light-Pygame
![Visual Maze Light](code/docs/images/maze_light_visual.png)
*Screenshot showing gameplay.*

## Gameplay
*Maze Light* is a top-down maze game: Try to collect as many coins as possible, evade the souleaters and find the way through the maze to the ring. Your only defense is to turn the light off, but the souleaters will remember where you have been, if they have seen you, before you switched the light off. Collect flowers to increase your speed, to heal, and to expand the light radius. Be aware that the more you see, the more you are being seen. 

## Setup and start the game
1.  In the project root `Maze-Light-Pygame/` create a new virtual environment:
    ```bash
    python3 -m venv .venv
    ```
2.  Activate virtual environment:
    ```bash
    source .venv/bin/activate
    ```
3.  Install requirements:
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
4.  Go to the `Maze-Light-Pygame/code` directory. Start game via: 
    ```bash
    python main.py
    ```

## Controls
`LEFT`, `RIGHT`, `DOWN`, `UP` - moving the player,
`SPACE` - toggle light on/off


