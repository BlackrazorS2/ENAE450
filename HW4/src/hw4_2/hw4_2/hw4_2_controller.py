import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute
from turtlesim.msg import Pose
from time import sleep
import math

class DemoPublisher(Node):

    def __init__(self):
        super().__init__('hw4_2_controller')
        # create velocity publisher
        self.publisher_vel = self.create_publisher(Twist,
                                                   '/turtlesim1/turtle1/cmd_vel', 
                                                   10)
        # create pen client
        self.pen_cli = self.create_client(SetPen, "/turtlesim1/turtle1/set_pen")
        
        while not self.pen_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('pen service not available, waiting...')

        # create teleport client
        self.tp_abso = self.create_client(TeleportAbsolute, 
                                          "/turtlesim1/turtle1/teleport_absolute")
        while not self.tp_abso.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('tp service not available, waiting...')
        
        self.pen = SetPen.Request()
        self.tp_req = TeleportAbsolute.Request()

        # create clear screen client
        self.clear_cli = self.create_client(Empty, "/turtlesim1/clear")
        self.empt = Empty.Request()

        # subscribe to the position of the turtle
        self.pose_sub = self.create_subscription(Pose, 
                                                 "/turtlesim1/turtle1/pose", 
                                                 self.pose_callback, 
                                                 10)
        self.pose_x = -5
        self.pose_y = -5
        self.pose_z = 0
        self.k = 1
        self.w = 1

    def move_request(self, x, y, theta):
        # teleport to a specified x, y, and theta
        self.tp_req.x = float(x)
        self.tp_req.y = float(y)
        self.tp_req.theta = float(theta)
        self.get_logger().info('params set, teleporting...')
        self.future = self.tp_abso.call_async(self.tp_req)
        self.get_logger().info('done')

    def pen_request(self, off):
        # lift the pen up or down as needed
        if off == True:
            self.pen.off = 255
        else:
            self.pen.off = 0
        self.get_logger().info('pen status set, changing...')
        self.future = self.pen_cli.call_async(self.pen)
        self.get_logger().info('done')

    def pose_callback(self, msg):
        # get the current position of the turtle and adjust it to fit our 
        # coordinate axes
        self.pose_x = msg.x - 5
        self.pose_y = msg.y - 5
        self.pose_z = msg.theta
        

    def clear_screen(self):
        self.future = self.clear_cli.call_async(self.empt)


    def lin_vel(self):
        # dy/dx or the velocity is going to be equal to k
        # angular velocity then is arctan k
        msg = Twist()
        msg.linear.x = 0.0
        req_z = math.atan(self.k)
        msg.angular.z = req_z - self.pose_z
        self.pose_z = req_z
        self.publisher_vel.publish(msg)
        sleep(1)
        # can go fast since its just a straight line
        msg.linear.x = 4.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)
        
    def cubic_vel(self):
        # derivative of y = kx^3 is 3kx^2
        msg = Twist()
        msg.linear.x = 1.0
        dydx = 3*self.k*math.pow(self.pose_x,2)
        req_z = math.atan(dydx)
        msg.angular.z = req_z - self.pose_z
        self.pose_z = req_z
        self.publisher_vel.publish(msg)
        sleep(1)
    def sin_vel(self):
        # derivative of y = ksin(wx) is kwcos(wx)
        msg = Twist()
        msg.linear.x = .5
        dydx = self.k*self.w*math.cos(self.w*self.pose_x)
        req_z = math.atan(dydx)
        msg.angular.z = req_z - self.pose_z
        self.pose_z = req_z
        self.publisher_vel.publish(msg)
        sleep(1)
        
        

def main(args=None):
    rclpy.init(args=args)

    hw4_2_controller = DemoPublisher()
    sleep(1)
    hw4_2_controller.pen_request(True)
    while rclpy.ok():
        rclpy.spin_once(hw4_2_controller)
        hw4_2_controller.get_logger().info('pen service not processed waiting...')
        if hw4_2_controller.future.done():
            break
    
    # move the turtle to the correct position to start the function y=kx
    hw4_2_controller.move_request(0,0,0) # starting at -5,-5
    hw4_2_controller.clear_screen()
    # now we loop through adjusting velocities
    for i in range(0,3):
        hw4_2_controller.pen_request(False)
        match i:
            case 0:
                # starting at -5,-5
                hw4_2_controller.move_request(0,0,0)
                hw4_2_controller.clear_screen()
                hw4_2_controller.pose_x = -5
                hw4_2_controller.pose_y = -5
                hw4_2_controller.pose_z = 0
                hw4_2_controller.get_logger().info('Drawing y=kx')
                while hw4_2_controller.pose_x <= 5 and hw4_2_controller.pose_y <=5:
                    hw4_2_controller.lin_vel()
                    rclpy.spin_once(hw4_2_controller)
                    rclpy.spin_once(hw4_2_controller)
            case 1:
                # starting at -1.7,-at theta = 1.55 rad
                hw4_2_controller.move_request(3.3,0,0)
                hw4_2_controller.clear_screen()
                hw4_2_controller.pose_x = -1.7
                hw4_2_controller.pose_y = -5
                hw4_2_controller.pose_z = 0
                hw4_2_controller.get_logger().info('Drawing y = kx^3')
                while hw4_2_controller.pose_x <= 5.5 and hw4_2_controller.pose_y <=5.5:
                    hw4_2_controller.cubic_vel()
                    rclpy.spin_once(hw4_2_controller)
                    rclpy.spin_once(hw4_2_controller)
            case 2:
                # starting at -1.7,-5 at pi/2 rad
                hw4_2_controller.move_request(0,5,math.pi/2) 
                hw4_2_controller.clear_screen()
                hw4_2_controller.pose_x = -5
                hw4_2_controller.pose_y = 0
                hw4_2_controller.pose_z = 0
                hw4_2_controller.get_logger().info('Drawing y= ksinwx')
                while hw4_2_controller.pose_x <= 5 and hw4_2_controller.pose_y <=5:
                    hw4_2_controller.sin_vel()
                    # this function needs some time normally
                    rclpy.spin_once(hw4_2_controller)
                    rclpy.spin_once(hw4_2_controller)
                    rclpy.spin_once(hw4_2_controller)
                    rclpy.spin_once(hw4_2_controller)
            case _:
                # should never be here
                break
        # lift up pen and clear
        hw4_2_controller.pen_request(True)
        hw4_2_controller.clear_screen()

        
    # spin to win
    rclpy.spin(hw4_2_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    hw4_2_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
