from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('simple_robot_gripper')
    xacro_file = os.path.join(pkg_path, 'urdf', 'simple_robot_gripper.xacro')
    rviz_file  = os.path.join(pkg_path, 'rviz', 'robot_config.rviz')
    controllers_file = os.path.join(pkg_path, 'config', 'controllers.yaml')

    robot_description = {'robot_description': Command([FindExecutable(name='xacro'), ' ', xacro_file])}

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            output='screen',
            parameters=[robot_description, controllers_file]
        ),
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
            output='screen'
        ),
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['arm_controller', '--controller-manager', '/controller_manager'],
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_file],
            output='screen'
        )
    ])