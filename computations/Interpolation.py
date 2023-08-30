import math
from array import array
import numpy as np


# Interpolator parent class
class Interpolator:
    def __init(self, x=[], y=[]):
        self.length = len(x)
        if self.length != len(y):
            raise ValueError('Warning: x and y coordinates must have the same length')
        
        temp = x.copy()
        temp.sort()
        if temp != x:
            raise ValueError('Warning: x coordinates must be in ascending order')
        
        self.x_coords = x
        self.y_coords = y

    def extend(self, x, y):
        self.x_coords.append(x)
        self.x_coords.sort()
        index = self.x_coords.index(x)
        self.y_coords.insert(index, y)
        self.length += 1

    def get_x_coordinates(self):
        return self.x_coords
    
    def get_y_coordinates(self):
        return self.y_coords
    
    def __len__(self):
        return self.length
    

# Piecewise Linear Interpolator
class PWL(Interpolator):

    def eval(self, x):
        if self.length == 0:
            print('This is an empty interpolator')
            return
        boolean_vector = []
        for x_coord in self.x_coords:
            if x <= x_coord:
                boolean_vector.append(True)
            else:
                boolean_vector.append(False)
        try:
            index = boolean_vector.index(True)
        except:
            print('Warning: extrapolating out of range')
            return self.x_coords[-1], self.y_coords[-1]
        
        if index == 0:
            return self.y_coords[0]
        else:
            alpha = (x - self.x_coords[index-1]) / (self.x_coords[index] - self.x_coords[index-1])
            return (1 - alpha) * self.y_coords[index-1] + alpha * self.y_coords[index]
    
    def delta(self, x, bump_index):
        if self.length == 0:
            print('This is an empty interpolator')
            return
        if bump_index >= self.length:
            raise ValueError('Warning: bump index out of range')
            return
        if self.length == 1:
            return 1
        boolean_vector = []
        for x_coord in self.x_coords:
            if x <= x_coord:
                boolean_vector.append(True)
            else:
                boolean_vector.append(False)
        try:
            index = boolean_vector.index(True)
        except ValueError:
            print('Warning: extrapolating out of range')
            if bump_index == self.length - 1:
                ret = 1
            else:
                ret = 0
            return ret
        
        if (index - 1) > bump_index or index < bump_index:
            return 0
        
        alpha = (x - self.x_coords[index-1]) / (self.x_coords[index] - self.x_coords[index-1])
        if bump_index == (index - 1):
            return 1 - alpha
        if bump_index == index:
            return alpha
        
    def copy_interpolator(self):
        copy = PWL(self.x_coords, self.y_coords)
        return copy
    

