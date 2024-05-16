import rclpy
import random

from rclpy.node import Node
from geometry_msgs.msg import Twist

import time
import math

from sensor_msgs.msg import LaserScan

class LidarTest(Node):

    def __init__(self):
        super().__init__('lidar_test')
        
        self.lidar_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.is_turning = False
        self.start_turn_time = time.time()
        self.angular_vel = 0.0
        
        self.dist_to_turn = 0.4
        
        
    def scan_callback(self, msg):
        front_distances = msg.ranges[320: 400]
        left_distances = msg.ranges[530: 550] # Left is 540
        right_distances = msg.ranges[170: 190] # Right is 180
        
        front_alpha_distances = msg.ranges[200:220]
        rear_alpha_distances = msg.ranges[140:160]
        
        # front_dist = self.average(front_distances)
        front_dist = min(front_distances)
        left_dist = self.average(left_distances)
        right_dist = self.average(right_distances)
        
        front_alpha_dist = self.average(front_alpha_distances)
        rear_alpha_dist = self.average(rear_alpha_distances)
        
        normalized_right = right_dist * (2 / math.sqrt(3))
        
        self.get_logger().info('Front Dist: "%s"' % front_dist)
        # self.get_logger().info('Left Dist: "%s"' % left_dist)
        self.get_logger().info('Right Dist: "%s"' % right_dist)
        # self.get_logger().info('Front Alpha Dist: "%s"' % front_alpha_dist)
        # self.get_logger().info('Rear Alpha Dist: "%s"' % rear_alpha_dist)
        #v self.get_logger().info('Normalized: "%s"' % normalized_right)
        

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
    lidar_test = LidarTest()
    rclpy.spin(lidar_test)
    
    lidar_test.destory_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()

