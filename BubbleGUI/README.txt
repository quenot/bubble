BubbleGUI

In case of any doubt, do not hesitate to send me a message: hugo.gonzalez1@etu.univ-grenoble-alpes.fr

The GUI allows the user to plot all the contours that were automatically computed for each image and delete the bubbles that are not pointing to any real bubble.

The program assumes that when you select a bubble image (png, jpg) there is a CSV file with the same name in the same folder with the information of the contours. Otherwise it will crash.

3 examples are provided with the code (img + csv): lv, lva, lvc.

Steps:

1) Launch the program.
2) Search for the image bubble and select it.
3) The program will automatically load the image, the CSV file with the contours info and it will display it on the screen.
4) Select a bubble with a left-click. It will turn red. If you click on it again it will be unselected.
   You can select more bubbles by clicking on them.
6) Once you have selected the bubbles you want to delete just press d. All the contours associated will disappear on the screen
7) If you think you committed a mistake, you can go back to the original contours by clicking on the button "original"
8) Once you have all the bubbles you want on the screen you can click on the button "Save Mask" to save a binary mask into the same folder

There are a lot of things to improve and to add to make this tool useful like:
Improve: The program selects the bubbles from the screen based on the closest center, so if you click on a blank space you will select the closest bubble.
Add: Select the bubbles that don't need to be deleted but recomputed. Then save those parameters to run the computational process again later.
Add: Save the final CSV with the contours parameters
Improve: The quality and size of the output mask could be improved
Improve: The program does not handle any kind of error, so it will crash in every case.
Improve: So far, there is no model to separate the model from the interface (like MVC).
Add: Change of image without having to close and open the program again
and many others...

