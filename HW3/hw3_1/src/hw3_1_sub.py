from random import randint
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt32, UInt32MultiArray, String


#Subscribe to the topics topic_1 and topic_2
#For each incoming message of the same serial number, merge the lists of numbers and sort the result
#Print to the console the serial number of the message (on one line) and the merged and sorted list of numbers ((on next line))

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription_1 = self.create_subscription(String,'topic_1',self.listener_callback,10)
        self.subscription_2 = self.create_subscription(String,'topic_2',self.listener_callback,10)
        self.subscription_1  # prevent unused variable warning
        self.subscription_2  # prevent unused variable warning
        self.publisher_3 = self.create_publisher()
        self.L1_recieved = False
        self.L1 = []
        self.L2_recieved = False
        self.L2 = []
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        merged = UInt32MultiArray()
        merged = []
        if not self.L1_recieved:
            self.L1 = msg.data
            self.L1_recieved = True
        if self.L1_recieved and not self.L2_recieved:
            self.L2 = msg.data
            self.L2_recieved = True
        if self.L1_recieved and self.L2_recieved:
            # check if both are same serial number before merging
            if self.L1[0] == self.L2[0]:
                serial = self.L1[0]
                merged = listSort(self.L1[1:] + self.L2[1:])
                merged.insert(0,serial)
                self.L1_recieved = False
                self.L2_recieved = False
                self.publisher_3.publish(merged)
                self.get_logger().info(f"Subscriber: Recieved list from serial number {serial}\nSubscriber: Sorted list of numbers is: {merged[1:]}")
            else:
                self.get_logger().info("Subscriber: Something broke and I can't merge the lists")
        

# Mergesort from HW 2
def listSort(list):
    """Takes in a list of integers and sorts it using a merge sort method"""
    if len(list) <= 1:
        return list
    # divide the list into n sublists where n is the length of the list
    # i.e. compare sublist 1 with sublist 2, 3 with 4, etc
    leftSplit = list[:(len(list)//2)]
    rightSplit = list[((len(list)//2)):]
    leftSplit = listSort(leftSplit)
    rightSplit = listSort(rightSplit)
    return merge(leftSplit, rightSplit)

def merge(leftSplit, rightSplit):
    # merge and sort the lists
    sortedList = []
    while len(leftSplit) > 0 and len(rightSplit) > 0:
        if leftSplit[0] >= rightSplit[0]:
            sortedList.append(rightSplit[0])
            rightSplit = rightSplit[1:]
        else: # this means that left is less than right
            sortedList.append(leftSplit[0])
            leftSplit = leftSplit[1:]
    if len(leftSplit) == 0:
        # Rightsplit still has elements
        sortedList = sortedList + rightSplit
    if len(rightSplit) == 0:
        # leftSplit still has elements
        sortedList = sortedList + leftSplit
    return sortedList

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
