#!/usr/bin/env python3
import json
import os
import urllib.request


class GroqChatWithMemory:
    """
    Einfaches Memory für Groq Cloud.
    Speichert vorherige User- und AI-Nachrichten.
    """
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY fehlt. Bitte als Umgebungsvariable setzen.")
        self.model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        # History: Liste von {"role": "user"/"assistant", "content": "..."}
        self.history = []

    def call_chat(self, prompt_text: str) -> dict:
        system_prompt = (
            "Du bist ein Parser für Robotik-Befehle. "
            "Eingabe ist Freitext auf Deutsch. "
            "Du musst die Gelenke bewegen, den Greifer öffnen/schließen oder einfach weiterbewegen. "
            "Benutze nur die Gelenke, die im JSON-Format unten erwähnt sind also nur joint1,joint2,left_finger_joint, right_finger_joint. "
            "Gib als Ausgabe ausschließlich JSON im folgenden Format zurück:\n"
            "{\n"
            "  \"steps\": [\n"
            "    {\"joint_names\": [\"joint1\"], \"positions\": [1.0], \"duration_sec\": 1.0},\n"
            "    {\"joint_names\": [\"joint2\"], \"positions\": [1.0], \"duration_sec\": 1.0},\n"
            "    {\"joint_names\": [\"left_finger_joint\",\"right_finger_joint\"], "
            "\"positions\": [0.04,0.04], \"duration_sec\": 1.0}\n"
            "  ]\n"
            "}\n"
            "Keine zusätzlichen Wörter, keine Markdown-Blöcke."
        )

        # Füge User-Input zur History hinzu
        self.history.append({"role": "user", "content": prompt_text})

        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}] + self.history,
            "temperature": 0.1,
        }

        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            # Füge AI-Output ebenfalls ins Memory ein
            self.history.append({"role": "assistant", "content": content})
            return json.loads(content)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise RuntimeError(f"HTTP Fehler {e.code}: {error_body}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON Parse Fehler: {e}")


def validate_steps(plan):
    if "steps" not in plan or not isinstance(plan["steps"], list):
        raise ValueError("Antwort enthält kein gültiges 'steps' Array.")

    for i, step in enumerate(plan["steps"], start=1):
        if not isinstance(step, dict):
            raise ValueError(f"Schritt {i} ist kein Objekt.")
        if "joint_names" not in step or "positions" not in step or "duration_sec" not in step:
            raise ValueError(f"Schritt {i} fehlt Pflichtfelder.")
        if not isinstance(step["joint_names"], list) or not isinstance(step["positions"], list):
            raise ValueError(f"Schritt {i} hat ungültige Listen.")
        if len(step["joint_names"]) != len(step["positions"]):
            raise ValueError(f"Schritt {i}: joint_names und positions haben unterschiedliche Längen.")
        if not isinstance(step["duration_sec"], (int, float)):
            raise ValueError(f"Schritt {i}: duration_sec ist keine Zahl.")
