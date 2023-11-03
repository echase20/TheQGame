# Game-state Component Interface

The game-state component should implement the following interface:

## Properties

- `players`: An array of player objects representing the players in the game.
- `current_player`: The player object representing the player whose turn it currently is.
- `game_over`: A boolean indicating whether the game is over or not.

## Methods

- `start_game()`: Initializes the game state and starts the game.
- `end_game()`: Ends the game and sets the `game_over` property to `true`.
- `save_state()`: Saves the current state of the game to a file.
- `load_state()`: Loads a previously saved state of the game from a file.
- `next_turn()`: Advances the game to the next turn.

# Interaction Protocol Ref-GameState

The referee and game state components should interact according to the following protocol:

1. The referee component initializes the game state component by calling its `start_game()` method.

2. The referee component checks the `game_over` property of the game state component to determine if the game is over.

3. If the game is not over, the referee component retrieves the `current_player` property of the game state component to determine whose turn it is.

4. The referee component prompts the current player to make a move.

5. The current player proposes a move and the referee checks the validity of the move.

6. If the move is valid the referee updates the game state component accordingly.

7. The game state component updates the `current_player` property to the next player.

8. The game state component checks if the game is over and updates the `game_over` property accordingly.

9. The referee component repeats steps 2-7 until the game is over.

10. The referee component calls the game state component's `end_game()` method to end the game.

Note: The `save_state()` and `load_state()` methods can be used to save and load the game state to and from a file, respectively, but are not part of the interaction protocol between the referee and game state components.