# Catmull-Rom Spline Interpolator
class CATMULL_ROM(Interpolator):
    def __init__(self, x=[], y=[]):
        super().__init__(x, y)
        self.coeff = []
        
        beta = (self.x_coords[1] - self.x_coords[0]) / (self.x_coords[2] - self.x_coords[0])

        beta_matrix = array('i', [0] * 4)

        beta_matrix[0] = (1 - beta) * self.y_coords[0] - self.y_coords[1] + beta * self.y_coords[2]
        beta_matrix[1] = (beta - 1) * self.y_coords[0] + self.y_coords[1] - beta * self.y_coords[2]
        beta_matrix[2] = self.y_coords[1] - self.y_coords[0]
        beta_matrix[3] = self.y_coords[0]

        self.coeff.append(beta_matrix.copy())

        loop_matrix = array('i', [0] * 4)

        for i in range(1, self.length-2):
            loop_alpha = (self.x_coords[i+1] - self.x_coords[i]) / (self.x_coords[i+1] - self.x_coords[i-1])
            loop_beta = (self.x_coords[i+1] - self.x_coords[i]) / (self.x_coords[i+2] - self.x_coords[i])

            loop_matrix[0] = -loop_alpha * self.y_coords[i-1] + (2 - loop_beta) * self.y_coords[i] + (loop_alpha - 2) * self.y_coords[i+1] + loop_beta * self.y_coords[i+2]
            loop_matrix[1] = 2 * loop_alpha * self.y_coords[i-1] + (loop_beta - 3) * self.y_coords[i] + (3 - 2 * loop_alpha) * self.y_coords[i+1] - loop_beta * self.y_coords[i+2]
            loop_matrix[2] = -loop_alpha * self.y_coords[i-1] + loop_alpha * self.y_coords[i+1]
            loop_matrix[3] = self.y_coords[i]

            self.coeff.append(loop_matrix.copy())

        alpha = (self.x_coords[-1] - self.x_coords[-2]) / (self.x_coords[-1] - self.x_coords[-3])

        alpha_matrix = array('i', [0] * 4)

        alpha_matrix[0] = -alpha * self.y_coords[-3] + self.y_coords[-2] + (alpha - 1) * self.y_coords[-1]
        alpha_matrix[1] = 2 * alpha * self.y_coords[-3] - 2 * self.y_coords[-2] + (2 - 2 * alpha) * self.y_coords[-1]
        alpha_matrix[2] = -alpha * self.y_coords[-3] + alpha * self.y_coords[-1]
        alpha_matrix[3] = self.y_coords[-2]

        self.coeff.append(alpha_matrix.copy())

    def eval(self, x):
        if self.length == 0:
            print('This is an empty interpolator')
            return

        boolean_vector = []
        for x_coord in self.x_coords:
            if x <= x_coord:
                boolean_vector.append(True)
            else:
                boolean_vector.append(False)
        try:
            index = boolean_vector.index(True)
        except ValueError:
            print('Warning: extrapolating out of range')
            return self.x_coords[-1], self.y_coords[-1]
        
        if index == 0:
            return self.y_coords[0]
        else:
            delta = (x - self.x_coords[index - 1]) / (self.x_coords[index] - self.x_coords[index - 1])
            return self.coeff[index-1][0] * delta**3 + self.coeff[index-1][1] * delta**2 + self.coeff[index-1][2] * delta + self.coeff[index-1][3]
        
    def delta(self, x, bump_index):
        pass

    def copy_interpolator(self):
        copy = CATMULL_ROM(self.x_coords, self.y_coords)
        return copy
    

# Natural Spline Interpolator
class NATURAL_SPLINE(Interpolator):
    def __init__(self, x=[], y=[]):
        super().__init__(x, y)

        lhs_matrix = np.zeros((self.length, self.length))
        lhs_matrix[0][0] = 1

        for i in range(1, self.length-1):
            lhs_matrix[i][i-1] = (self.x_coords[i] - self.x_coords[i-1]) / 6
            lhs_matrix[i][i] = (self.x_coords[i+1] - self.x_coords[i-1]) / 3
            lhs_matrix[i][i+1] = (self.x_coords[i+1] - self.x_coords[i]) / 6
        
        lhs_matrix[-1][-1] = 1
        rhs_array = np.zeros((self.length, 1))

        for i in range(1, self.length-1):
            rhs_array = (self.y_coords[i+1] - self.y_coords[i]) / (self.x_coords[i+1] - self.x_coords[i]) - (self.y_coords[i] - self.y_coords[i-1]) / (self.x_coords[i] - self.x_coords[i-1])

        self.fprime = np.linalg.solve(lhs_matrix, rhs_array)
    
    def eval(self, x):
        if self.length == 0:
            print('This is an empty interpolator')
            return
        boolean_vector = []
        for x_coord in self.x_coords:
            if x <= x_coord:
                boolean_vector.append(True)
            else:
                boolean_vector.append(False)
        try:
            index = boolean_vector.index(True)
        except ValueError:
            print('Warning: extrapolating out of range')
            return self.x_coords[-1], self.y_coords[-1]
        
        if index == 0:
            return self.y_coords[0]
        else:
            pos_x = self.x_coords[index] - x
            neg_x = x - self.x_coords[index-1]
            h_val = self.x_coords[index] - self.x_coords[index-1]
            ret = self.fprime[index-1] * pos_x**3 / h_val / 6 + self.fprime[index] * neg_x**3 / h_val / 6 \
                + (self.y_coords[index-1] / h_val - h_val * self.fprime[index-1] / 6) * pos_x + (self.y_coords[index] / h_val - h_val * self.fprime[index] / 6) * neg_x
            return ret
        
    def delta(self, x, bump_index):
        pass

    def copy_interpolator(self):
        copy = NATURAL_SPLINE(self.x_coords, self.y_coords)
        return copy