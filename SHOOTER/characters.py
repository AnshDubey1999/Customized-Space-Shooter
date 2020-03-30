from graph import Graph
import random
import path_finding

class Zombie:
  #timer variable applies to all zombies
  timer = 0

  def __init__ (self, coordinates):
    #zombie's coordinates in relation to the 15 x 15 grid
    self.coordinates = coordinates

    # path of zombie to the player
    # is a list of vertices that the zombie must visit to get to player
    # is the shortest path to player
    self.path = []

    # keep track of the which vertex the zombie is currently at within
    # its path list
    self.currentpathindex = 0


  # calculates the path from zombie to player using breadth-first-search
  def path_to_player(self, playercoords, graph):
    reached = path_finding.breadth_first_search(graph, self.coordinates)
    self.path = path_finding.get_path(reached, self.coordinates, playercoords)
  
  # increases the current path index
  # called when the zombie has moved once
  def increasepathindex(self):
    self.currentpathindex += 1

  # class method that increases the all zombie's current timer by given 
  # value "increase"
  # is called every tick
  # when the zombie timer hits 30, zombie makes a move
  @classmethod
  def increasetimer(cls, increase):
    cls.timer += increase

  # retrieves the zombie's current timer
  @classmethod
  def gettimer(cls):
    return cls.timer

  # resets the zombie timer
  @classmethod
  def resettimer(cls):
    cls.timer = 0

# class that keeps track of the player's coordinates
class Player:
    def __init__ (self, coordinates):
        self.coordinates = coordinates

# function that respawns zombies in the outer 2 rings of the grid
def spawnzombies(zombielist, playercoords, graph):

  # list of values that correspond to the 2 outside rings of the 15 x 15 grid
  cornerrange = [0,1,13,14]

  # list of values of every possible coordinate within the 15 x 15 grid
  fullrange = []
  for i in range(15):
    fullrange.append(i)

  # keeps track of which zombie is currently being worked on
  zombieindex = 0

  for zombie in zombielist:
    # list for coordinates that already exist
    coordlist = []
    
    # initializes coordinate variable
    # pulls a random zombie coordinate that exists within existing zombies
    generatedcoordinate = random.choice(zombielist).coordinates

    for zombie in zombielist:

      # append the current zombie's coordinates to the coordinate list
      coordlist.append(zombie.coordinates)

      # keeps generating a random coordinate until 
      # a coordinate that does not currently exist is generated.
      while generatedcoordinate in coordlist:

        # randomly creates x coordinate from 0-15
        xcoord = random.choice(fullrange)
        ycoord = 0

        # if the x coordinate is 0, 1, 13, 14, 
        # the y coordinate can be any value from 0 - 15
        # this keeps the zombies from spawning on top of the player
        if xcoord < 2 or xcoord > 12:
          ycoord = random.choice(fullrange)

        # if the x coordinate in not currently on the first 2 of last 2 values of
        # the 15 x 15 grid, the y coordinate must be 0, 1, 13, 14 to keep
        # the zombie from spawning on top of the player
        else:
          ycoord = random.choice(cornerrange)

        # set up the coordinates into a tuple (zombie coordinates must be in tuple)
        generatedcoordinate = (xcoord, ycoord)
    # applies new coordinate to current zombie
    zombielist[zombieindex].coordinates = generatedcoordinate

    #calculates new path to player
    zombielist[zombieindex].path_to_player(playercoords, graph)

    # index increases to work on the next zombie
    zombieindex += 1
  return zombielist

# recalculates zombie's path to player
def recalculate_zombie_path(zombielist, player, graph):
  for zombie in zombielist:
    zombie.path_to_player(player.coordinates, graph)
    zombie.currentpathindex = 0

