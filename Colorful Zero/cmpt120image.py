# cmpt120image.py
# Some helper functions to wrap the Pygame image functions
# Supports laod+save for common image formats like PNG, JPG, and BMP
# Pre-requisite: Pygame and Numpy modules imported
# Authors: Angelica Lim, Victor Cheung
# Last update: 29 Oct, 2021

import pygame
import numpy


def getImage(filename):
    """
  Input: filename - string containing image filename to open
  Returns: 3d list of lists (a height-by-width-by-3 list)
  """
    image = pygame.image.load(filename)
    # do a transpose so its rows correspond to height of the image
    return pygame.surfarray.array3d(image).transpose(1, 0, 2).tolist()


def saveImage(pixels, filename):
    """
  Input:  pixels - 3d list of lists of RGB values (a height-by-width-by-3 list)
          filename - string containing filename to save image
  Output: Saves a file containing pixels
  """
    # do a transpose so its rows correspond to width of the image (used by Pygame)
    nparray = numpy.asarray(pixels).transpose(1, 0, 2)
    surf = pygame.surfarray.make_surface(nparray)
    (width, height, colours) = nparray.shape
    surf = pygame.display.set_mode((width, height))
    pygame.surfarray.blit_array(surf, nparray)
    pygame.image.save(surf, filename)


def showImage(pixels):
    """
  Input:  pixels - 3d list of list of RGB values (a height-by-width-by-3 list)
  Output: show the image in a window
  *this function uses the Pygame to display a window in a not-so-conventional way
  (without an event loop) so it might appear frozen.
  Suggested use: use it at the end of the program to show how the image looks like
  and make it stay by a this line:
  print("Press enter to quit")
  """
    # do a transpose so its rows correspond to width of the image (used by Pygame)
    nparray = numpy.asarray(pixels).transpose(1, 0, 2)
    surf = pygame.surfarray.make_surface(nparray)
    (width, height, colours) = nparray.shape
    # surf = pygame.display.set_mode((width, height))
    # pygame.surfarray.blit_array(surf, nparray)
    # for pixels2
    pygame.display.init()
    pygame.display.set_caption("CMPT120 - Image")
    screen = pygame.display.set_mode((width, height))
    screen.fill((225, 225, 225))
    screen.blit(surf, (0, 0))
    pygame.display.update()


def getBlackImage(width, height):
    """
  Input:  width - width of the image
          height - height of the image
  Output: 3d list of lists of a black image (a height-by-width-by-3 list)
  """
    return [[[0, 0, 0] for i in range(width)] for j in range(height)]
