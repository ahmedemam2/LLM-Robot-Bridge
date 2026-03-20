from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable
from pathlib import Path
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_path = get_package_share_directory('simple_robot_gripper')
    xacro_file = os.path.join(pkg_path, 'urdf', 'simple_robot_gripper_gz.xacro')  
    controllers_file = os.path.join(pkg_path, 'config', 'controllers.yaml')  
    world_file = os.path.join(pkg_path, 'worlds', 'gazebo.world')
    robot_description = Command([FindExecutable(name='xacro'), ' ', xacro_file])  # ✅

    # 1. Gazebo starten (sofort)
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )

    # 2. Robot State Publisher (sofort)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
    )

    # 3. Roboter spawnen (nach 3 Sekunden)
    spawn_entity = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                output='screen',
                arguments=[
                    '-name', 'simple_robot_gripper',
                    '-topic', 'robot_description',
                    '-z', '0.5'
                ],
            )
        ]
    )

    # 4. Controller Manager (nach 5 Sekunden)
    control_node = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='controller_manager',
                executable='ros2_control_node',
                output='screen',
                parameters=[
                    {'robot_description': robot_description},
                    controllers_file,
                ],
            )
        ]
    )

    # 5. Joint State Broadcaster (nach 8 Sekunden)
    jsb_spawner = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'joint_state_broadcaster',
                    '--controller-manager', '/controller_manager'
                ],
                output='screen',
            )
        ]
    )

    # 6. Arm Controller (nach 9 Sekunden)
    arm_spawner = TimerAction(
        period=9.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'arm_controller',
                    '--controller-manager', '/controller_manager'
                ],
                output='screen',
            )
        ]
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        # control_node,
        jsb_spawner,
        arm_spawner,
    ])
