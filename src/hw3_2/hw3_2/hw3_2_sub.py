from random import randint
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32, UInt32MultiArray, String


#Subscribe to the topics topic_1 and topic_2
#For each incoming message of the same serial number, merge the lists of numbers and sort the result
#Print to the console the serial number of the message (on one line) and the merged and sorted list of numbers ((on next line))

class HW32Subscriber(Node):

    def __init__(self):
        super().__init__('hw3_2_sub')
        # set up subscriptions
        self.subscription_1 = self.create_subscription(UInt32MultiArray,'topic_1',self.topic_1_listener,10)
        self.subscription_2 = self.create_subscription(UInt32,'topic_2',self.topic_2_listener,10)
        self.subscription_1  # prevent unused variable warning
        self.subscription_2  # prevent unused variable warning
        # set up trackers so we know when we got data
        self.L1_recieved = False
        self.L1 = []
        self.L2_recieved = False
        self.L2 = 0

    def resolve(self):
        serial = self.L1[0]
        workstring = str(self.L2)
        strnum = workstring.replace(str(serial),"", 1) # deletes the serial number, we have to specify doing it once because we dont want to eliminate part of the number
        corrected_L2 = int(strnum)
        found = binSearch(self.L1, corrected_L2) # using the binary search function from HW because why not
        # you could do this with builtin functions by using index and some list shenanigans
        self.get_logger().info(f"NODE_SUB [INFO]: Received list and integer from PUB with serial: {serial}")
        self.get_logger().info(f"NODE_SUB [INFO]: Search parameter was: {corrected_L2}")
        self.get_logger().info(f"NODE_SUB [INFO]: Found?: {found}\n")

    def topic_1_listener(self, msg):
        self.L1 = msg.data
        self.L1_recieved = True
        self.get_logger().info(f"NODE_SUB [topic_1]: Receive <- {msg.data}")
        if self.L2_recieved and self.L1_recieved:
            self.L1_recieved = False
            self.L2_recieved = False
            self.resolve()
            self.L1 = []
            self.L2 = 0

    def topic_2_listener(self, msg):
        self.L2 = msg.data
        self.L2_recieved = True
        self.get_logger().info(f"NODE_SUB [topic_2]: Receive <- {msg.data}")
        if self.L2_recieved and self.L1_recieved:
            self.L1_recieved = False
            self.L2_recieved = False
            self.resolve()
            self.L1 = []
            self.L2 = 0

def binSearch(targetArray, searchValue):
    # does the binary search
    found = False
    while len(targetArray) >= 1:
        if searchValue == targetArray[len(targetArray)//2]:
            found = True
            break
        elif len(targetArray) == 1 and searchValue != targetArray[0]:
            # cant find it :(
            break
        elif searchValue > targetArray[len(targetArray)//2]:
            # searchValue is greater than middle of list, we want to check the right side
            targetArray = targetArray[(len(targetArray)//2):]
        elif searchValue < targetArray[len(targetArray)//2]:
            # searchValue is less than middle of list, we want to check the left side
            targetArray = targetArray[:(len(targetArray)//2)]
    return found

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = HW32Subscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
