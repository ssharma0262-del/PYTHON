import ollama


def ask_ollama(prompt):

    try:

        response = ollama.chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful voice assistant named Hello. Give short, clear and simple answers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        print("Ollama Error:", e)

        return "Sorry, I am having trouble connecting to my AI model."


if __name__ == "__main__":

    answer = ask_ollama("What is coding?")

    print("\nAI:")
    print(answer)