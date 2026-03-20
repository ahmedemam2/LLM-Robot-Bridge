#!/usr/bin/env python3
import json

import rclpy

from robot_contoller import ArmTestNode
from llm_agent import GroqChatWithMemory, validate_steps


def main(args=None):
    rclpy.init(args=args)
    node = ArmTestNode()
    chat_memory = GroqChatWithMemory()

    try:
        while True:
            try:
                prompt_text = input("\nGib deinen Roboter-Prompt ein (oder 'ctrl + c' zum Beenden): ").strip()
                if prompt_text.lower() in ['exit', 'quit', 'q']:
                    print("Beende Programm...")
                    break
                if not prompt_text:
                    print("Leerer Prompt. Bitte Text eingeben.")
                    continue

                print("Sende Anfrage an Groq API mit Memory...")
                plan = chat_memory.call_chat(prompt_text)
                print(f"Erhaltener Plan: {json.dumps(plan, indent=2)}")

                validate_steps(plan)
                print(f"Führe {len(plan['steps'])} Schritte aus...")

                for i, step in enumerate(plan["steps"], start=1):
                    print(f"Schritt {i}/{len(plan['steps'])}: {step['joint_names']}")
                    node.move_joints(
                        step["joint_names"],
                        step["positions"],
                        duration_sec=step["duration_sec"],
                    )

                print("✓ Alle Schritte erfolgreich ausgeführt!")

            except KeyboardInterrupt:
                print("\n\nProgramm mit Ctrl+C beendet.")
                break
            except Exception as e:
                print(f"Fehler: {e}")

    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
