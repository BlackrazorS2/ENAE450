William Bauer 117987676
Questions attempted:
1, 2, 3 with bonuses
In order to run question 1, source ros and run
ros2 launch hw4_1 hw4_1_launch.py

In order to run question 2, source ros and run
ros2 launch hw4_2 hw4_2_launch.py

In order to run question 3, source ros and run
ros2 launch hw4_3 hw4_3_launch.py

you can configure the environment for question 3 to check the
original question and its bonuses by changing the parameters in the
launch file.

For bonus 1, respawning if it hits any walls, you can set the parameter
"respawning" to True under the node named "controller"

For bonus 2, selecting the closest turtle instead of the first turtle,
you can set the parameter "closest" to True under the node named "controller"

For bonus 3, you can define the number of obstacle turtles present by using the "obstacles" parameter under the node named "spawner"
You can check the placement of the obstacles as they are spawned initially, their names are obst_NUMBER

The configuration that the launch file was submitted in was:
respawning: True
closest: True
timer: 10
obstacles: 2
