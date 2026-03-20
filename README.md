A ROS 2 Jazzy demo featuring a 4-DOF robot arm controlled via natural German language commands using a Groq/LLaMA LLM.

## Architecture
```
ros_core container          ai_controller container
├── robot_state_publisher   └── move_robot.py
├── controller_manager            └── Groq API (LLaMA 3.3 70B)
├── joint_state_broadcaster
└── arm_controller
```

Both containers communicate via ROS 2 DDS over `network_mode: host`.

## Prerequisites

- ROS 2 Jazzy
- Docker & Docker Compose (for headless, otherwise no need)
- Groq API key (is free wink wink)→ [console.groq.com](https://console.groq.com)

## Quick Start (Local)
```bash
cd ./gaztest
colcon build --packages-select simple_robot_gripper
source install/setup.bash

# Terminal 1 – Visualization
ros2 launch simple_robot_gripper display.launch.py (Rviz2)
ros2 launch simple_robot_gripper gazebo.launch.py (Gazebo)

# Terminal 2 – LLM Controller
source .venv/bin/activate 
export GROQ_API_KEY=your_key 
python3 src/simple_robot_gripper/scripts/move_robot.py
```

For Gazebo simulation:
```bash
ros2 launch simple_robot_gripper gazebo.launch.py
```

If nodes behave unexpectedly, kill stale processes first:
```bash
pkill -f robot_state_publisher && pkill -f controller_manager && pkill -f spawner
```

## Docker
```bash
# Create .env file
echo "GROQ_API_KEY=your_key" > .env

# Build and start
docker compose -f docker/docker-compose.yml up -d

# Attach to interactive prompt
docker attach docker-ai_controller-1

# Stop
docker compose -f docker/docker-compose.yml down
```

## Example Commands
(You can change the prompt to follow whatever language the model supports)
| German Input | Action |
|---|---|
| `Drehe joint1 auf 1.0` | Rotate arm left/right |
| `Bewege joint2 auf 0.5` | Tilt arm up/down |
| `Dreh den Arm` | Rotates arm|
| `Greife etwas links von dir` | Full pick sequence |

## Project Structure
```
src/simple_robot_gripper/
├── urdf/          # URDF for RViz2 (mock) and Gazebo (gz_ros2_control)
├── launch/        # display, gazebo, headless_rviz, headless_gz
├── config/        # controllers.yaml (joint_trajectory_controller)
├── scripts/       # move_robot.py, llm_agent.py, robot_contoller.py
└── rviz/          # RViz2 config
docker/
├── Dockerfile.ros_core
├── Dockerfile.ai_controller
└── docker-compose.yml
```

## Notes

- `.env` is gitignored — never hardcode API keys
- Visualization (RViz2/Gazebo) runs locally; containers run headless
- `ros_core` uses `mock_components/GenericSystem` — no real hardware needed
