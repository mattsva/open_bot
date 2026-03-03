# utils/ai.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
import ollama
import subprocess
from config import Meta


class Ollama:
    _process = None

    @staticmethod
    def startup() -> None:
        if Ollama._process is not None:
            return  # already started
        try:
            Ollama._process = subprocess.Popen( # Start ollama with `ollama serve`
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            raise RuntimeError(
                f"Ollama startup failed. Ensure `ollama` is installed and in PATH. Error: `{e}`"
            )

    @staticmethod
    def ai(content: str) -> str:
        if not isinstance(content, str):
            raise TypeError("Ollama.ai expects a string input.")

        if not isinstance(Meta.ai_messages, list): # ensure message history is a list
            raise TypeError("Meta.ai_messages must be a list.")

        Meta.ai_messages.append({ # append user message
            "role": "user",
            "content": content
        })

        response = ollama.chat(
            model=Meta.ai_model,
            messages=Meta.ai_messages
        )

        assistant_content = response["message"]["content"]

        Meta.ai_messages.append({
            "role": "assistant",
            "content": assistant_content
        })

        return assistant_content

# TODO:
# - Add model change
# - Add more AI systems
# - - Add GPT4ALL integration