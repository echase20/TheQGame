# Overview
### This file documents the content of Q/Common, which is the path containing programs relating to the Q game.
  
&nbsp;

# Sub-Paths
Q/Common is a single layer path. 

&nbsp;

# Files
This path contains the following files: 

- `game_state.py,`
which is the Python program that keeps track of all necessary data of the game (e.g. the map, the players, etc.) of the Q Game;

- `player.py,`
which contains the class that holds the data for an individual player for which the game state can access. It does not represent an actual player communicating with the game; 

- `xtest_game_state.py`,
the unit test for the integrated functionalities of the game state and the map.

- `map.py,`
which is the Python program that generates and stores all of the data in regards to the map of the Q game;

- `ShapeRenderer.py`,
which includes the class that visualizes the map's data;

- `xtest.py`,
the unit test for the functionalities of the map.

&nbsp;
# Milestone 3 - running xmap

Please refer to [the path containing xmap.py](https://github.khoury.northeastern.edu/CS4500-F23/sly-mice/tree/main/3/Tests) on further instructions in running xmap.

&nbsp;
# Milestone 3 - running xtest_game_state

To run xtest_game_state.py as a shell program, please use `make` prior to running to install the virtual Python environment and genearte then according, executable shell file. 

After this step, you will see a new file in the path named `xtest_game_state`. Please execute the file with the

~~~
./xtest_game_state
~~~
command.
 
&nbsp;
# Milestone 2 - running xtest
*Note: Makefile temporarily removed for milestone 3 to avoid confusion.

To run xtest.py as a shell program, please use `make` prior to running to install the virtual Python environment and genearte then according, executable shell file. 

After this step, you will see a new file in the path named `xtest`. Please execute the file with the

~~~
./xtest
~~~
command.

&nbsp;
# Cleaning filepath

To uninstall the virtual environment and remove the executable file, simply run `make clean`.
