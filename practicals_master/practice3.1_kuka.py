#!/usr/bin/env python
# encoding: utf-8
"""
Please open the scenes/kuka_14_R820.ttt scene before running this script.

INSTRUCTIONS:
    JUST RUN THE CODE. The RG2 gripper does collide with the robot wrist and the robot is stopped in simulation.

@Authors: Arturo Gil
@Time: April 2021

@Review: July 2023
"""
import numpy as np
from artelib.euler import Euler
from robots.grippers import GripperRG2
from robots.kukalbr import RobotKUKALBR
from robots.simulation import Simulation


def pick_and_place(robot, gripper, step_number):
    # max linear speed
    vmax = 0.5
    target_positions = [[0.6, -0.2, 0.25],  # initial in front of conveyor
                        [0.6, 0.1, 0.25],  # pick the piece
                        [0.6, -0.1, 0.4],  # bring the piece up (and backwards)
                        [0.2, -0.7, 0.4],  # over the table
                        [0.2, -0.7, 0.35]]  # drop the piece on the table
    target_orientations = [[-np.pi / 2, 0, -np.pi / 2],
                           [-np.pi / 2, 0, -np.pi / 2],
                           [-np.pi / 2, 0, -np.pi / 2],
                           [-np.pi, 0, 0],
                           [-np.pi, 0, 0]]
    # change target points for drop zone
    target_positions[3] = target_positions[3] + step_number * np.array([0, 0.06, 0])
    target_positions[4] = target_positions[4] + step_number * np.array([0, 0.06, 0])

    # initial arm position
    q0 = np.array([-np.pi/8, 0, -np.pi/2, -np.pi/2, 0, -np.pi/2, 0])
    robot.secondary_objective = False
    # plan trajectories
    q1_path = robot.inversekinematics_line(target_position=target_positions[0],
                                           target_orientation=Euler(target_orientations[0]), q0=q0, vmax=vmax)
    q2_path = robot.inversekinematics_line(target_position=target_positions[1],
                                           target_orientation=Euler(target_orientations[1]), q0=q1_path[-1], vmax=vmax)
    q3_path = robot.inversekinematics_line(target_position=target_positions[2],
                                           target_orientation=Euler(target_orientations[2]), q0=q2_path[-1], vmax=vmax)
    q4_path = robot.inversekinematics_line(target_position=target_positions[3],
                                           target_orientation=Euler(target_orientations[3]), q0=q3_path[-1], vmax=vmax)
    q5_path = robot.inversekinematics_line(target_position=target_positions[4],
                                           target_orientation=Euler(target_orientations[4]), q0=q4_path[-1], vmax=vmax)

    # NOW execute trajectories computed before.
    # set initial position of robot
    robot.moveAbsJ(q_target=q0, precision=True)
    robot.wait(15)
    gripper.open(precision=True)
    # set the target we are willing to reach on Coppelia
    # robot.set_target_position_orientation(target_positions[0], target_orientations[0])
    # robot.set_joint_target_trajectory(q1_path, precision='last')
    # robot.set_joint_target_trajectory(q2_path, precision='last')
    # gripper.close(precision=True)
    # robot.set_joint_target_trajectory(q3_path, precision='last')
    # robot.set_joint_target_trajectory(q4_path, precision='last')
    # robot.set_joint_target_trajectory(q5_path, precision='last')
    # gripper.open(precision=True)
    # # reverse array, from q4 to q5 and now q5 to q4
    # robot.set_joint_target_trajectory(q_path=q5_path[::-1])
    # # back to initial
    # robot.set_joint_target_positions(q0, precision=False)
    # robot.wait(15)


def pallet_application():
    simulation = Simulation()
    simulation.start()
    robot = RobotKUKALBR(simulation=simulation)
    robot.start()
    gripper = GripperRG2(simulation=simulation)
    gripper.start(name='/LBR_iiwa_14_R820/RG2/RG2_openCloseJoint')

    for i in range(0, 6):
        pick_and_place(robot, gripper, i)

    robot.plot_trajectories()
    simulation.stop()


if __name__ == "__main__":
    pallet_application()
