import numpy as np
import numpy.linalg as la


"""------------------------Basic-Bilinear-Interpolation-Function(Scipy libraries can also be used)------------------ """
"""
check under alternative algorithm on
https://en.wikipedia.org/wiki/Bilinear_interpolation
for more details regarding the algorithm used.
"""


def bilinear_interpolate(x, y, x_grid, y_grid, F, ghost_cells):
  # x, y are the coordinates at which Interpolated fields have to found
  # x_grid and y_grid are the spatial grids for the field F used
  # F is the electric or magnetic field

  F_function = F

  n = len(F_function[0, :]) - 1 - 2 * ghost_cells  # number of zones

  x_zone = int(n * (x - x_grid[0]))  # indexing from zero itself
  y_zone = int(n * (y - y_grid[0]))

  # the 4*4 matrix for solving as mention in the wiki page
  A = np.matrix( \
                  [ [1, x_grid[x_zone], y_grid[y_zone], x_grid[x_zone] * y_grid[y_zone]], \
                    [1, x_grid[x_zone], y_grid[y_zone + 1], x_grid[x_zone] * y_grid[y_zone + 1]], \
                    [1, x_grid[x_zone + 1], y_grid[y_zone], x_grid[x_zone + 1] * y_grid[y_zone]], \
                    [1, x_grid[x_zone + 1], y_grid[y_zone + 1], x_grid[x_zone + 1] * y_grid[y_zone + 1]] \
                  ]\
               )

  # The 1D matrix for the points for interpolation
  point_to_calculated_for = np.matrix([[1], [x], [y], [x * y]])

  # Calculating the coefficient matrix
  b = (la.inv(A)).transpose() * point_to_calculated_for

  # assigning the values at the corner points at the grid cell

  Q11 = F_function[y_zone, x_zone]
  Q21 = F_function[y_zone, x_zone + 1]
  Q12 = F_function[y_zone + 1, x_zone]
  Q22 = F_function[y_zone + 1, x_zone + 1]

  Q = np.matrix([[Q11], [Q12], [Q21], [Q22]])

  # Calculating the interpolated value

  F_interpolated = b.transpose() * Q

  return F_interpolated


# Vectorizing the interpolator

bilinear_interpolate = np.vectorize(bilinear_interpolate, excluded=(['x_grid', 'y_grid', 'F']))

"""-------------------------------------------------------END--------------------------------------------------------"""