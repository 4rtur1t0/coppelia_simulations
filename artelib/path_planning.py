#!/usr/bin/env python
# encoding: utf-8
"""
Simple path planning functions.

@Authors: Arturo Gil
@Time: April 2021

"""
import numpy as np
from artelib.orientation import Quaternion
from artelib.tools import euler2rot, rot2quaternion, slerp, rot2euler, quaternion2rot, buildT


def potential(r):
    K = 0.3
    rs = 0.1  # radius of the sphere
    rmax = 0.2
    if r < rs:
        r = rs
    p = K * (1 / r - 1 / rmax)
    if p < 0:
        p = 0
    return p


def n_movements(p_current, p_target, vmax=1.0, delta_time=0.05):
    total_time = np.linalg.norm(np.array(p_target) - np.array(p_current)) / vmax
    n = total_time / delta_time
    n = np.ceil(n)
    return int(n)


def generate_target_positions(p_current, p_target, n):
    tt = np.linspace(0, 1, int(n))
    target_positions = []
    p_current = np.array(p_current)
    p_target = np.array(p_target)
    for t in tt:
        target_pos = t*p_target + (1-t)*p_current
        target_positions.append(target_pos)
    return target_positions


def generate_target_orientations(abc_current, abc_target, n):
    """
    Generate a set of Euler angles between abc_current and abc_target.
    """
    abc_current = np.array(abc_current)
    abc_target = np.array(abc_target)
    R1 = euler2rot(abc_current)
    R2 = euler2rot(abc_target)
    Q1 = rot2quaternion(R1)
    Q2 = rot2quaternion(R2)

    tt = np.linspace(0, 1, int(n))
    target_orientations = []
    for t in tt:
        Q = slerp(Q1, Q2, t)
        R = quaternion2rot(Q)
        abc = rot2euler(R)
        target_orientations.append(abc)
    return target_orientations


def generate_target_orientations_Q(Q1, Q2, n):
    """
    Generate a set of n quaternions between Q1 and Q2. Use SLERP to find an interpolation between them.
    """
    tt = np.linspace(0, 1, int(n))
    target_orientations = []
    for t in tt:
        Q = slerp(Q1, Q2, t)
        Q = Quaternion(Q)
        target_orientations.append(Q)
    return target_orientations


def move_target_positions_obstacles(target_positions, sphere_position):
    """
    Moves a series of points on a path considering a repulsion potential field.
    """
    sphere_position = np.array(sphere_position)
    final_positions = target_positions
    while True:
        total_potential = 0
        for i in range(len(final_positions)):
            r = np.linalg.norm(sphere_position-final_positions[i])
            u = final_positions[i]-sphere_position
            if r > 0:
                u = u/r
            pot = potential(r)
            # modify current position in the direction of u considering potential > 0
            final_positions[i] = final_positions[i] + 0.01*pot*u
            total_potential += pot
        if total_potential < 0.01:
            break
    return final_positions