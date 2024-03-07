import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32, UInt32MultiArray

class HW31Publisher(Node):
    def __init__(self):
        super().__init__("hw_3_1_publisher_node")
        self.publisher_=self.create_publisher(UInt32MultiArray, "topic_1", 10)
        timer_period = 2
        self.serial = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
    def timer_callback(self):
        msg = UInt32MultiArray()
        msg.data = [self.serial]
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")
        self.serial += 1

def main(args=None):
    rclpy.init(args=args)
    
    hw_3_1_publisher = HW31Publisher()

    rclpy.spin(hw_3_1_publisher)

    hw_3_1_publisher.destroy_node()
    rclpy.shutdown()



    node = rclpy.create_node("hw_3_1_publisher_node")
    publisher = node.create_publisher(UInt32MultiArray, "topic_1", 10)
    serial = 1
    timer_period = 2
    node.create_timer(timer_period, node.timer_callback)
        # while the node is running
        # Should operate at a freq of .5 Hz = every 2 seconds
        # make list of integers from 0 to 100
        # append serial number of message to begining
        # publish on topic_1 and topic_2

if __name__ == "__main__":
    main()