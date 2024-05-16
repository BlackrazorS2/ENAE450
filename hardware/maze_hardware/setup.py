from setuptools import find_packages, setup

package_name = 'maze_hardware'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='benloan',
    maintainer_email='benloan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "maze_solver = maze_hardware.maze_solver:main",
            "lidar_test = maze_hardware.lidar_test:main",
            "maze_hardware = maze_hardware.maze_hardware:main"
        ],
    },
)
