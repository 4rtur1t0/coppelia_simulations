#!/usr/bin/env python
# encoding: utf-8
"""
Please open the scenes/irb140_palletizing_color.ttt scene before running this script.

Use the camera on the robot arm to detect a color using a simple image processing.
The mean color of the image is returned and compared to pure colors.
A simple classification in RGB is then used to place the pieces in three main destinations (without any order)

Please: beware that increasing the image resolution may lead to a slow execution.

@Authors: Arturo Gil
@Time: April 2022
"""
import numpy as np
from artelib.euler import Euler
from artelib.path_planning import compute_3D_coordinates
from artelib.vector import Vector
from artelib.homogeneousmatrix import HomogeneousMatrix
from robots.abbirb140 import RobotABBIRB140
from robots.grippers import SuctionPad
from robots.objects import get_object_transform
from robots.proxsensor import ProxSensor
from robots.simulation import Simulation
from robots.camera import Camera


def find_color(robot, camera, piece_index):
    """
    Places the camera on top of the piece.
    Saves the image for inspection.
    Computes the image to get the mean RGB value and the color name (red, green, blue).
    """
    T_piece = get_object_transform(clientID=robot.clientID, base_name='Cuboid', piece_index=piece_index)
    # leer la posición de la pieza
    p_piece = T_piece.pos()
    to = Euler([np.pi/2, -np.pi, 0])
    # position and orientation so that the camera sees the piece
    tp1 = p_piece + np.array([0.0, 0.1, 0.2])
    tp2 = p_piece + np.array([0.0, 0.1, 0.3])
    robot.show_target_points([tp1], [to])
    robot.moveJ(target_position=tp1, target_orientation=to)
    # captures an image and returns the closest color
    print('get_image')
    color = camera.get_color_name()
    robot.moveJ(target_position=tp2, target_orientation=to)
    return color


def pick(robot, gripper, piece_index):
    """
    Picks the piece from the conveyor belt.
    """
    # Esta función devuelve una matriz de transformación de la pieza
    T_piece = get_object_transform(clientID=robot.clientID, base_name='Cuboid', piece_index=piece_index)
    piece_length = 0.08
    p_piece = T_piece.pos()
    o_piece = T_piece.euler()[0]
    # ángulo de giro de la pieza sobre el eje Z (yaw)
    o_piece = o_piece.abg[2]

    # robot.moveAbsJ(q0, precision=False)
    # use gripper.open para soltar la pieza
    # gripper.open(precision=False)
    # robot.moveJ(...)
    # robot.moveL()
    # use gripper.close para asir la pieza
    # gripper.close(precision=False)



def place(robot, gripper, color, color_indices):
    # define que piece length and a small gap
    piece_length = 0.08
    piece_gap = 0.005

    if color == 'R':
        # defina T0m para las piezas rojas
        piece_index = color_indices[0]
    elif color == 'G':
        # defina T0m para las piezas verdes
        piece_index = color_indices[1]
    else:
        piece_index = color_indices[2]
        # defina T0m para las piezas azules

    # POSICION DE LA PIEZA i EN EL SISTEMA MÓVIL m (RELATIVA)
    pi = compute_3D_coordinates(index=piece_index, n_x=2, n_y=3, n_z=4, piece_length=piece_length, piece_gap=piece_gap)
    # POSICION p0 INICIAL SOBRE EL PALLET
    p0 = pi + np.array([0, 0, 2.5 * piece_length])
    # Defina una matriz Tmp relativa usando p0 y una orintación

    # CALCULE LA TRANSFORMACION TOTAL
    T0 = T0m*Tmp

    # Para mostrar los target points
    robot.show_target_points([T0.pos()], [T0.R()])
    robot.show_target_points([T1.pos()], [T1.R()])

    # ejecute los movimientos especificando los target points
    # robot.moveAbsJ(q0, precision=False)
    # robot.moveJ(...)
    # robot.moveL()
    # gripper.open(precision=True)
    # robot.moveL


def pick_and_place():
    simulation = Simulation()
    clientID = simulation.start()
    robot = RobotABBIRB140(clientID=clientID)
    robot.start()
    conveyor_sensor = ProxSensor(clientID=clientID)
    conveyor_sensor.start()
    camera = Camera(clientID=clientID)
    camera.start()
    gripper = SuctionPad(clientID=clientID)
    gripper.start()
    robot.set_TCP(HomogeneousMatrix(Vector([0, 0.065, 0.105]), Euler([-np.pi / 2, 0, 0])))
    q0 = np.array([0, 0, 0, 0, np.pi / 2, 0])
    robot.moveAbsJ(q_target=q0, precision=False)

    piece_index = 0
    color_indices = np.array([0, 0, 0])
    n_pieces = 30
    for i in range(n_pieces):
        print('PROCESSING PIECE: ', i)
        while True:
            if conveyor_sensor.is_activated():
                break
            simulation.wait()

        color = find_color(robot, camera, piece_index)
        pick(robot, gripper, piece_index)
        place(robot, gripper, color, color_indices)
        robot.moveAbsJ(q_target=q0, precision=False)

        # Next piece! Update indices
        piece_index += 1
        if color == 'R':
            color_indices[0] += 1
        elif color == 'G':
            color_indices[1] += 1
        else:
            color_indices[2] += 1

    simulation.stop()


if __name__ == "__main__":
    pick_and_place()

