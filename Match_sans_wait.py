# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:34:43 2023

@author: vince
"""

from numpy import pi, cos, sin, tan, arctan2
import rsk
import random
import time
from math import sqrt
from rsk.constants import field_length, field_width, goal_width, defense_area_length, defense_area_width, robot_radius
from rsk.utils import all_robots
dx = field_length/100
dy = field_width/100
with rsk.Client("127.0.0.1", "") as c:

    blue1 = c.blue1
    blue2 = c.blue2
    green1 = c.green1
    green2 = c.green2

    def real_to_grid(x, y):
        return int((field_length/2+x)/dx), int((field_width/2-y)/dy)

    def add_grid(map, x, y):
        x_grid, y_grid = real_to_grid(x, y)
        if x_grid > 0 and x_grid < 100 and y_grid > 0 and y_grid < 100:
            map[y_grid][x_grid] = 1
        return map

    def add_obstacle(map, obstacle):
        x_center, y_center = obstacle.position[0], obstacle.position[1]
        x_center_grid, y_center_grid = real_to_grid(x_center, y_center)
        x, y = 0, 0
        while y <= robot_radius:
            x = 0
            while x <= sqrt(robot_radius-y**2):
                map = add_grid(map, x_center+x, y_center+y)
                map = add_grid(map, x_center-x, y_center-y)
                map = add_grid(map, x_center+x, y_center-y)
                map = add_grid(map, x_center-x, y_center+y)
                x = x+dx
            y = y+dy
        return map

    def init_map(robots):
        map = []
        for i in range(0, 100):
            ligne = []
            for j in range(0, 100):
                ligne.append(0)
            map.append(ligne)

        for obstacle in robots:
            map = add_obstacle(map, obstacle)
        return map

    def affiche_graph(map):
        for y in range(0, 100):
            print(map[y])

    def test():
        affiche_graph(init_map((green1,green2,blue1)))