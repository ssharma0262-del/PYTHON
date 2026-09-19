from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import requests
import pyperclip
import time
import os
import json


# =========================
# SETTINGS
# =========================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:4b"

CHECK_INTERVAL = 2

# This keeps WhatsApp logged in between runs
PROFILE_PATH = os.path.join(os.getcwd(), "whatsapp-profile")


# =========================
# CLEAN AI REPLY
# =========================

def clean_ai_reply(reply):

    if not reply:
        return ""

    reply = reply.strip()

    # Remove thinking blocks if model sends them
    if "</think>" in reply:
        reply = reply.split("</think>")[-1].strip()

    reply = reply.replace("<think>", "")
    reply = reply.replace("</think>", "")

    # Try JSON first
    try:
        data = json.loads(reply)

        if isinstance(data, dict):
            reply = data.get("reply", "")

    except Exception:
        pass

    reply = str(reply).strip()

    # Remove common prefixes
    prefixes = [
        "Reply:",
        "AI Reply:",
        "Final answer:",
        "The reply is:",
        "So the reply is:",
        "Answer:"
    ]

    for prefix in prefixes:
        if reply.lower().startswith(prefix.lower()):
            reply = reply[len(prefix):].strip()

    # Keep only first line
    reply = reply.split("\n")[0].strip()

    # Remove unnecessary quotes
    if len(reply) >= 2:
        if (reply[0] == '"' and reply[-1] == '"') or \
           (reply[0] == "'" and reply[-1] == "'"):
            reply = reply[1:-1].strip()

    # Remove excessive spaces
    reply = " ".join(reply.split())

    # Reject instruction-like AI output
    bad_starts = [
        "we are instructed",
        "the user said",
        "the message says",
        "we need to",
        "the instruction",
        "i should",
        "i need to",
        "the reply should",
        "here is the reply",
        "here's the reply",
        "as an ai",
        "as an assistant",
        "i will",
        "i would",
        "the appropriate response",
        "the correct response"
    ]

    lower_reply = reply.lower()

    for bad in bad_starts:
        if lower_reply.startswith(bad):
            return ""

    return reply


# =========================
# ASK OLLAMA
# =========================

