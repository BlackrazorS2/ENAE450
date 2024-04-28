import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class outsideWallFollow(Node):

    def __init__(self):
        super().__init__("hw5_3_outside")
        
        # grab params from launch file
        self.declare_parameter("travel_dist", rclpy.Parameter.Type.FLOAT) # in meters
        self.declare_parameter("clockwise", rclpy.Parameter.Type.BOOL) # true for clockwise, false for ccw
        
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_list = self.create_subscription(Type, "/scan", self.scan_callback, 10)



    def scan_callback(self, msg):
        pass

def main(args=None):
    rclpy.init(args=args)
    # create node
    outsideFollow = outsideWallFollow()

    rclpy.spin(outsideFollow)



if __name__ in "__main__":
    main()