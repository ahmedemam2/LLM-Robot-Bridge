from setuptools import find_packages, setup

package_name = 'simple_robot_gripper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/simple_robot_gripper']),
    ('share/simple_robot_gripper', ['package.xml']),
    ('share/simple_robot_gripper/launch', ['launch/gazebo.launch.py',
                                           'launch/display.launch.py', 
                                           'launch/headless_rviz.launch.py',
                                           'launch/headless_gz.launch.py']),
    ('share/simple_robot_gripper/urdf', ['urdf/simple_robot_gripper.xacro',
                                         'urdf/simple_robot_gripper_gz.xacro']),
    ('share/simple_robot_gripper/config', ['config/controllers.yaml']),
    ('share/simple_robot_gripper/worlds', ['worlds/gazebo.world']),
    ('share/simple_robot_gripper/rviz', ['rviz/robot_config.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmed@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
