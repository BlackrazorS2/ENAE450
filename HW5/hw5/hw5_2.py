# create subscriber to the /scan topic
# create publisher to the /cmd_vel topic
# read parameters for travel distance from wall
# and rotation direction
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from time import sleep


class insideWallFollow(Node):
    

    def __init__(self):
        super().__init__("hw5_2_inside")
        # grab params from launch file
        self.declare_parameter("travel_dist", rclpy.Parameter.Type.DOUBLE) # in meters
        self.declare_parameter("clockwise", rclpy.Parameter.Type.BOOL) # true for clockwise, false for ccw
        self.clockwise = self.get_parameter("clockwise").value
        self.get_logger().info(f"Clockwise rotation set to [{self.clockwise}]")
        self.dist =self.get_parameter("travel_dist").value
        self.get_logger().info(f"Travel distance set to [{self.dist}]")
        
        
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_list = self.create_subscription(LaserScan, "/scan", self.scan_callback,10)

        self.pace = 0.1 # sets how long to wait between publishes
        
    def scan_callback(self, msg):
        # for some reason in gazebo this ranges from 0 to 360, while in lab it ranges from 0 to 720
        
        adjust = Twist()
        rangeData = list(msg.ranges)
        mindist = min(rangeData)
    
        rightdist = self.average(rangeData[260:280])
        leftdist = self.average(rangeData[80:100])
        backdist = self.average(rangeData[135:225])
        frontdist = self.average((rangeData[355:360]+rangeData[0:5]))



        if mindist > self.dist+.1 and (leftdist > self.dist+.2 and rightdist > self.dist+.2):
            adjust.angular.z = 0.0
            adjust.linear.x = 0.4
            self.vel_pub.publish(adjust)
            sleep(self.pace)

            
        elif frontdist < self.dist:
            if self.clockwise:
                adjust.angular.z = -3.14
            else:
                adjust.angular.z = 3.14
            adjust.linear.x = 0.0
            self.vel_pub.publish(adjust)
            sleep(self.pace)
        
        elif leftdist < rightdist and leftdist < self.dist: # wall is on our left, move out a bit
            
            adjust.angular.z = -0.2
            adjust.linear.x = 0.2
            self.vel_pub.publish(adjust)
            sleep(self.pace)
        
        elif leftdist < rightdist and (leftdist > self.dist): # wall is on our left, move in a bit
            
            adjust.angular.z = 0.2
            adjust.linear.x = 0.2
            self.vel_pub.publish(adjust)
            sleep(self.pace)
    
        elif leftdist > rightdist and (rightdist > self.dist): # wall is on our right, move in a bit
            
            adjust.angular.z = -0.2
            adjust.linear.x = 0.2
            self.vel_pub.publish(adjust)
            sleep(self.pace)
        
        elif leftdist > rightdist and rightdist < self.dist: # wall is on our right, move out a bit
            
            adjust.angular.z = 0.2
            adjust.linear.x = 0.2
            self.vel_pub.publish(adjust)
            sleep(self.pace)
        
        
        else:
            adjust.angular.z = 0.0
            adjust.linear.x = 0.4
            self.vel_pub.publish(adjust)
            sleep(self.pace)

    def average(self, iterable):      
        total = sum(iterable)
        length = len(iterable)
        return total/length
    
def main(args=None):
    rclpy.init(args=args)
    # create node
    insideFollow = insideWallFollow()

    rclpy.spin(insideFollow)

    insideFollow.destroy_node()
    rclpy.shutdown()

if __name__ in "__main__":
    main()