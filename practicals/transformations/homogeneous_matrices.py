#!/usr/bin/env python
# encoding: utf-8
"""
This script introduces you to the use of the classes:
    HomogeneousMatrix

    The use of the plot method is illustrated.
    Finally, a Homogeneous matrix can be created by means of a RotationMatrix and a Vector.

@Time: July 2022
"""
import numpy as np
from artelib.rotationmatrix import Rx
from artelib.vector import Vector
from artelib.homogeneousmatrix import HomogeneousMatrix

if __name__ == "__main__":
    # Diferentes formas de crear una matriz homogénea
    T1 = HomogeneousMatrix()
    T1.plot('Identity HomogeneousMatrix', block=True)

    T2 = HomogeneousMatrix([[1, 0, 0, 0.5], [0, 1, 0, 0.7], [0, 0, 1, 0.8], [0, 0, 0, 1]])
    T2.plot('Transformation T2')

    print('Position: ', T2.pos())
    print('Rotation: ', T2.R())

    position = Vector([1, 2, 3])
    rotation_matrix = Rx(np.pi/4)
    T3 = HomogeneousMatrix(position, rotation_matrix)
    T3.plot('Transformation T3')

    T4 = T2*T3
    T4 = T4.inv()
    T4.plot('Transformation T4')

    # Transformar un vector
    u = Vector(np.array([1, 2, 3, 1]))
    u.plot('A 3D vector')
    u = T4*u.T()
    print(u)
    u.plot('A vector transformed by T4')


