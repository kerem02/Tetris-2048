import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
from tetromino import Tetromino # used for showing next tetromino
import random
# A class for modeling the game grid
class GameGrid:
   # A constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles locked on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(45, 45, 45)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(80, 80, 80)
      self.boundary_color = Color(200, 200, 200)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.002
      self.box_thickness = 5 * self.line_thickness
      self.score = 0 # new variable for scoreboard
      self.next_tetromino = self.create_tetromino()

   def create_tetromino(self):
      # create a random tetromino
      types = ['I', 'O', 'Z', 'S', 'T', 'J', 'L']
      type = random.choice(types)
      return Tetromino(type)
   # set the next tetromino to current tetromino
   def update_tetromino(self):
      self.current_tetromino = self.next_tetromino
      self.next_tetromino = self.create_tetromino()
      return self.current_tetromino

   def draw_next_tetromino(self):
      base_x = self.grid_width + 0.7
      base_y = self.grid_height - 20
      grid_size = 4
      tile_size = 1.5

      # calcute size of tetromino
      tetromino_width = len(self.next_tetromino.tile_matrix[0])
      tetromino_height = len(self.next_tetromino.tile_matrix)

      # draw tetromino
      for row in range(tetromino_height):
         for col in range(tetromino_width):
            if self.next_tetromino.tile_matrix[row][col] is not None:
               draw_x = base_x + (col + (grid_size - tetromino_width) / 2) * tile_size + tile_size / 2
               draw_y = base_y + (grid_size - 1 - row - (grid_size - tetromino_height) / 2) * tile_size + tile_size / 2

               # fill the background of every cell with appropaite color
               if self.next_tetromino.tile_matrix[row][col].number == 2:
                  stddraw.setPenColor(Color(239, 230, 221))
               elif self.next_tetromino.tile_matrix[row][col].number == 4:
                  stddraw.setPenColor(Color(239, 227, 205))

               stddraw.filledSquare(draw_x, draw_y, tile_size / 2)

               # show number of the tile
               stddraw.setPenColor(Color(30, 30, 30))
               stddraw.text(draw_x, draw_y, str(self.next_tetromino.tile_matrix[row][col].number))

               # draw frame for each tile
               stddraw.setPenColor(Color(0, 0, 0))  # set frame color black
               stddraw.setPenRadius(0.005)  # thickness of frame
               stddraw.rectangle(draw_x - tile_size / 2, draw_y - tile_size / 2, tile_size, tile_size)

      # reset thickness
      stddraw.setPenRadius()

   # A method for displaying the game grid
   def display(self):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None
      # (the case when the game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid
      self.draw_boundaries()
      # draw scoreboard
      stddraw.setFontFamily("Retro")
      stddraw.setFontSize(60)
      stddraw.setPenColor(Color(255, 255, 255))
      score_text_x = self.grid_width + 3.5
      score_text_y = self.grid_height -3
      score_value_y = self.grid_height -5
      info_pause = self.grid_height -8
      stddraw.text(score_text_x, score_text_y, "SCORE")
      stddraw.text(score_text_x, score_value_y, str(self.score))
      stddraw.setFontSize(30)
      stddraw.text(score_text_x, info_pause, "P to pause")
      self.draw_next_tetromino()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(250)

   # A method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # if the current grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               # draw this tile
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the game grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method used checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

      #check if the row full
   def full_row_check(self, row):
      for col in range(self.grid_width):
         if self.tile_matrix[row][col] is None:
            return False
      return True
   #
   #a
   #add score counter here 
   #for every tile that we remove add its point to sum
   #   
   def remove_row(self, row):
      for col in range(self.grid_width):
         if self.tile_matrix[row][col] is not None:
            self.score += self.tile_matrix[row][col].number # compute the sum of numbers on removed tiles
         self.tile_matrix[row][col] = None
   #shift all rows down
   def shift_row(self, row):
      for r in range(row+1,self.grid_height):
         for col in range(self.grid_width):
            self.tile_matrix[r-1][col] = self.tile_matrix[r][col]
            self.tile_matrix[r][col] = None
   #gaher up all remove row functions
   def full_row_remove(self):
      for row in range(self.grid_height):
         while self.full_row_check(row):
            self.remove_row(row)
            self.shift_row(row)

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # A method that locks the tiles of a landed tetromino on the grid checking
   # if the game is over due to having any tile above the topmost grid row.
   # (This method returns True when the game is over and False otherwise.)
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the grid
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each tile (occupied cell) onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # return the value of the game_over flag
      self.merge()
      self.eliminate_floating_pieces()
      self.full_row_remove()
      return self.game_over

   # check merging for every column
   def merge(self):
      for col in range(self.grid_width):
         control = True
         while control:
            control = self.merge_control(col)

   # check and merge tiles on the same column from bottom to top
   def merge_control(self, col):
      for row in range(self.grid_height - 1):
         if self.tile_matrix[row][col] is not None and self.tile_matrix[row + 1][col] is not None:
            if self.tile_matrix[row][col].number == self.tile_matrix[row + 1][col].number:
               self.tile_matrix[row][col].number += self.tile_matrix[row][col].number
               self.score += self.tile_matrix[row][col].number
               self.tile_matrix[row + 1][col] = None
               for r in range(row + 1, self.grid_height - 1):
                  self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
               return True
      return False

   def free_piece_remove(self):
      for col in range(self.grid_width):
         for row in range(self.grid_height):
            if not self.free_piece_control(row, col):
               self.tile_matrix[row][col] = None

   # delete all floating pieces
   def eliminate_floating_pieces(self):
      self.check_connections()
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               if self.tile_matrix[row][col].is_connected == False:
                  self.score += self.tile_matrix[row][col].number
                  self.tile_matrix[row][col] = None
      self.check_connections()

   # check all the tiles if they are connected
   def check_connections(self):
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].is_connected = False
      # tiles at the ground are connected
      for col in range(self.grid_width):
         if self.tile_matrix[0][col] is not None:
            self.tile_matrix[0][col].is_connected = True
      for x in range(10):
         # check all the tiles above the ground to see if they're connected
         self.sweep()

   def sweep(self):
      # check all the tiles starting from bottom to top
      for row in range(1, self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               # check the below neighbor
               if self.tile_matrix[row - 1][col] is not None:
                  if self.tile_matrix[row - 1][col].is_connected == True:
                     self.tile_matrix[row][col].is_connected = True
      # check all the tiles form left to right
      for row in range(1, self.grid_height):
         for col in range(1, self.grid_width):
            if self.tile_matrix[row][col] is None:
               continue
            if self.tile_matrix[row][col - 1] is not None:
               if self.tile_matrix[row][col - 1].is_connected == True:
                  self.tile_matrix[row][col].is_connected = True
      # check all the tiles form right to left
      for row in range(1, self.grid_height):
         for col in range(self.grid_width - 2, -1, -1):
            if self.tile_matrix[row][col] is None:
               continue
            if self.tile_matrix[row][col + 1] is not None:
               if self.tile_matrix[row][col + 1].is_connected == True:
                  self.tile_matrix[row][col].is_connected = True