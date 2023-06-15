# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:45:51 2023

@author: vince
"""

from numpy import pi, cos, sin, tan, arctan2
import rsk
import random
import time
from rsk.constants import field_length, field_width, goal_width, defense_area_length, defense_area_width


with rsk.Client("127.0.0.1", "") as c:

    blue1 = c.blue1
    blue2 = c.blue2
    green1 = c.green1
    green2 = c.green2

    def compute_straight_coordinates(angle, radius=0.3, center=(0, 0)):
        """
        Computes the (x,y,alpha) coordinates of a target on a straight circle.
        Target is oriented toward the middle of the circle.

        Parameters
        ----------
        angle : float
            Angle of the target position. [radiant]
        radius : float, optional
            Value of the radius of the circular trajectory. The default is 0.3. [meters]
        center : float, optional
            Coordinates of the center of the circular trajectory. The default is (0, 0).

        Returns
        -------
        x : float
            X Coordinate of the target point.[meters]
        y : float
            Y Coordinate of the target point.[meters]
        alpha : float
            Orientation of the target point.[radiants]

        """
        x = radius*cos(angle) + center[0]
        y = radius*sin(angle) + center[1]
        alpha = pi + angle
        return x, y, alpha

    def compute_wavy_coordinates(angle, modulation, radius=0.3, center=(0, 0)):
        """
        Computes the (x,y,alpha) coordinates of a target on a wavy circle.
        Target is oriented toward the right.

        Parameters
        ----------
        angle : float
            Angle of the target position. [radiant]
        radius : float, optional
            Value of the radius of the circular trajectory. The default is 0.3. [meters]
        center : float, optional
            Coordinates of the center of the circular trajectory. The default is (0, 0).
        modulation : float
            Angle of the modulation responsible of the wavyness of the trajectory.[radiants]
            Increase the value to make it wave faster
        Returns
        -------
        x : float
            X Coordinate of the target point.[meters]
        y : float
            Y Coordinate of the target point.[meters]
        alpha : float
            Orientation of the target point.[radiants]


        """
        x = (radius+0.10*sin(modulation))*cos(angle) + center[0]
        y = (radius+0.10*sin(modulation))*sin(angle) + center[0]
        alpha = pi+angle
        return x, y, alpha

    def compute_eight_coordinates(angle, radius=0.3, center=(0, 0)):
        """
        Computes the (x,y,alpha) coordinates of a target on a eight shape trajectory.
        Target is oriented toward the the direction it s going.

        Parameters
        ----------
        angle : float
            Angle of the target position. [radiant]
        radius : float, optional
            Value of the radius of the circular trajectory. The default is 0.3. [meters]
        center : float, optional
            Coordinates of the center of the circular trajectory. The default is (0, 0).

        Returns
        -------
        x : float
            X Coordinate of the target point.[meters]
        y : float
            Y Coordinate of the target point.[meters]
        alpha : float
            Orientation of the target point.[radiants]


        """
        x = radius*cos(angle) + center[0]
        y = radius*sin(2*angle) + center[0]
        alpha = 0
        return x, y, alpha

    def compute_cross_coordinates(angle, is_x_axis, radius=0.3, center=(0, 0)):
        """
        Computes the (x,y,alpha) coordinates of a target on a cross shape trajectory.
        Target is oriented toward the the direction it s going.

        Parameters
        ----------
        angle : float
            Angle of the target position. [radiant]
        is_x_axis : boolean
            Is true if axis to move on is x axis
        radius : float, optional
            Value of the radius of the circular trajectory. The default is 0.15. [meters]
        center : float, optional
            Coordinates of the center of the circular trajectory. The default is (0, 0).

        Returns
        -------
        x : float
            X Coordinate of the target point.[meters]
        y : float
            Y Coordinate of the target point.[meters]
        alpha : float
            Orientation of the target point.[radiants]


        """
        axe = radius*sin(angle)
        alpha = angle
        if is_x_axis:
            return axe+center[0], center[1], alpha
        else:
            return center[0], axe+center[1], alpha

    def all_leds_to(red, green, blue):
        """
        Changes the leds of all robots to given rgb values

        Parameters
        ----------
        red : int
            Red component value. Between 0 and 255
        green : int
            Green component value. Between 0 and 255
        blue : int
            Blue component value. Between 0 and 255

        Returns
        -------
        None.

        """
        blue1.leds(red, green, blue)
        blue2.leds(red, green, blue)
        green1.leds(red, green, blue)
        green2.leds(red, green, blue)

    def color_changer(color_timer, red, green, blue):
        """
        changes red green and blue values to make fluid transitions

        Parameters
        ----------
        color_timer : int
            counter that resets at value = 153.
        red : int
            Between 0 and 255.
        green : int
            Between 0 and 255.
        blue : int
            Between 0 and 255.

        Returns
        -------
        red : int
            Between 0 and 255.
        green : int
            Between 0 and 255.
        blue : int
            Between 0 and 255.

        """
        if (color_timer < 51):
            red = red-5
            green = green+5
        elif (color_timer < 102):
            green = green-5
            blue = blue+5
        else:
            blue = blue-5
            red = red+5
            
        print(red,blue,green)
        
        return red, green, blue

    def firestorm(start_angle, phase_shift):
        """
        Moves the robots in a wavy circle trajectory with their leds turned red.

        Parameters
        ----------
        start_angle : float
            Starting angle of the trajectory, robots will be regularly distributed
            from this angle.
        phase_shift : float
            Value responsible of the angle's growth the higher the faster.
            Be careful, if you try to go to fast robots will follow a strange trajectory.

        Returns
        -------
        None.

        """
        continuer = True
        red = 255
        green = 0
        blue = 0
        angle = start_angle
        all_leds_to(red, green, blue)
        while continuer == True:

            angle = angle+phase_shift
            blue1.goto(compute_wavy_coordinates((angle+3*pi/4), angle), False)
            blue2.goto(compute_wavy_coordinates((angle-3*pi/4), angle), False)
            green1.goto(compute_wavy_coordinates((angle-pi/4), angle), False)
            green2.goto(compute_wavy_coordinates((angle+pi/4), angle), False)

    def rainbow_firestorm(start_angle, phase_shift):
        """
        Moves the robots in a wavy circle trajectory with their leds turned red and changing color.

        Parameters
        ----------
        start_angle : float
            Starting angle of the trajectory, robots will be regularly distributed
            from this angle.
        phase_shift : float
            Value responsible of the angle's growth the higher the faster.
            Be careful, if you try to go to fast robots will follow a strange trajectory.

        Returns
        -------
        None.

        """
        continuer = True
        color_timer = 0
        red = 255
        green = 0
        blue = 0
        angle = start_angle
        all_leds_to(red, green, blue)
        while continuer == True:
            angle = angle+phase_shift
            blue1.goto(compute_wavy_coordinates((angle+3*pi/4), angle), False)
            blue2.goto(compute_wavy_coordinates((angle-3*pi/4), angle), False)
            green1.goto(compute_wavy_coordinates((angle-pi/4), angle), False)
            green2.goto(compute_wavy_coordinates((angle+pi/4), angle), False)
            
            red,green,blue = color_changer(color_timer, red, green, blue)
            all_leds_to(red,blue,green)
            color_timer = (color_timer+1) % 153
            if color_timer == 152:
                continuer = False

    def enigma(start_angle, phase_shift):
        """
        Moves the robots in a wavy circle trajectory with their leds turned red.

        Parameters
        ----------
        start_angle : float
            Starting angle of the trajectory, robots will be regularly distributed
            from this angle.
        phase_shift : float
            Value responsible of the angle's growth the higher the faster.
            Be careful, if you try to go to fast robots will follow a strange trajectory.

        Returns
        -------
        None.

        """
        cross_counter = 0
        time_counter = 0
        continuer = True
        red = 255
        green = 0
        blue = 0
        angle = start_angle
        is_x_axis = True
        all_leds_to(red, green, blue)
        while continuer == True:
            angle = angle+phase_shift

            blue1.goto(compute_eight_coordinates(
                angle, center=(-field_length/4, -field_length/4)), False)
            blue2.goto(compute_cross_coordinates(
                angle, is_x_axis, center=(-field_length/4, field_length/4)), False)
            green1.goto(compute_straight_coordinates(
                angle, center=(field_length/4, -field_length/4)), False)
            green2.goto(compute_wavy_coordinates(
                angle, 3*angle, center=(field_length/4, field_length/4)), False)
            if (cross_counter == 79):
                is_x_axis = not (is_x_axis)
            cross_counter = (cross_counter+1) % 80
            if time_counter == 160:
                continuer = False
            time_counter = time_counter+1

    c.goto_configuration('side')
    c.goto_configuration('dots')
    rainbow_firestorm(0, pi/20)
    enigma(0, pi/40)
