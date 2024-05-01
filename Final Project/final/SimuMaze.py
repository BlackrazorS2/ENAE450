import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from time import sleep


class insideWallFollow(Node):
    

    def __init__(self):
        super().__init__("simuMaze")
                
        self.vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.scan_list = self.create_subscription(LaserScan, "/scan", self.scan_callback,10)
        self.side_dist = .4
        self.front_dist = .4
        self.turning = False
        self.completed = False
        #self.pace = 0.1 # sets how long to wait between publishes
        
    def scan_callback(self, msg):
        # for some reason in gazebo this ranges from 0 to 360, while in lab it ranges from 0 to 720
        
        adjust = Twist()
        rangeData = list(msg.ranges)
        mindist = min(rangeData)
        rdist = rangeData[260:280]
        ldist = rangeData[80:100]
        fdist = (rangeData[350:360]+rangeData[0:10])
        rdist = rangeData[170:190]
        rightdist = self.average(rdist)
        leftdist = self.average(ldist)
        frontdist = self.average(fdist)
        reardist = self.average(rdist)

        # logic idea
        # if we have walls on both sides and nothing in front, go straight
        # if we have a wall in front of us and nothing on the sides, turn in a direction
        # if we have a wall on only one side and nothingn in front, we can go straight
        # if we have wall in front and a 
        if not self.completed:
            if self.turning:
                if frontdist > 1:
                    adjust.angular.z = 0.0
                    adjust.linear.x = 0.0
                    self.vel_pub.publish(adjust)
                    self.turning = False
                else:
                    return None
            elif frontdist < self.front_dist:
                # make the turn
                adjust.linear.x = 0.0
                adjust.angular.z = 1.0
                self.vel_pub.publish(adjust)
                self.turning = True
            elif leftdist < self.side_dist and rightdist < self.side_dist:
                # need to squeeze, find the angle of minimum distance
                if abs(ldist.index(min(ldist))-90) < 2: # we can just go straight
                    adjust.angular.z = 0.0
                    adjust.linear.x = 0.2 
                else:   
                    adjust.angular.z = -0.1 * self.sign(ldist.index(min(ldist))-90)
                    adjust.linear.x = 0.2
                self.vel_pub.publish(adjust)
            elif leftdist < self.side_dist:
                adjust.angular.z = -0.1
                adjust.linear.x = 0.2
                self.vel_pub.publish(adjust)
            elif rightdist < self.side_dist:
                adjust.angular.z = 0.1
                adjust.linear.x = 0.2
                self.vel_pub.publish(adjust)
            elif leftdist > 1 and rightdist > 1:
                # we are out of the maze
                # turn 180
                adjust.linear.x = 0.0
                adjust.angular.z = 3.0
                self.vel_pub.publish(adjust)
                sleep(1)
                self.completed = True

    def sign(self, number):
        if number == 0:
            return 0
        elif number > 0:
            return 1
        elif number < 0:
            return -1

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