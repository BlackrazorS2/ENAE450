from random import randint
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32, UInt32MultiArray


class HW31Publisher(Node):
    def __init__(self):
        super().__init__("hw_3_1_publisher_node")
        self.publisher_1=self.create_publisher(UInt32MultiArray, "topic_1", 10)
        self.publisher_2=self.create_publisher(UInt32MultiArray, "topic_2", 10)
        timer_period = 2
        self.serial = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
    def timer_callback(self):
        msg_1 = UInt32MultiArray()
        msg_2 = UInt32MultiArray()
        msg_1.data = [self.serial]
        msg_2.data = [self.serial]
        for i in range(0,10):
            num = randint(0, 101)
            msg_1.data.append(num)
        for i in range(0,10):
            num = randint(0, 101)
            msg_2.data.append(num)
        self.publisher_1.publish(msg_1)
        self.publisher_2.publish(msg_2)
        self.get_logger().info(f"NODE_PUB [topic_1]: Publish -> {msg_1.data}")
        self.get_logger().info(f"NODE_PUB [topic_2]: Publish -> {msg_2.data}\n")
        self.serial += 1

def main(args=None):
    rclpy.init(args=args)
    
    hw_3_1_publisher = HW31Publisher()

    rclpy.spin(hw_3_1_publisher)

    hw_3_1_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()