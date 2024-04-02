import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from turtlesim.srv import SetPen
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from random import uniform

class spawnerNode(Node):

    def __init__(self):
        super().__init__('hw4_3_spawner')
        # grab params from launch file
        self.declare_parameter("timer", rclpy.Parameter.Type.INTEGER)
        self.declare_parameter("obstacles", rclpy.Parameter.Type.INTEGER)
        self.timer_period = self.get_parameter("timer").value
        # change this to alter the amount of goals that are already present when
        # the nodes are initialized
        self.initial_goals = 2
        
        # create counters for turtle naming
        self.goal_counter = 1
        self.obst_counter = 1
        
        # create strings that will hold array data
        self.aliveArray = String()
        self.obstArray = String()

        # creating publisher for alive turtles
        self.alive_goals=self.create_publisher(String, "/alive_turtles", 10)
        # creating publisher for list of obstacles
        self.obstacles_pub=self.create_publisher(String, "/obstacles", 10)
        # creating kill service
        self.catch_cli = self.create_service(Kill, "/catch_turtle", 
                                             self.catch_callback)

        # create spawn client
        self.spawner = self.create_client(Spawn, "/turtlesim1/spawn")
        while not self.spawner.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawner service not available, waiting...')
        self.spawnRq = Spawn.Request()
        
        # create kill client
        self.killer = self.create_client(Kill, "/turtlesim1/kill")
        while not self.killer.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Killer service not available, waiting...')        
        self.killRq = Kill.Request()

        # create timer for spawining more goals
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
    def spawn(self, goal=True):
        # spawns a new turtle onto the field, if goal is true it will be a goal 
        # turtle, if false it will be treated as an obstacle

        # randomize x and y position of turtle
        self.spawnRq.x = uniform(1,10)
        self.spawnRq.y = uniform(1,10)
        self.spawnRq.theta = 0.0
        if goal: # creating a goal turtle
            # make its name definite for clarity
            self.spawnRq.name = f"goal_{self.goal_counter}" 
            self.goal_counter += 1 # update turtle counter
            # call spawning service
            self.future = self.spawner.call_async(self.spawnRq) 
            # update the alive turtles data
            self.aliveArray.data = (self.aliveArray.data 
                                    + f"|{self.spawnRq.name},{self.spawnRq.x},{self.spawnRq.y},{self.spawnRq.theta}")
            self.alive_goals.publish(self.aliveArray)
        else: # its an obstacle
            self.spawnRq.name = f"obst_{self.obst_counter}" # make its name definite for clarity
            self.obst_counter += 1 # update counter
            self.future = self.spawner.call_async(self.spawnRq) # call spawner service
            # update array data
            self.obstArray.data = (self.obstArray.data 
                                    + f"|{self.spawnRq.name},{self.spawnRq.x},{self.spawnRq.y},{self.spawnRq.theta}")
            self.obstacles_pub.publish(self.obstArray)
    
    def kill_request(self, name):
        # kills a turtle of a given name, and logs it with level info
        self.killRq.name = name
        self.get_logger().info(f"Killing {name}...")
        self.future = self.killer.call_async(self.killRq)
        self.get_logger().info('Catch confirmed')

    def catch_callback(self, request, response):
        # responds to a catch request by forwarding name to the kill service 
        # and updating the alive array
        self.kill_request(request.name)
        # find and remove from alive array
        workArr = self.aliveArray.data.split("|")
        for sublist in workArr:
            sublist.split(",")
        for idx, sublist in enumerate(workArr,0):
            for part in sublist.split(","):
                if part == request.name: # name
                    self.get_logger().info('Matched name')
                    del workArr[idx]
        # reassemble and publish
        workStr = ""
        for sublist in workArr:
            sublist = ",".join(sublist)
        workStr = "|".join(workArr)
        self.aliveArray.data = workStr
        self.alive_goals.publish(self.aliveArray)
        
        # return a response, even if none, to keep spinning
        return response
    
    def timer_callback(self):
        # spawn on the specified timer
        self.spawn()
    

def main(args=None):
    rclpy.init(args=args)
    # create node
    hw4_3_spawn = spawnerNode()
    # figure out how many obstacles we wanted
    hw4_3_spawn.num = hw4_3_spawn.get_parameter("obstacles").value
    # spawn obstacles
    for i in range(0, hw4_3_spawn.num):
        hw4_3_spawn.spawn(goal=False)
    # spawn starting goals
    for i in range(0, hw4_3_spawn.initial_goals):
        hw4_3_spawn.spawn()

    # spin to win
    rclpy.spin(hw4_3_spawn)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    hw4_3_spawn.destroy_node()
    rclpy.shutdown()

if __name__ in "__main__":
    main()

        