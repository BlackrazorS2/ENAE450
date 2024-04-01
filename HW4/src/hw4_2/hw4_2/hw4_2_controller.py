import rclpy
from rclpy.node import Node

from rcl_interfaces.msg import ParameterDescriptor

from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute
from time import sleep
import math

class DemoPublisher(Node):

    def __init__(self):
        super().__init__('hw4_1_controller')
        self.publisher_vel = self.create_publisher(Twist, '/turtlesim1/turtle1/cmd_vel', 10)
        self.get_logger().info('publisher made')
        self.pen_cli = self.create_client(SetPen, "/turtlesim1/turtle1/set_pen")
        self.get_logger().info('pen cli made')
        while not self.pen_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('pen service not available, waiting...')
        self.tp_abso = self.create_client(TeleportAbsolute, "/turtlesim1/turtle1/teleport_absolute")
        self.get_logger().info('tp cli made')
        while not self.tp_abso.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('tp service not available, waiting...')
        self.pen = SetPen.Request()
        self.tp_req = TeleportAbsolute.Request()
        self.get_logger().info('done with init')
        self.k = 1
        self.w = 1

    def move_request(self, x, y, theta):
        self.tp_req.x = float(x)
        self.tp_req.y = float(y)
        self.tp_req.theta = float(theta)
        self.get_logger().info('params set, teleporting...')
        self.future = self.tp_abso.call_async(self.tp_req)
        self.get_logger().info('done')

    def pen_request(self, off):
        if off == True:
            self.pen.off = 255
        else:
            self.pen.off = 0
        self.get_logger().info('pen status set, changing...')
        self.future = self.pen_cli.call_async(self.pen)
        self.get_logger().info('done')

def main(args=None):
    rclpy.init(args=args)

    hw4_1_controller = DemoPublisher()
    hw4_1_controller.get_logger().info('setting pen')
    hw4_1_controller.pen_request(True)
    hw4_1_controller.get_logger().info('set')
    while rclpy.ok():
        rclpy.spin_once(hw4_1_controller)
        hw4_1_controller.get_logger().info('pen service not processed waiting...')
        if hw4_1_controller.future.done():
            break

    rclpy.spin(hw4_1_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    hw4_1_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
