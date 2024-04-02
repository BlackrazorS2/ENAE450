import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Kill
from turtlesim.msg import Pose
from time import sleep
import math

class controlNode(Node):

    def __init__(self):
        super().__init__('hw4_3_controller')
        # grab params from launch file
        self.declare_parameter("respawning", rclpy.Parameter.Type.BOOL)
        self.declare_parameter("closest", rclpy.Parameter.Type.BOOL)
        
        

        # publish to cmd_vel to control turtle velocity
        self.publisher_vel = self.create_publisher(Twist, 
                                                   '/turtlesim1/turtle1/cmd_vel',
                                                     10)

        # subscribe to alive_turtles to get where alive goals are, and obstacles to find obstacles
        self.alive_sub = self.create_subscription(String, 
                                                  "/alive_turtles", 
                                                  self.alive_callback, 
                                                  10)
        self.obst_sub = self.create_subscription(String, 
                                                 "/obstacles", 
                                                 self.obstacle_callback, 
                                                 10)
        self.aliveList = []
        self.obstList = []
        self.goal_x = 0
        self.goal_y = 0
        self.goal_delta = 0
        self.goal_name = ""

        # create the catch client, which will kill turtles when we reach them
        self.catch_cli = self.create_client(Kill, "/catch_turtle")
        while not self.catch_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Catch turtle service not available, waiting...')
        self.catching = Kill.Request()

        # make a client for the SetPen so we can lift pen at start
        self.pen_cli = self.create_client(SetPen, "/turtlesim1/turtle1/set_pen")
        while not self.pen_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('pen service not available, waiting...')
        self.pen = SetPen.Request()

        # make a client to respawn when hitting a wall
        self.tp_abso = self.create_client(TeleportAbsolute, 
                                          "/turtlesim1/turtle1/teleport_absolute")
        while not self.tp_abso.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('tp service not available, waiting...')
        self.tp_req = TeleportAbsolute.Request()

        # subscribe to the postition topic to see where we are
        self.pose_sub = self.create_subscription(Pose, 
                                                 "/turtlesim1/turtle1/pose", 
                                                 self.pose_callback, 
                                                 10)
        # initial position
        self.pose_x = 5.5
        self.pose_y = 5.5
        self.pose_z = 0

    def move_request(self, x, y, theta):
        # teleports the turtle to a specified x y and theta
        self.tp_req.x = float(x)
        self.tp_req.y = float(y)
        self.tp_req.theta = float(theta)
        self.future = self.tp_abso.call_async(self.tp_req)
        self.get_logger().info('done')

    def pen_request(self, off):
        # raises or lowers the pen
        if off == True:
            self.pen.off = 255
        else:
            self.pen.off = 0
        self.get_logger().info('pen status set, changing...')
        self.future = self.pen_cli.call_async(self.pen)
        self.get_logger().info('done')

    def pose_callback(self, msg):
        # gets the current position of the main turtle
        self.pose_x = msg.x
        self.pose_y = msg.y
        self.pose_z = msg.theta

    def alive_callback(self, msg):
        # retrives the most up to date list of alive turtles
        # it's retrieved as a string so we have to break it up and parse
        # it into a list for easy comprehension
        workArr = msg.data.split("|")
        self.aliveList = []
        for sublist in workArr:
            temp = sublist.split(",")
            self.aliveList.append(temp)
        # each sublist is a name, x, y, and theta
        if self.aliveList[0][0] == '':
            del self.aliveList[0]
        self.get_logger().info(f"Current alive list: {self.aliveList}")
    
    def obstacle_callback(self, msg):
        # retrives the most up to date list of obstacle turtles
        # it's retrieved as a string so we have to break it up and parse
        # it into a list for easy comprehension
        workArr = msg.data.split("|")
        self.obstList = []
        for sublist in workArr:
            temp = sublist.split(",")
            self.obstList.append(temp)
        # each sublist is a name, x, y, and theta
        if self.obstList[0][0] == '':
            del self.obstList[0]

    def respawn(self):
        # wrapper for a teleport to the center of the screen for when the 
        # turtle hits a wall or obstacle
        self.move_request(5,5,self.goal_delta)

    def checkGoal(self):
        # compare current pose to all alive goals, 
        # if any are within a certain range, call the catch service
        for goal in self.aliveList:
            # calculate norm
            norm = math.sqrt(pow((float(goal[1])-self.pose_x),2)
                             +pow((float(goal[2])-self.pose_y),2))
            if norm <= 1.3:
                self.catching.name = goal[0]
                self.future = self.catch_cli.call_async(self.catching)
                
    
    def checkObst(self):
        # compare current pose to all alive obstacles
        # if there are any in a certain range, try to avoid them
        # if they are especially close, we hit it and have to respawn
        for obst in self.obstList:
            norm = math.sqrt(pow((float(obst[1])-self.pose_x),2)
                             +pow((float(obst[2])-self.pose_y),2))
            if norm <= 1.3 and norm >= 1.2:
                evade = Twist()
                evade.linear.x = 1.0
                evade.angular.z = 1.0
                self.publisher_vel.publish(evade)
                sleep(.1)
            if norm < 1:
                self.get_logger().info("Hit an obstacle! Respawning...")        
                self.respawn()
                sleep(1)
    
    def setTarget(self):
        select_closest = self.get_parameter("closest").value
        if select_closest == True:
            # find closest by comparing euclidean norm of each goal turtle
            close_norm = 10000000
            for goal in self.aliveList:
                norm = math.sqrt(pow((float(goal[1])-self.pose_x),2)
                                 +pow((float(goal[2])-self.pose_y),2))
                if norm < close_norm:
                    if self.goal_name != goal[0]:
                        self.goal_name = goal[0]
                    self.goal_x = float(goal[1])
                    self.goal_y = float(goal[2])
                    y_dist = self.goal_y - self.pose_y
                    x_dist = self.goal_x - self.pose_x
                    self.goal_delta = math.atan(y_dist/x_dist)
                    # map to the proper quadrant since atan is pi/2 to -pi/2
                    if (x_dist<0 and y_dist>0) or (x_dist<0 and y_dist<0):
                        self.goal_delta += math.pi
            
        else:
            # just get first in array
            if len(self.aliveList) > 0: # if there are targets
                if self.goal_name != self.aliveList[0][0]:
                    self.goal_name = self.aliveList[0][0]
                self.goal_x = float(self.aliveList[0][1])
                self.goal_y = float(self.aliveList[0][2])
                # do some trig to find the angle between
                y_dist = self.goal_y - self.pose_y
                x_dist = self.goal_x - self.pose_x
                self.goal_delta = math.atan(y_dist/x_dist)
                # map to the proper quadrant since atan is pi/2 to -pi/2
                if (x_dist<0 and y_dist>0) or (x_dist<0 and y_dist<0):
                    self.goal_delta += math.pi

    def nav(self):
        # one iteration of navigating checks for goals and handles moving in
        # relation to the target

        # make sure we are in bounds
        respawning_allowed = self.get_parameter("respawning").value
        if (((self.pose_x>=10.5 or self.pose_y>=10.5) 
            or (self.pose_x<=0.5 or self.pose_y<=0.5)) 
            and respawning_allowed):

            self.get_logger().info("Respawning...")    
            self.respawn()
            sleep(1)


        movement = Twist()
        # update targeting
        self.setTarget()
        
        # decide which direction we should turn in:
        if self.pose_z - self.goal_delta < 0:
            # adjust angle
            movement.linear.x = 1.0
            movement.angular.z = 1.0 # move at 1 rad/s
            self.publisher_vel.publish(movement)
            sleep(.1)
        if self.pose_z - self.goal_delta > 0:
            # adjust angle
            movement.linear.x = 1.0
            movement.angular.z = -1.0 # move at 1 rad/s
            self.publisher_vel.publish(movement)
            sleep(.1)
        else:
            movement.linear.x = 1.0
            movement.angular.z = 0.0
            self.publisher_vel.publish(movement)
            sleep(1)
        self.checkGoal()
        self.checkObst()



def main(args=None):
    rclpy.init(args=args)
    # create node
    hw4_3_control = controlNode()
    # left up pen so we're not leaving a trail everywhere
    hw4_3_control.get_logger().info('setting pen')
    hw4_3_control.pen_request(True)
    hw4_3_control.get_logger().info('set')

    while rclpy.ok():
        rclpy.spin_once(hw4_3_control)
        hw4_3_control.get_logger().info('pen service not processed waiting...')
        if hw4_3_control.future.done():
            break
    # set an initial target
    hw4_3_control.setTarget()
    # spin to win
    while True:
        rclpy.spin_once(hw4_3_control)
        hw4_3_control.nav()
        rclpy.spin_once(hw4_3_control)


if __name__ in "__main__":
    main()