TO: Co-CEO's of company

FROM: Angela Shen and Shivam Patel

DATE: September 14, 2023

SUBJECT: The Plan   

## Sprint 1:

The first step to turn this vision of the game into reality will be to set up the tile and referee classes. The tile class will hold all of the different tiles that can be used in the game. The referee class will hold the rules of the game and the creation of the board as well as placement of tiles. The referee is important because it holds the logic of the game, so we know tht the game is running correctly when we test. We will also create a visual alongside the game in order to visualize the changes we make; this will make it easier to debug and add more features. Lastly, we will be able to generate a certain set of tiles to test if the logic of the game is correct.

## Sprint 2:

The second sprint includes creating the player component that will be able to play the game. This component will have to communicate with the referee component to ensure the game is being played fairly. We will implement the referee checking the input of the player to make sure they are making valid moves. It makes sense to make sure that the logic of the game is correct before adding players to the game, which is why this is in the second sprint.


## Sprint 3:

After we create a solid communication between the referee and the player, we can set up a valid scoring system based on the players moves. We will also ensure that the board and visual is updating with the player input. Lastly, we will ensure all test edge cases are accounted for and that the game will end when a certain state is reached based on the rules of the game.
