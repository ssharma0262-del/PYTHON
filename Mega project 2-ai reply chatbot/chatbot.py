import requests

def ask_ai(message):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3:4b",
                "prompt": message,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()

        data = response.json()
        return data["response"]

    except Exception as e:
        return f"Error: {e}"


message = "Hello"
reply = ask_ai(message)

print("AI Reply:")
print(reply)