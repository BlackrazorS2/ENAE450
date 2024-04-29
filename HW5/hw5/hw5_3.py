import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from time import sleep
import math


class outsideWallFollow(Node):

    def __init__(self):
        super().__init__("hw5_3_outside")
                
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_list = self.create_subscription(LaserScan, "/scan", self.scan_callback,10)

        self.pace = 0.1 # sets how long to wait between publishes
        self.approached = False
        self.dist = 0.5 # meters
        self.edge = 0

    def scan_callback(self, msg):
        adjust = Twist()
        rangeData = list(msg.ranges)
        mindist = min(rangeData)
        rightdist = self.average(rangeData[260:280])
        leftdist = self.average(rangeData[80:100])
        backdist = self.average(rangeData[135:225])
        frontdist = self.average((rangeData[355:360]+rangeData[0:5]))

        if not self.approached:
            if frontdist <= self.dist:
                self.get_logger().info("Approached!")
                adjust.angular.z = 1.3124
                adjust.linear.x = 0.0
                self.vel_pub.publish(adjust)
                sleep(1)
                self.approached = True
                return None
            else:
                adjust.angular.z = 0.0
                adjust.linear.x = 0.2
                self.vel_pub.publish(adjust)
                sleep(self.pace)
        else:
            if rightdist < self.dist and self.approached:
                adjust.angular.z = 0.03
                adjust.linear.x = 0.4
                self.vel_pub.publish(adjust)
                sleep(self.pace)
            elif rightdist > self.dist and self.approached:
                adjust.angular.z = -0.03
                adjust.linear.x = 0.4
                self.vel_pub.publish(adjust)
                sleep(self.pace)
            else:
                adjust.angular.z = 0.0
                adjust.linear.x = 0.4
                self.vel_pub.publish(adjust)
                sleep(self.pace) 
            if rightdist > self.dist+1 and self.approached: # we are past the edge of the wall
                self.edge += 1
                if self.edge > 5: # gives time to fully pass
                    self.get_logger().info("Turning corner")
                    adjust.angular.z = -1.59
                    adjust.linear.x = 0.0
                    self.vel_pub.publish(adjust)
                    sleep(1)
                    self.edge = -50 # gives time to complete turn and get back to wall
            else:
                if self.edge < -5:
                   self.edge += 1
                else:
                    self.edge = 0

    def average(self, iterable):      
        total = sum(iterable)
        length = len(iterable)
        return total/length
    

def main(args=None):
    rclpy.init(args=args)
    # create node
    outsideFollow = outsideWallFollow()

    rclpy.spin(outsideFollow)

    outsideFollow.destroy_node()
    rclpy.shutdown()

if __name__ in "__main__":
    main()