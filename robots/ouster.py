#!/usr/bin/env python
# encoding: utf-8
"""
Classes to manage a OS1 LIDAR in Coppelia simulations (a LiDAR sensor)

@Authors: Arturo Gil
@Time: April 2021
"""
import numpy as np


class Ouster():
    def __init__(self, simulation):
        self.simulation = simulation
        self.handle = None

    def start(self, name='OS1'):
        handle = self.simulation.sim.getObject(name)
        self.handle = handle

    def get_laser_data(self):
        """
        This reads the laserdata signal in Coppelia and returns it.
        The laserdata signal must be defined as in the UR5_velodyne.ttt environment.
        """
        for i in range(5):
            data = self.simulation.sim.readCustomDataBlock(self.simulation.sim.handle_scene, "laserdata")
            data = self.simulation.sim.unpackFloatTable(data)
            if data != None:
                # reshape to 3D points
                data = np.reshape(data, (-1, 3))
                self.pointcloud.points = o3d.utility.Vector3dVector(data)
                return data

    def from_file(self, filename):
        self.pointcloud = o3d.io.read_point_cloud(filename, print_progress=True)


    def from_points(self, points):
        self.pointcloud.points = o3d.utility.Vector3dVector(points)

    def save_pointcloud(self, output_filename):
        o3d.io.write_point_cloud(output_filename, self.pointcloud)

