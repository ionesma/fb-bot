from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "irakli123"
PAGE_ACCESS_TOKEN = "EAAWvGRv9Q9cBSwg5mBLpBgZBmortM1ZAHQYKvkzljb462xMgXQDIhCaYc4ciTz9uY9kulv3MaQeUenGFQpNd2LTQTdeO2ah5yxLmBcoJS2ULlsw0uIUZBVhNDWmJKqthhJ2IYogY3HJaZCPNvznOO9HVu2cImVzVsk5GziMW7mBpEX2cc08bahB3quVDUaiBiU6oIPqAAGuCpBc1GJCiXwZDZD"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "error", 403


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:
        for entry in data["entry"]:
            for messaging in entry["messaging"]:

                sender_id = messaging["sender"]["id"]

                if "message" in messaging:

                    text = messaging["message"].get("text", "").lower()

                    if "სარბენი" in text or "biliki" in text or "sarbeni" in text:
                        reply = """
✅ გვაქვს 2 მოდელი

1. სტანდარტული - 280 ლარი

2. პრემიუმ - 380 ლარი
(ძლიერი ძრავით)

🚚 მიწოდება - 30 ლარი
"""
                    else:
                        reply = "გამარჯობა 👋 რით შემიძლია დაგეხმაროთ?"

                    send_message(sender_id, reply)

    except Exception as e:
        print(e)

    return "ok", 200


def send_message(recipient_id, text):

    url = f"https://graph.facebook.com/v23.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    requests.post(url, json=payload)


@app.route("/")
def home():
    return "FB Messenger Bot Online"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
