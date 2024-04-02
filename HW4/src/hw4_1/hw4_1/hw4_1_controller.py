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
        # create velocity publisher
        self.publisher_vel = self.create_publisher(Twist,
                                                    '/turtlesim1/turtle1/cmd_vel', 
                                                    10)
        # create pen and tp clients
        self.pen_cli = self.create_client(SetPen, 
                                          "/turtlesim1/turtle1/set_pen")
        while not self.pen_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('pen service not available, waiting...')
        self.tp_abso = self.create_client(TeleportAbsolute, 
                                          "/turtlesim1/turtle1/teleport_absolute")
        while not self.tp_abso.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('tp service not available, waiting...')
        self.pen = SetPen.Request()
        self.tp_req = TeleportAbsolute.Request()

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

    def drawTriange(self):
        msg = Twist()
        # draw bottom
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)
        #stop
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        # spin to draw next side
        msg.angular.z = 3*math.pi/4
        self.publisher_vel.publish(msg)
        sleep(1)
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)

        # draw side
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)
        #stop
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        # spin to draw next side
        msg.angular.z = 2.0
        self.publisher_vel.publish(msg)
        sleep(1)
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)

        # draw side
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(.75)
        #stop
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        # spin to be back at the start
        msg.angular.z = 3*math.pi/4
        self.publisher_vel.publish(msg)
        sleep(1)
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)

    def drawSquare(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)

        msg.linear.x = 0.0
        msg.angular.z = math.pi/2
        self.publisher_vel.publish(msg)
        sleep(1)

        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)

        msg.linear.x = 0.0
        msg.angular.z = math.pi/2
        self.publisher_vel.publish(msg)
        sleep(1)


        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)

        msg.linear.x = 0.0
        msg.angular.z = math.pi/2
        self.publisher_vel.publish(msg)
        sleep(1)

        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)

        msg.linear.x = 0.0
        msg.angular.z = math.pi/2
        self.publisher_vel.publish(msg)
        sleep(1)

    def drawDecagon(self):
        msg = Twist()
        for i in range(0,10):
            msg.linear.x = 1.0
            self.publisher_vel.publish(msg)
            sleep(1)
            msg.linear.x = 0.0
            msg.angular.z = 36*math.pi/180
            self.publisher_vel.publish(msg)
            sleep(1)
            msg.angular.z = 0.0
            self.publisher_vel.publish(msg)
            sleep(1)

    def drawCricle(self):
        msg = Twist()
        msg.linear.x = 4.0
        msg.angular.z = 2*math.pi
        self.publisher_vel.publish(msg)
        sleep(1)
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_vel.publish(msg)
        sleep(1)

    def setPen(self, off):
        pass
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
    hw4_1_controller.get_logger().info('teleporting')
    hw4_1_controller.move_request(1, 1,0)
    hw4_1_controller.get_logger().info('done')
    sleep(1)
    while rclpy.ok():
        rclpy.spin_once(hw4_1_controller)
        hw4_1_controller.get_logger().info('tp service not processed waiting...')
        if hw4_1_controller.future.done():
            break
    hw4_1_controller.get_logger().info('setting pen again')
    hw4_1_controller.pen_request(False)
    hw4_1_controller.get_logger().info('set')
    while rclpy.ok():
        rclpy.spin_once(hw4_1_controller)
        hw4_1_controller.get_logger().info('pen service not processed waiting...')
        if hw4_1_controller.future.done():
            break
    hw4_1_controller.get_logger().info('drawing triangle')
    hw4_1_controller.drawTriange()
    hw4_1_controller.get_logger().info('done')

    hw4_1_controller.pen_request(True)
    hw4_1_controller.move_request(1,7,0)
    hw4_1_controller.pen_request(False) 

    hw4_1_controller.drawSquare()

    hw4_1_controller.pen_request(True)
    hw4_1_controller.move_request(7,7,0)
    hw4_1_controller.pen_request(False)

    hw4_1_controller.drawDecagon() 

    hw4_1_controller.pen_request(True)
    hw4_1_controller.move_request(8,1,0)
    hw4_1_controller.pen_request(False)

    hw4_1_controller.drawCricle()
    rclpy.spin(hw4_1_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    hw4_1_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
