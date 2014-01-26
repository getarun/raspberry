#/usr/bin/python
# -*- coding: utf-8 -*-
#
# parse Gcode
#

import sys
import re
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
import inspect
import math
import pygame
import time


class Point3d(object):
    """
    three dimension vetor representation
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.X = float(x)
        self.Y = float(y)
        self.Z = float(z)

    def __repr__(self):
        return("Point3d(%s, %s, %s)" % (self.X, self.Y, self.Z))

    def __str__(self):
        return("(%s, %s, %s)" % (self.X, self.Y, self.Z))

    def __add__(self, other):
        return(Point3d(self.X + other.X, self.Y + other.Y, self.Z + other.Z))

    def __iadd__(self, other):
        self.X += other.X
        self.Y += other.Y
        self.Z += other.Z

    def __sub__(self, other):
        return(Point3d(self.X - other.X, self.Y - other.Y, self.Z - other.Z))

    def __isub__(self, other):
        self.X -= other.X
        self.Y -= other.Y
        self.Z -= other.Z

    def __mul__(self, scalar):
        return(Point3d(self.X * scalar, self.Y * scalar, self.Z * scalar))

    def __imul__(self, scalar):
        self.X *= scalar
        self.Y *= scalar
        self.Z *= scalar

    def __div__(self, scalar):
        return(Point3d(self.X / scalar, self.Y / scalar, self.Z / scalar))

    def __idiv__(self, scalar):
        self.X /= scalar
        self.Y /= scalar
        self.Z /= scalar

    def length(self):
        return(math.sqrt(self.X**2 + self.Y**2 + self.Z**2))

    def unit(self):
        """
        return unit vector of self
        divide every element of self by length of self

        length of unit vector is always 1
        """
        length = self.length()
        return(Point3d(self.X / length, self.Y / length, self.Z / length))

    def product(self, other):
        """
        returns the cross product of self with other
        a = self
        b = other

        cx = ay * bz - az * by
        cy = az * bx - ax * bz
        cz = ax * by - ay * bx
        
        the returned vector is orthogonal to the plan a,b
        """
        cx = self.Y * other.Z - self.Z * other.Y
        cy = self.Z * other.X - self.X * other.Z
        cz = self.X * other.Y - self.Y * other.X
        return(Point3d(xy, cy, cz))

    def rotated_Z(self, theta):
        """
        return rotated version of self around Z-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        |cos θ   -sin θ   0| |x|   |x cos θ - y sin θ|   |x'|
        |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
        |  0       0      1| |z|   |        z        |   |z'|
        """
        xr = self.X * math.cos(theta) - self.Y * math.sin(theta)
        yr = self.X * math.sin(theta) + self.Y * math.cos(theta)
        zr = self.Z
        return(Point3d(xr, yr, zr))

    def rotated_Y(self, theta):
        """
        return rotated version of self around Y-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
        |   0      1       0| |y| = |         y        | = |y'|
        |-sin θ    0   cos θ| |z|   |-x sin θ + z cos θ|   |z'|
        """
        xr = self.X * math.cos(theta) + self.Z * math.sin(theta)
        yr = self.Y
        zr = (-1) * self.X * math.sin(theta) + self.Z * math.cos(theta)
        return(Point3d(xr, yr, zr))

    def rotated_X(self, theta):
        """
        return rotated version of self around X-Axis
        theta should be given in radians
        http://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
        |1     0           0| |x|   |        x        |   |x'|
        |0   cos θ    -sin θ| |y| = |y cos θ - z sin θ| = |y'|
        |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
        """
        xr = self.X
        yr = self.Y * math.cos(theta) - self.Z * math.sin(theta)
        zr = self.Y * math.sin(theta) + self.Z * math.cos(theta)
        return(Point3d(xr, yr, zr))

    def dot(self, other):
        """
        Dot Product of two vectors with the same number of items
        """
        return(self.X * other.X + self.Y * other.Y + self.Z * other.Z)

    def angle(self):
        """
        which angle does this vector has, from his origin
        """
        add_angle = 0
        # corect angle if in 3rd or 4th quadrant
        if self.Y < 0 :
            return(2 * math.pi - math.acos(self.X))
        else:
            return(math.acos(self.X))

    def angle_between(self, other):
        """
        angle between self and other vector
        """
        return(math.acos(self.dot(other)))
