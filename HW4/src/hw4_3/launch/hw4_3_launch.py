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
            package='hw4_3',
            namespace='turtlesim1',
            executable='hw4_3_controller',
            name='controller',
            parameters=[
                {"respawning": True},
                {"closest": True},
            ]
        ),
        Node(
            package='hw4_3',
            namespace='turtlesim1',
            executable='hw4_3_spawner',
            name='spawner',
            parameters=[
                {"timer":10},
                {"obstacles": 2},
            ]
        ),

    ])