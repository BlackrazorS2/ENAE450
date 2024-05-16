import rclpy
import random

from rclpy.node import Node
from geometry_msgs.msg import Twist

import time
import math

from sensor_msgs.msg import LaserScan


class MazeHardware(Node):

    def __init__(self):
        super().__init__('maze_hardware')

        self.lidar_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.is_turning = False
        self.outside_turn = False
        self.left_turn = False
        self.start_turn_time = time.time()
        self.start_run_time = time.time()
        self.angular_vel = 0.0

        self.dist_to_turn = 0.3

    def scan_callback(self, msg):
        front_distances = msg.ranges[350: 370]
        left_distances = msg.ranges[530: 550]  # Left is 540
        right_distances = msg.ranges[170: 190]  # Right is 180

        front_alpha_distances = msg.ranges[200:220]
        rear_alpha_distances = msg.ranges[140:160]

        front_dist = self.average(front_distances)
        left_dist = self.average(left_distances)
        right_dist = self.average(right_distances)

        front_alpha_dist = self.average(front_alpha_distances)
        rear_alpha_dist = self.average(rear_alpha_distances)

        self.get_logger().info('Front Alpha Dist: "%s"' % front_alpha_dist)
        self.get_logger().info('Rear Alpha Dist: "%s"' % rear_alpha_dist)
        self.get_logger().info('Left Dist: "%s"' % left_dist)

        twist = Twist()

        if not self.is_turning:  # Case 1)
            twist.linear.x = 0.3
            self.angular_vel = 0.0

            if front_alpha_dist < 1:  # For wall correction
                self.angular_vel = (rear_alpha_dist - front_alpha_dist) * 6

            if front_dist < self.dist_to_turn and right_dist < self.dist_to_turn:  # Case 2)
                twist.linear.x = 0.0

                self.is_turning = True
                self.left_turn = True
                self.start_turn_time = time.time()

                self.angular_vel = (math.pi / 2) / 2  # (is this turning left or right? assuming left)

            if front_alpha_dist >= 1:  # Case 3)
                if front_dist >= 1.5*self.dist_to_turn:
                    self.start_run_time = time.time()

                    while time.time() - self.start_run_time < 2:
                        twist.linear.x = 0.3

                twist.linear.x = 0.0

                self.is_turning = True
                self.outside_turn = True

        else:  # Turning - Estimate for 90 degrees
            if self.left_turn:
                if time.time() - self.start_turn_time >= 2:
                    self.angular_vel = 0.0
                    self.is_turning = False
                    self.left_turn = False
            if self.outside_turn:
                while front_alpha_dist >= 1:
                    self.angular_vel = -(math.pi / 2) / 2  # (negative is for turning right?)
                self.angular_vel = 0.0
                self.is_turning = False
                self.outside_turn = False

        twist.angular.z = float(self.angular_vel)
        self.vel_pub.publish(twist)

    def average(self, list_to_avg):
        count = 0
        cur_sum = 0
        for item in list_to_avg:
            if item < 100:
                cur_sum += item
                count += 1

        if count == 0:
            return 0
        else:
            return cur_sum / count


def main(args=None):
    rclpy.init(args=args)
    maze_hardware = MazeHardware()
    rclpy.spin(maze_hardware)

    maze_hardware.destory_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
