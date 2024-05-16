import rclpy
import random

from rclpy.node import Node
from geometry_msgs.msg import Twist

import time
import math

from sensor_msgs.msg import LaserScan

class MazeSolver(Node):

    def __init__(self):
        super().__init__('maze_solver')
        
        self.lidar_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.is_turning = False
        self.start_turn_time = time.time()
        self.angular_vel = 0.0
        
        self.dist_to_turn = 0.4
        self.dist_to_wall = 0.35
        
        self.turn_time = 4.7
        
        self.has_right_wall = False
        self.approach_outside_corner = True
        
        self.state = "Start"
        
        
    def scan_callback(self, msg):
    	
    	# Get Direct Distances
        front_distances = msg.ranges[320: 400]
        left_distances = msg.ranges[530: 550] # Left is 540
        right_distances = msg.ranges[170: 190] # Right is 180
        
        # Get two beams on the right side
        front_alpha_distances = msg.ranges[200:220]
        rear_alpha_distances = msg.ranges[140:160]
        
        front_dist = min(front_distances)
        left_dist = self.average(left_distances)
        right_dist = self.average(right_distances)
        
        front_alpha_dist = self.average(front_alpha_distances)
        rear_alpha_dist = self.average(rear_alpha_distances)
        
        # self.get_logger().info('Front Dist: "%s"' % front_dist)
        # self.get_logger().info('Left Dist: "%s"' % left_dist)
        # self.get_logger().info('Right Dist: "%s"' % right_dist)
        self.get_logger().info('State: %s' % self.state)
        twist = Twist()

        if self.state == "Start":
            if right_dist < 0.6:
                self.state = "Straight"
            else:
                twist.linear.x = 0.25
                self.get_logger().info('Moving')
                if front_dist < self.dist_to_turn:
                    twist.linear.x = 0.0
                    self.state = "Inside Turn"
                    if left_dist > 0.6:
                        self.turn_left()
                    elif right_dist > 0.6:
                        self.turn_right()
                    else:
                        self.turn_around()
        elif self.state == "Straight": 
            twist.linear.x = 0.5
            
            if front_dist < 1.0:
                twist.linear.x = front_dist / 4
            
            self.angular_vel = 0.0
            
            if rear_alpha_dist < 0.6 and front_alpha_dist < 0.6: 
                self.angular_vel = (rear_alpha_dist - front_alpha_dist) * 4
                self.angular_vel += -1 * (right_dist - self.dist_to_wall) * 2
            elif front_alpha_dist > 0.4 and abs(front_alpha_dist - rear_alpha_dist) - 0.15 :
                self.state = "Approach Outside"
                self.start_turn_time = time.time()
            
            if front_dist < self.dist_to_turn: # Prepare to turn
                twist.linear.x = 0.0
                
                self.state = "Two Beam Adjust"
                
        elif self.state == "Two Beam Adjust":
            twist.linear.x = 0.0
            
            if 0.2 > abs(rear_alpha_dist - front_alpha_dist) > 0.01:
                self.angular_vel = (rear_alpha_dist - front_alpha_dist) * 4
            elif front_dist < self.dist_to_turn + 0.05:
                self.angular_vel = 0.0
                self.state = "Inside Turn"
                if right_dist > 0.6:
                    self.turn_right()
                elif left_dist > 0.6:
                    self.turn_left()
                else:
                    self.turn_around()
            else:
                self.angular_vel = 0.0
                self.state = "Straight"
                
        elif self.state == "Inside Turn": # Inside Corner Turning. Once estimate has been done use two beam adjustment to correct misalignment
            if time.time() - self.start_turn_time >= self.turn_time:
                self.angular_vel = 0.0
                # self.state = "Approach Wall"
                self.state = "Two Beam Adjust"      
                 
        elif self.state == "Approach Outside":
            self.angular_vel = 0.0
            
            search_range = msg.ranges[0: 180]
            
            min_angle = search_range.index(min(search_range)) / 2
            
            if front_dist > 0.5:
                if abs(45 - min_angle) < 5:
                    twist.linear.x = 0.0
                    self.turn_right()
                    self.state = "Outside Turn"
                else:
                    if rear_alpha_dist > 0.5:
                        twist.linear.x = (min_angle - 45) / 45
                    else:
                        twist.linear.x = 0.25
            else:
                if front_dist < self.dist_to_turn:
                    twist.linear.x = 0.0
                    self.turn_right()
                    self.state = "Outside Turn"
                else:
                    twist.linear.x = front_dist / 4

        elif self.state == "Outside Turn": 
            if time.time() - self.start_turn_time >= self.turn_time:
                self.angular_vel = 0.0
                
                search_range = msg.ranges[180: 360]
                min_angle = search_range.index(min(search_range)) / 2
                
                if abs(45 - min_angle) < 5:
                    self.angular_vel = 0.0
                    self.state = "Approach Wall"
                else:
                    self.angular_vel = 0.5 * (min_angle - 45) / 45
            
        elif self.state == "Approach Wall":
            twist.linear.x = 0.25
            self.angular_vel = 0.0
            if front_dist < self.dist_to_turn:
                twist.linear.x = 0.0
                self.state = "Inside Turn"
                if left_dist > 0.6:
                    self.turn_left()
                elif right_dist > 0.6:
                    self.turn_right()
                else:
                    self.turn_around()
            elif right_dist < 0.55:
                twist.linear.x = 0.0
                self.angular_vel = 0.0
                
                self.state = "Straight"                    
        elif self.state == "End":
            twist.linear.x = 0.0
            self.angular_vel = 0.0
            
        
        if left_dist > 2 and right_dist > 2 and front_dist > 2:
            twist.linear.x = 0.0
            self.angular_vel = 0.0
            self.state = "End"
            self.get_logger().info('End')
        
        twist.angular.z = float(self.angular_vel)
        self.vel_pub.publish(twist) 
        
    def turn_right(self):
        self.start_turn_time = time.time()

        self.angular_vel = -1 * (math.pi / 2) / 4
        
    def turn_left(self):
        self.start_turn_time = time.time()

        self.angular_vel = (math.pi / 2) / 4
        
    def turn_around(self):
        self.start_turn_time = time.time()

        self.angular_vel = (math.pi / 2) / 2    

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
    maze_solver = MazeSolver()
    rclpy.spin(maze_solver)
    
    maze_solver.destory_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()

