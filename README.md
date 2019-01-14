# framework3
PyGame based framework

In order to run the framework, create a Game object from Core.Game and call the start() method.
This should create a blank pygame window. In order to customize it, create a subclass that inherits from Game and implement your own game logic.

There are 4 phases:
1. Loading
2. Initalization
3. Game Loop
  3.1 Updating
  3.2 Drawing
4. Exiting (TBI)

## Loading (Core.Loader)
The Game object has a "resource" member which can be used to load and get resources. These include:
  1. Images
  2. Fonts (TBI)
  3. Audio (TBI)
  4. JSON Files (TBI)

In order to load a resource, call the specific load function. For example for images it is load_image(image_name, image_path). Every resource has a name, and a path.
The name is used to retrieve the resource, using get_image(image_name).

## Initialization
The game contains scenes, which are the basic wrapper class for all game logic. It currently handles GUI, Collision, and Actors.

## Game Loop
### Updating
Responsivle for component logic and catching  and handling events.
### Drawing
Draws stuff.

## Documentation
Should probably make one.
