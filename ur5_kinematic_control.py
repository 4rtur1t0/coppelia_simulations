#!/usr/bin/env python
# encoding: utf-8
"""
Please open the scenes/ur5.ttt scene before running this script.

@Authors: Arturo Gil
@Time: April 2021

"""
import time
import sim
import sys
import numpy as np

# from artelib.tools import R2quaternion, compute_w_between_R
from artelib.ur5 import RobotUR5
from artelib.scene import Scene
import matplotlib.pyplot as plt

# standard delta time for Coppelia, please modify if necessary
from sceneconfig.ur5_scene import init_simulation_UR5

DELTA_TIME = 50.0/1000.0




def pick_and_place():
    robot, scene = init_simulation_UR5()
    target_positions = [[0.6, -0.2, 0.25],
                        [0.6, 0.1, 0.25],
                        [0.6, 0.1, 0.35],
                        [0.2, -0.6, 0.4],
                        [0.2, -0.6, 0.3]]
    target_orientations = [[-np.pi/2, 0, -np.pi/2],
                           [-np.pi/2, 0, -np.pi/2],
                           [-np.pi/2, 0, -np.pi/2],
                           [-np.pi, 0, 0],
                           [-np.pi, 0, 0]]

    q0 = np.array([-np.pi, 0, np.pi / 2, 0, 0, 0])
    # set initial position of robot
    robot.set_arm_joint_target_positions(q0, wait=True)

    # set the target we are willing to reach
    robot.set_target_position_orientation(target_positions[0], target_orientations[0])
    # plan trajectories
    [q1_path, _] = robot.inversekinematics(target_position=target_positions[0],
                                           target_orientation=target_orientations[0], q0=q0, fine=False)
    [q2_path, _] = robot.inversekinematics(target_position=target_positions[1],
                                           target_orientation=target_orientations[1], q0=q1_path[-1])
    [q3_path, _] = robot.inversekinematics(target_position=target_positions[2],
                                           target_orientation=target_orientations[2], q0=q2_path[-1], fine=False)
    [q4_path, _] = robot.inversekinematics(target_position=target_positions[3],
                                           target_orientation=target_orientations[3], q0=q3_path[-1])
    [q5_path, _] = robot.inversekinematics(target_position=target_positions[4],
                                           target_orientation=target_orientations[4], q0=q4_path[-1])
    # execute trajectories
    robot.open_gripper()
    robot.follow_q_trajectory(q1_path)
    robot.follow_q_trajectory(q2_path)
    robot.close_gripper(wait=True)
    robot.follow_q_trajectory(q3_path)
    robot.follow_q_trajectory(q4_path)
    robot.follow_q_trajectory(q5_path)
    robot.open_gripper(wait=True)

    robot.plot_trajectories()
    robot.stop_arm()
    scene.stop_simulation()


def pick_and_place_rep():
    robot, scene = init_simulation_UR5()
    target_positions = [[0.6, -0.2, 0.25],
                        [0.6, 0.1, 0.25],
                        [0.6, 0.1, 0.35],
                        [0.2, -0.7, 0.4]]
    target_orientations = [[-np.pi/2, 0, -np.pi/2],
                           [-np.pi/2, 0, -np.pi/2],
                           [-np.pi/2, 0, -np.pi/2],
                           [-np.pi, 0, 0]]

    q0 = np.array([-np.pi, 0, np.pi / 2, 0, 0, 0])
    # set initial position of robot
    robot.set_arm_joint_target_positions(q0, wait=True)

    # set the target we are willing to reach
    robot.set_target_position_orientation(target_positions[0], target_orientations[0])

    for i in range(0, 6):
        # plan trajectories
        [q1_path, _] = robot.inversekinematics_line(target_position=target_positions[0],
                                               target_orientation=target_orientations[0], q0=q0, fine=False)
        [q2_path, _] = robot.inversekinematics_line(target_position=target_positions[1],
                                               target_orientation=target_orientations[1], q0=q1_path[-1])
        [q3_path, _] = robot.inversekinematics_line(target_position=target_positions[2],
                                               target_orientation=target_orientations[2], q0=q2_path[-1], fine=False)
        target_pos = target_positions[3] + i * np.array([0, 0.07, 0])
        target_orient = target_orientations[3]
        [q4_path, _] = robot.inversekinematics_line(target_position=target_pos,
                                               target_orientation=target_orient, q0=q3_path[-1])
        target_pos = target_pos + np.array([0, 0, -0.1])
        [q5_path, _] = robot.inversekinematics_line(target_position=target_pos,
                                               target_orientation=target_orient, q0=q4_path[-1])
        target_pos = target_pos + np.array([0, 0, 0.1])
        [q6_path, _] = robot.inversekinematics_line(target_position=target_pos,
                                               target_orientation=target_orient, q0=q5_path[-1])
        q0 = q6_path[-1]

        # execute trajectories
        robot.open_gripper()
        robot.follow_q_trajectory(q1_path, 2)
        robot.follow_q_trajectory(q2_path, 2)
        robot.close_gripper(wait=True)
        robot.follow_q_trajectory(q3_path, 2)
        robot.follow_q_trajectory(q4_path, 2)
        robot.follow_q_trajectory(q5_path, 2)
        robot.open_gripper(wait=False)
        robot.follow_q_trajectory(q6_path, 2)

    robot.plot_trajectories()
    robot.stop_arm()
    scene.stop_simulation()


if __name__ == "__main__":
    # pick_and_place()
    pick_and_place_rep()