def ask_ai(message):

    message = message.strip()

    if not message:
        return ""

    print()
    print("Message received:", message)
    print("AI is generating a reply...")

    prompt = f"""
You are replying to a WhatsApp message.

IMPORTANT:
- Understand the actual message.
- Reply naturally like a normal person.
- Reply in ONE short sentence.
- Maximum 12 words.
- Do not explain the message.
- Do not mention instructions.
- Do not mention AI.
- Do not say "the user said".
- Do not provide reasoning.
- Output ONLY valid JSON.
- The JSON must contain only one field named "reply".

Example:
Message: Good night
Output: {{"reply":"Good night! Sleep well 😊"}}

Message: Kya kar rahe ho?
Output: {{"reply":"Bas bhai, thoda kaam kar raha hoon."}}

Now reply to this message:

{message}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {
                "reply": {
                    "type": "string"
                }
            },
            "required": ["reply"]
        },
        "keep_alive": "10m",
        "options": {
            "temperature": 0.2,
            "num_predict": 40
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        raw_reply = data.get("response", "").strip()

        print("Raw AI output:", raw_reply)

        reply = clean_ai_reply(raw_reply)

        if not reply:
            print("AI produced an invalid reply.")
            return ""

        print("Final reply:", reply)

        return reply

    except Exception as e:

        print("Ollama error:", e)

        return ""


# =========================
# CHECK OWN MESSAGE
# =========================

def is_own_message(element):

    try:

        # WhatsApp sometimes exposes this label
        own_elements = element.find_elements(
            By.CSS_SELECTOR,
            "[aria-label='You:']"
        )

        if own_elements:
            return True

    except Exception:
        pass

    return False


# =========================
# GET MESSAGES
# =========================

def get_messages(driver):

    messages = []

    try:

        elements = driver.find_elements(
            By.CSS_SELECTOR,
            "[data-testid^='conv-msg-']"
        )

        for element in elements:

            try:

                message_id = element.get_attribute("data-id")

                if not message_id:
                    continue

                # Find message text
                text = element.text.strip()

                if not text:
                    continue

                # Sender/time metadata
                sender_info = ""

                try:

                    meta = element.find_element(
                        By.CSS_SELECTOR,
                        "[data-pre-plain-text]"
                    )

                    sender_info = meta.get_attribute(
                        "data-pre-plain-text"
                    )

                except Exception:
                    pass

                own = is_own_message(element)

                messages.append({
                    "id": message_id,
                    "text": text,
                    "sender": sender_info,
                    "own": own
                })

            except Exception:
                continue

    except Exception as e:

        print("Message reading error:", e)

    return messages


# =========================
# FIND UNANSWERED MESSAGE
# =========================

def find_unanswered_message(messages):

    pending = None

    for message in messages:

        if message["own"]:

            pending = None

        else:

            pending = message

    return pending


# =========================
# SEND MESSAGE
# =========================

def send_message(driver, message):

    if not message:
        return False

    try:

        input_box = driver.find_element(
            By.CSS_SELECTOR,
            "#main footer [contenteditable='true']"
        )

        input_box.click()

        pyperclip.copy(message)

        input_box.send_keys(Keys.CONTROL, "v")

        time.sleep(0.5)

        input_box.send_keys(Keys.ENTER)

        time.sleep(3)

        # Verify message appeared
        recent_messages = get_messages(driver)

        for item in recent_messages[-5:]:

            if item["own"] and item["text"].strip() == message.strip():

                print("Reply sent successfully!")

                return True

        print("Reply could not be verified.")

        return False

    except Exception as e:

        print("Send message error:", e)

        return False


# =========================
# CREATE CHROME DRIVER
# =========================

def create_driver():

    options = webdriver.ChromeOptions()

    # Persistent profile
    options.add_argument(
        f"--user-data-dir={PROFILE_PATH}"
    )

    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        options=options
    )

    return driver


# =========================
# MAIN PROGRAM
# =========================

print()
print("Starting WhatsApp AI Auto Reply...")
print()

driver = None

try:

    driver = create_driver()

    driver.get("https://web.whatsapp.com")

    print("Opening WhatsApp Web...")

    time.sleep(15)

    print()
    print("If QR code appears, scan it once.")
    print("Then open the chat where you want auto-reply.")
    print()

    input("Open the selected chat and press ENTER...")

    time.sleep(3)

    # =========================
    # HANDLE OLD UNANSWERED MESSAGE
    # =========================

    print()
    print("Checking old unanswered messages...")

    messages = get_messages(driver)

    pending = find_unanswered_message(messages)

    if pending:

        print()
        print("Old unanswered message found:")
        print(pending["text"])

        reply = ask_ai(pending["text"])

        if reply:

            send_message(
                driver,
                reply
            )

    else:

        print("No old unanswered message found.")

    # =========================
    # REMEMBER EXISTING MESSAGES
    # =========================

    messages = get_messages(driver)

    processed_ids = set()

    for message in messages:

        processed_ids.add(
            message["id"]
        )

    print()
    print("Auto-reply is now ACTIVE.")
    print("Waiting for new messages...")
    print()

    # =========================
    # CONTINUOUS MONITORING
    # =========================

    while True:

        time.sleep(CHECK_INTERVAL)

        messages = get_messages(driver)

        if not messages:
            continue

        latest = messages[-1]

        message_id = latest["id"]

        # Already processed
        if message_id in processed_ids:
            continue

        # Remember message
        processed_ids.add(message_id)

        print()
        print("--------------------------------")
        print("New message detected!")
        print("Message:", latest["text"])
        print("--------------------------------")

        # Ignore own messages
        if latest["own"]:

            print("This is your own message. Ignoring.")

            continue

        # Generate AI reply
        reply = ask_ai(
            latest["text"]
        )

        if not reply:

            print("No valid AI reply generated.")

            continue

        # Send reply
        send_message(
            driver,
            reply
        )


except KeyboardInterrupt:

    print()
    print("Program stopped.")


except Exception as e:

    print()
    print("Program error:", e)


finally:

    if driver:

        print()
        print("Closing browser...")

        driver.quit()