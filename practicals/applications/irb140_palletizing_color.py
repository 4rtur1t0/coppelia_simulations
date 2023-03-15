#!/usr/bin/env python
# encoding: utf-8
"""
Please open the scenes/irb140.ttt scene before running this script.

The script shows how to use the camera on the robot arm to detect a color using a simple image processing.
The mean color of the image is returned and compared to pure colors.
A simple classification in RGB is then used to place the pieces in three main destinations (without any order)

Please: beware that increasing the image resolution may lead to a slow execution.

@Authors: Arturo Gil
@Time: April 2022
"""
import numpy as np
from artelib.euler import Euler
from artelib.homogeneousmatrix import HomogeneousMatrix
from artelib.rotationmatrix import RotationMatrix
from artelib.vector import Vector
from robots.abbirb140 import RobotABBIRB140
from robots.grippers import GripperRG2
from robots.proxsensor import ProxSensor
from robots.simulation import Simulation
from robots.camera import Camera


def find_color(robot, camera):
    """
    Places the camera on top of the piece.
    Saves the image for inspection.
    Computes the image to get the mean RGB value and the color name (red, green, blue).
    """
    # position and orientation so that the camera sees the piece
    tp1 = Vector([0.6, 0.33, 0.4])
    tp2 = Vector([0.6, 0.33, 0.3])
    to = Euler([0, np.pi, 0])
    q0 = np.array([0, 0, 0, 0, np.pi / 2, 0])
    robot.moveAbsJ(q0)
    robot.moveJ(target_position=tp1, target_orientation=to)
    robot.moveL(target_position=tp2, target_orientation=to)
    # capture an image and returns the closest color
    print('get_image')
    color = camera.get_color_name()
    print('Piece is: ', color)
    robot.moveL(target_position=tp1, target_orientation=to)
    return color


def pick(robot, gripper):
    """
    Picks the piece from the conveyor belt.
    """
    tp1 = Vector([0.6, 0.267, 0.23])  # approximation
    tp2 = Vector([0.6, 0.267, 0.19])  # pick
    to = Euler([0, np.pi, 0])
    gripper.open(precision=True)
    robot.moveJ(target_position=tp1, target_orientation=to, precision=True)
    robot.moveL(target_position=tp2, target_orientation=to, precision='last')
    gripper.close(precision=True)


def place(robot, gripper, color):
    """
    Places, at three different heaps the pieces
    """
    if color == 'R':
        tp = Vector([-0.5, -0.5, 0.5])  # pallet R base position
    elif color == 'G':
        tp = Vector([0.0, -0.5, 0.5])  # pallet R base position
    else:
        tp = Vector([0.5, -0.5, 0.5])  # pallet R base position

    to = Euler([0, np.pi, 0])
    q0 = np.array([0, 0, 0, 0, 0, 0])
    robot.moveAbsJ(q0)
    robot.moveJ(target_position=tp, target_orientation=to)
    tp = tp + Vector(np.array([0, 0, -0.05]))
    robot.moveJ(target_position=tp, target_orientation=to)
    gripper.open(precision=True)


def pick_and_place():
    # Start simulation
    simulation = Simulation()
    clientID = simulation.start()
    # Connect to the robot
    robot = RobotABBIRB140(clientID=clientID)
    robot.start()
    # Connect to the proximity sensor
    conveyor_sensor = ProxSensor(clientID=clientID)
    conveyor_sensor.start()
    # Connect to the gripper
    gripper = GripperRG2(clientID=clientID)
    gripper.start()
    # set the TCP of the RG2 gripper
    robot.set_TCP(HomogeneousMatrix(Vector([0, 0, 0.19]), RotationMatrix(np.eye(3))))
    # Connect a camera to obtain images
    camera = Camera(clientID=clientID)
    camera.start()

    q0 = np.array([0, 0, 0, 0, np.pi / 2, 0])
    robot.moveAbsJ(q0, precision=True)
    n_pieces = 48
    for i in range(n_pieces):
        while True:
            if conveyor_sensor.is_activated():
                break
            robot.wait()
        color = find_color(robot, camera)
        pick(robot, gripper)
        place(robot, gripper, color)

    simulation.stop()


if __name__ == "__main__":
    pick_and_place()

