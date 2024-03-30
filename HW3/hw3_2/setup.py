from setuptools import find_packages, setup

package_name = 'hw3_2'

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
    maintainer='proving_ground_home',
    maintainer_email='williambauer00@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hw3_2_pub = hw3_2.hw3_2_pub:main',
            'hw3_2_sub = hw3_2.hw3_2_sub:main',
        ],
    },
)
