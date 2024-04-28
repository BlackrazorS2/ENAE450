# create subscriber to the /scan topic
# create publisher to the /cmd_vel topic
# read parameters for travel distance from wall
# and rotation direction
from importlib.abc import Traversable
from ssl import VERIFY_CRL_CHECK_CHAIN
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from time import sleep
import math

class insideWallFollow(Node):
    

    def __init__(self):
        super().__init__("hw5_2_inside")
        # grab params from launch file
        self.declare_parameter("travel_dist", rclpy.Parameter.Type.FLOAT) # in meters
        self.declare_parameter("clockwise", rclpy.Parameter.Type.BOOL) # true for clockwise, false for ccw
        self.clockwise = self.get_parameter("clockwise").value
        self.dist =self.get_parameter("travel_dist").value
        # get parameter using respawning_allowed = self.get_parameter("respawning").value
        
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_list = self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)


    def scan_callback(self, msg):
        adjust = Twist()
       
        # look at the scan topic
        # determine if we are in a corner or just along the wall, or facing the wall
        # call the appropriate function
        # left is 540 right is 180
        rangeData = msg.ranges
        for idx, range in rangeData: # idx is our angle value
            if range < self.dist: # we are in range of wall
                # ok now we do logic for turning
                # we desire an angle of 90 degrees (index 180 or 540 on the lidar)
                if self.clockwise:
                    # wall is on the left of the robot
                    if idx > 540: # we need to rotate counter clockwise to become parallel
                        adjust.angular_z = (idx-180)*math.pi/180
                        adjust.linear_x = 1.0
                        self.vel_pub.publish(adjust)
                        sleep(1) 


        pass

    def alongWall(self):
        # check if we are the correct distance from the wall
        # if not turn slightly to go in and out
        # if we are then just go forward a small amount
        pass
    
    def corner(self):
        pass

    def wallFace(self):
        if self.clockwise:
            # rotate to the right a bit 
            pass

    def average(iterable):      
        total = sum(iterable)
        length = len(iterable)
        return total/length
def main(args=None):
    rclpy.init(args=args)
    # create node
    insideFollow = insideWallFollow()

    rclpy.spin(insideFollow)



if __name__ in "__main__":
    main()