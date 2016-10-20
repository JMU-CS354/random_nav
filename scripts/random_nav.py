#!/usr/bin/env python

"""This node repeatedly selects random map positions until it finds
  one that can be navigated to.

  It then navigates to the random goals using the ROS navigation stack.

"""
import rospy
import map_utils

from nav_msgs.msg import OccupancyGrid

class RandomNavNode(object):
    def __init__(self):
        rospy.init_node('random_nav')

        rospy.Subscriber('map', OccupancyGrid, self.map_callback)

        self.map_msg = None

        while self.map_msg is None and not rospy.is_shutdown():
            rospy.loginfo("Waiting for map...")
            rospy.sleep(.1)

        self.map = map_utils.Map(self.map_msg)

        self.demo_map()

        # REPEAT THE FOLLOWING UNTIL ROSPY IS SHUT DOWN:
        #
        #    GENERATE A RANDOM GOAL LOCATION:
        #       *GENERATE RANDOM LOCATIONS WHERE X AND Y ARE BOTH
        #        IN THE RANGE [-10, 10].
        #       *CONTINUE GENERATING RANDOM GOAL LOCATIONS UNTIL ONE IS
        #        AT A FREE LOCATION IN THE MAP (see demo_map below)
        #
        #    ATTEMPT TO NAVIGATE TO THE GOAL:
        #       * SEND THE DESIRED GOAL IN THE MAP COORDINATE FRAME
        #         (see provided action_nav.py file)

    def demo_map(self):
        """ Illustrate how to interact with a loaded map object. """
        x_pos = 0.0
        y_pos = -2.0

        if self.map.get_cell(x_pos, y_pos) == 0:
            message = "clear"
        elif self.map.get_cell(x_pos, y_pos) < .5:
            message = "unknown"
        else:
            message = "occupied"

        message = "Position ({}, {}) is ".format(x_pos, y_pos) + message
        rospy.loginfo(message)

    def map_callback(self, map_msg):
        """ map_msg will be of type OccupancyGrid """
        self.map_msg = map_msg


if __name__ == "__main__":
    RandomNavNode()
