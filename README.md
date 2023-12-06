# The Q Game

The Q game is a spinoff of the board game Qwirkle. The Q Game involves 2-4 players who try to earn as many points as possible by placing their tiles. Each tile placement earns points and potentially bonus points by placing in contigious sequences, completing a Q or placing the rest of the players tiles. The game ends when either a player places all their tiles, all players in a round pass or exchange, or all players are kicked because of invalid moves.

## Run Game

To work on this project and run the program through a terminal one must use the command:
```
pip install -e .
```
This command allows for all of the dependices to reference each other, allowing the imports to work. 

There are a few scripts that one might wish to run to simulate some functionality during the game. <br>

- `xgames` in /7 which simualtes a game with some players.
- `xgames-with-observer` in /8 which simualtes a game with some players and an observer GUI if you wish by using the --show command.
- `xbaddies` in /9 which simulates a game with some good behaving players and some not so nice players that attempt to cheat. 
- `xclients` and `xserver` in /10 simulates a server client relationship over TCP between the referee and the players. 

<p> For all the scripts above, there is examples of input into the script in their respective /Tests/ folder. 
