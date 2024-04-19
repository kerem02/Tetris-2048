################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
import time # used for creating diffuculty settings

fall_delay = 0.5 # A global variable for fall delay, it is default by 0.5
is_paused = False # A global variable for pause game

# The main function where this program starts execution
def start():
   global fall_delay # declares global variable fall_delay in this function
   global is_paused # # declares global variable is_paused in this function
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
   # increase the size for scoreboard and showing the next piece
   canvas_w += 8 * 40
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   # added +7 to open space for scoreboard and showing the next piece
   stddraw.setXscale(-0.5, grid_w +8 - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)
   # record the current time to initialize the auto-fall timer for tetrominos
   last_fall_time = time.time()
   game_over = False # declaring game over variable False by default

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "up":
            # rotate the active tetromino
            current_tetromino.rotation(grid)
         elif key_typed == "space":
            while current_tetromino.move("down", grid):
            # performs hard drop action to tetromino
             pass
         elif key_typed == "p":
            is_paused = not is_paused
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      #check if the game is paused
      if is_paused:
         display_pause_message(grid_h, grid_w) # displays the pause text on screen
         continue

      if not is_paused:
         # capture the current time to check against the last fall time for auto-falling tetrominos
         current_time = time.time()
         # check if the auto fall interval has elapsed
         if current_time - last_fall_time > fall_delay:
            #attempt to move the current tetromino down
            success = current_tetromino.move("down", grid)
            #update the time of the last succesful fall
            last_fall_time = current_time
            # check if the tetromino could not move down
            if not success:
               # lock the current tetromino, indicating it cannot move anymore
               current_tetromino.is_locked = True
               # retrieve the minimal bounding matrix of the tetromino and its grid position
               tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
               # Lock the tetrominos tiles onto the game grid
               game_over = grid.update_grid(tiles, pos)
               #  check if the last tetromino landed over the border
               if game_over:
                  print("Game Over")
                  break
               # create a new tetromino
               current_tetromino = grid.update_tetromino()

      # display the game grid with the current tetromino
      grid.display()

   # print a message on the console when the game is over
   print("Game over")
# a function for "Paused" message
def display_pause_message(grid_h, grid_w):
   stddraw.setFontSize(45)
   stddraw.setFontFamily("Retro")
   stddraw.setPenColor(stddraw.WHITE)
   stddraw.text(grid_w / 2 - 0.6, grid_h / 2, "Paused")
   stddraw.show(100)

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z','S','T','J','L']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   global fall_delay # declares global variable fall_delay in this function
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/new_menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width + 7) / 2 , grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the buttons
   button_w, button_h = 5, 1.5
   # the coordinates of the "Easy", "Normal" and "Hard" buttons
   button_easy_x, button_easy_y = img_center_x - button_w / 2, 7
   button_normal_x, button_normal_y = img_center_x - button_w / 2, 5
   button_hard_x, button_hard_y = img_center_x - button_w / 2, 3
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_easy_x, button_easy_y, button_w, button_h)
   stddraw.filledRectangle(button_normal_x, button_normal_y, button_w, button_h)
   stddraw.filledRectangle(button_hard_x, button_hard_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Retro")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   # texts for the buttons
   text_easy = "EASY MODE"
   text_normal = "NORMAL MODE"
   text_hard = "HARD MODE"
   # draw the texts
   stddraw.text(img_center_x, 7.7, text_easy)
   stddraw.text(img_center_x, 5.7, text_normal)
   stddraw.text(img_center_x, 3.7, text_hard)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the buttons
         if mouse_x >= button_easy_x and mouse_x <= button_easy_x + button_w:
            if mouse_y >= button_easy_y and mouse_y <= button_easy_y + button_h:
               fall_delay = 1 # adjust the delay to 0.5 seconds for easy mode
               break
         if mouse_x >= button_normal_x and mouse_x <= button_normal_x + button_w:
            if mouse_y >= button_normal_y and mouse_y <= button_normal_y + button_h:
               fall_delay = 0.5 # adjust the delay to 0.5 seconds for normal mode
               break
         if mouse_x >= button_hard_x and mouse_x <= button_hard_x + button_w:
            if mouse_y >= button_hard_y and mouse_y <= button_hard_y + button_h:
               fall_delay = 0.05 # adjust the delay to 0.1 seconds for hard mode
               break


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()