TO: Co-CEO's of company

FROM: Angela Shen and Shivam Patel

DATE: September 27, 2023

SUBJECT: Referee Designs


&nbsp;

### <u>Data Representation:</u>

`Tile -> Map`

A `Tile` is an object that has two fields, color and shape. 

A `color` is one of: 
~~~
red, blue, green, orange, yellow, purple.
~~~
A `shape` is one of: 
~~~
circle, square, diamond, star, 8star, clover.
~~~

The `Map` is a 2D array, where each item in the array represents a space for a tile. The space can either be None, representing the lack of a tile, or a Tile object. The Map keeps track of all of the valid positions where a new tile can be placed. It also keeps track of where a tile can be placed based on the shape or color. The map generates the initial referee tile in the center of the grid. If a tile is placed on the edge of the map, the map automatically expands to accomodate for new tile placements. This ensures that the outer-most layer of the map will always be consisted of blank, None-type grids.

&nbsp;

### <u>Wish List</u>

### <strong>Tile</strong>
Fields:   
- Color - <i>Color of the shape within the tile </i>
- Shape - <i>Shape within the tile</i>


### <strong>Map</strong>
Fields:   
-  map - <i>A 2D array representing the map of the Q game.</i>

Methods:
- generate_tile: None -> Tile - <i>Returns a Tile object with random shapesand color.</i>
- generate_ref: None -> Tile - <i>Returns the referee tile, which is currently set as a red star for ease in testing. Places the tile in the center of the map.</i>
- expand: int, int -> None - <i>Takes in a row and column and expands the map toward the according directions if a tile is on the edge of the map.</i>
- place_tile_given: int, int, Tile -> None - <i>Places the given Tile at the given coordinate on the map. For testing purpose only.</i>
- place_tile: int, int -> None - <i>Invokes place_tile_given(). Places a randomly generated tile on the given coordinates.</i>
- valid_pos: Tile -> List of Str - <i>Takes in a Tile object and returns and print to stdout all possible coordinates the tile can be legally placed, according to Q game's rules, on the current map.</i>


### <strong>ShapeRenderer</strong>
Fields:   
- length - <i>Length of the display canvas</i>
- mid_point - <i>Midpoint of the canvas</i>
- padding - <i>The space between the edges of the shape and the canvas</i>
- corner - <i>Rightmost point of the triangle's coordinate</i>
- s_padding - <i> The space between the edges specifically for the star and 8star</i>

Methods:
- rotate: list-of-int, int, tuple of int - <i>Rotates the given list of coordinates by the given angle around the given center coordinate.</i>
- make_shape: str, str -> None - <i>Takes in a shape string and a color string and draws the according shape on the display canvas.</i>
- save_images: str -> None - <i>Takes in a filename and saves the current canvas as a png with the filename.</i>

