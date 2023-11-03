Player-Referee Interaction Protocol
1. Initialization Phase:
~~~
The game is initialized by the referee.
Players are registered with the referee, and each player is assigned a unique player ID.
The game state is initialized with the map and other initial parameters.
~~~
2. Turn-Based Gameplay:
~~~
The game proceeds in turns, with players taking actions in a predefined order.
Players follow a turn order specified by the referee.
~~~
3. Player's Turn:
~~~
When it's a player's turn, the referee notifies the active player.
The active player receives the current game state, including the map, player states, and other relevant information.
The player formulates their action based on the current state and game rules.
~~~
4. Action Proposal:
~~~
The active player proposes an action, such as placing a tile or making a move.
The action should follow the game rules.
The action proposal is sent to the referee for validation.
~~~
5. Action Validation:
~~~
The referee checks the proposed action's validity:
Whether it adheres to the game rules.
Whether it's the correct player's turn.
Whether it's a legal move.
If the action is valid, it's executed; otherwise, the player is eliminated from the game.
~~~
6. Game State Update:
~~~
If the action is valid and executed, the game state is updated based on the action's outcome.
The map state is modified, player scores are updated, and other relevant changes are made.
~~~
7. Turn Transition:
~~~
After the action is completed, the referee updates the turn order.
The active player becomes the next player according to the predefined order.
~~~
8. Game Continues:
~~~
Steps 3 to 7 are repeated until the game's end conditions are met.
~~~
9. End of Game:
~~~
The referee checks for the end conditions, such as a winning condition or a draw.
When the game ends, the referee announces the winner or records a draw.
~~~
10. Game Over:
~~~
The game is officially over, and players are informed of the final result.
~~~
