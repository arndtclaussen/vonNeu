# UI Guide
Building a web-based strategy game UI inspired by VS Code's layout. Here's a summary of the components and their functions:


# General structure
## Menu Bar
A horizontal bar at the top with menu items like "Admin" and "Help," providing access to game settings and information.

## Activity Bar
A vertical bar on the left with icons (or labels) representing different game views/activities. For the moment we only have:
* Probes
* Asteroids

Clicking an activity switches the content in the Side Bar and Main Area.

## Side Bar:
A panel to the right of the Activity Bar. Its content dynamically changes based on the selected activity. For example, clicking "Probes" shows all available probes in a list. While clicking "Asteroids" shows already located asteroids for further mining activties.

## Main Area (Editor Area):
The largest central area where the core game information and interactions are displayed. 


## Panels: 
Located below the Main Area. Initially, a "Game Logs" panel will display messages about game events.


# User Interaction Flow:
*  The player selects an activity from the Activity Bar.
* The Side Bar and Main Area update to display content relevant to the chosen activity.
* The player interacts with the game elements in the Main Area 
* Game events and updates are logged in the Game Logs panel.

