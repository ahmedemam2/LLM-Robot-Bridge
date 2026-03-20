#!/usr/bin/env python3
import time

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class ArmTestNode(Node):
    def __init__(self):
        super().__init__('arm_test_node')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        time.sleep(1)  # kurz warten, bis alles gestartet ist

    def move_joints(self, joint_names, positions, duration_sec):
        traj = JointTrajectory()
        traj.joint_names = joint_names
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = int(duration_sec)
        point.time_from_start.nanosec = int((duration_sec - int(duration_sec)) * 1e9)
        traj.points.append(point)
        self.pub.publish(traj)
        self.get_logger().info(f"Published trajectory: {joint_names} -> {positions}")
        time.sleep(duration_sec + 0.5)  # warten bis Bewegung abgeschlossen
