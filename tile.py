import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random

# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on this tile
      if random.randint(0, 9) > 5:
         self.number = 4
      else:
         self.number = 2
      # set the colors of this tile
      self.background_color = Color(151, 178, 199)  # background (tile) color
      self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      self.box_color = Color(0, 100, 200)  # box (boundary) color
      self.is_connected = False

   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      if self.number == 2:
         self.background_color = Color(239, 230, 221)
      elif self.number == 4:
         self.background_color = Color(239, 227, 205)
      elif self.number == 8:
         self.background_color = Color(245, 179, 127)
      elif self.number == 16:
         self.background_color = Color(247, 152, 107)
      elif self.number == 32:
         self.background_color = Color(247, 124, 90)
      elif self.number == 64:
         self.background_color = Color(247, 93, 59)
      elif self.number == 128:
         self.background_color = Color(239, 205, 115)
      elif self.number == 256:
         self.background_color = Color(239, 206, 99)
      elif self.number == 512:
         self.background_color = Color(239, 198, 82)
      elif self.number == 1024:
         self.background_color = Color(238, 198, 66)
      elif self.number == 2048:
         self.background_color = Color(239, 194, 49)
      else:
         self.background_color = Color(61, 58, 51)

      self.boundary_color = Color(188, 174, 161)
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

