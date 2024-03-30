from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='sim'
        ),
       Node(
            package='hw4_1',
            namespace='turtlesim1',
            executable='hw4_1_controller',
            name='controller'
        ),
#        Node(
#            package='turtlesim',
#            executable='mimic',
#            name='mimic',
#            remappings=[
#                ('/input/pose', '/turtlesim1/turtle1/pose'),
#                ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
#            ]
#        ) 
    ])