from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('simple_robot_gripper')
    xacro_file = os.path.join(pkg_path, 'urdf', 'simple_robot_gripper_gz.xacro')
    controllers_file = os.path.join(pkg_path, 'config', 'controllers.yaml')
    world_file = os.path.join(pkg_path, 'worlds', 'gazebo.world')

    robot_description = {'robot_description': Command([FindExecutable(name='xacro'), ' ', xacro_file])}

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '--headless-rendering', world_file],  # kein Fenster
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}],
    )

    spawn_entity = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                output='screen',
                arguments=['-name', 'simple_robot_gripper', '-topic', 'robot_description', '-z', '0.5'],
            )
        ]
    )

    jsb_spawner = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                output='screen',
            )
        ]
    )

    arm_spawner = TimerAction(
        period=9.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['arm_controller', '--controller-manager', '/controller_manager'],
                output='screen',
            )
        ]
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        jsb_spawner,
        arm_spawner,
    ])
