# Design Task

### Changing the bonus points again and allow more players to participate in a game
- This change to our code base would be a difficulty of 2.
- This change would not be too difficult because the bonus points score could be set in initialization with the use of if statements. We would also easily be able to change the number of players allowed in the game by changing the restriction of a max amount of players in the gameOver function and add a check in the begining of the referee function.

### Adding wildcard tiles
- This change would be a difficulty of 3
- This would impose a medium difficulty of 3. It is not difficult to account for a wildcard tile in terms of logic, the only difficulty is finding all places where tiles are compared or checked for validity and make sure wildcards are accounted for. Eg. (scoring points, checking placement validity, strategies, etc.)

### Imposing restrictions that enforce the rules of Qwirkle instead of Q.
- This change would be a difficulty of 4
- The task itself would be a matter of creating an abstract class of the game_state and implementing the rules of qwirkle in game_state. The same idea would go for the referee function. This task would be more tedious than difficult.