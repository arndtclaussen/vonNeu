This files describes the target UI:

You're building a web-based strategy game UI inspired by VS Code's layout. Here's a summary of the components and their functions:

Title Bar: Handled by the browser, displays game name.

Menu Bar: A horizontal bar at the top with menu items like "Admin" and "Help," providing access to game settings and information.

Activity Bar: A vertical bar on the left with icons (or labels) representing different game views/activities, such as "Space," "Heaven," "Resources," "Research," and "Engineering." Clicking an activity switches the content in the Side Bar and Main Area.

Side Bar: A panel to the right of the Activity Bar. Its content dynamically changes based on the selected activity. For example, clicking "Space" might display a star map, while clicking "Research" shows available technologies.

Main Area (Editor Area): The largest central area where the core game information and interactions are displayed. This could include a game map, unit information, resource displays, or other relevant data, potentially organized with tabs.

Panels: Located below the Main Area. Initially, a "Game Logs" panel will display messages about game events.

User Interaction Flow:

The player selects an activity from the Activity Bar.
The Side Bar and Main Area update to display content relevant to the chosen activity.
The player interacts with the game elements in the Main Area (e.g., moving units, managing resources, conducting research).
Game events and updates are logged in the Game Logs panel.
This structure provides a clear, organized layout that allows players to easily navigate and manage different aspects of their strategy game. The VS Code-inspired design leverages a familiar interface paradigm, potentially enhancing user intuitiveness and experience.

