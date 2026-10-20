from flask import Flask, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

VERIFY_TOKEN = "irakli123"

PAGE_ACCESS_TOKEN = "EAAWvGRv9Q9cBSwg5mBLpBgZBmortM1ZAHQYKvkzljb462xMgXQDIhCaYc4ciTz9uY9kulv3MaQeUenGFQpNd2LTQTdeO2ah5yxLmBcoJS2ULlsw0uIUZBVhNDWmJKqthhJ2IYogY3HJaZCPNvznOO9HVu2cImVzVsk5GziMW7mBpEX2cc08bahB3quVDUaiBiU6oIPqAAGuCpBc1GJCiXwZDZD"

TELEGRAM_BOT_TOKEN = "8800332184:AAGBfBfxje1lhiIWsQp5dhlof6XfPteCg2g"
TELEGRAM_CHAT_ID = "7937718581"

user_state = {}

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }
    )

def send_message(recipient_id, text):

    url = f"https://graph.facebook.com/v23.0/me/messages"

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text
        }
    }

    requests.post(url, params=params, json=payload)

@app.route("/")
def home():
    return "FB BOT ONLINE ✅"

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

        for entry in data.get("entry", []):

            for messaging in entry.get("messaging", []):

                sender_id = messaging["sender"]["id"]

                if "message" not in messaging:
                    continue

                text = messaging["message"].get("text", "")
                msg = text.lower()

                if sender_id not in user_state:
                    user_state[sender_id] = {}

                user = user_state[sender_id]

                treadmill_words = [
                    "სარბენი",
                    "ბილიკი",
                    "sarbeni",
                    "biliki",
                    "treadmill",
                    "беговая",
                    "дорожка",
                    "ფასი",
                    "fasi"
                ]

                if any(word in msg for word in treadmill_words):

                    user["step"] = "model"

                    send_message(
                        sender_id,
                        "✅ გვაქვს 2 მოდელი\n\n"
                        "1️⃣ სტანდარტული - 280 ლარი\n\n"
                        "2️⃣ პრემიუმ - 380 ლარი\n"
                        "(ძლიერი ძრავით)\n\n"
                        "🚚 მიწოდება - 30 ლარი\n\n"
                        "მომწერეთ:\n280 ან 380"
                    )

                elif user.get("step") == "model":

                    if "280" in msg:
                        user["product"] = "სარბენი ბილიკი 280"
                    elif "380" in msg:
                        user["product"] = "სარბენი ბილიკი 380"
                    else:
                        send_message(
                            sender_id,
                            "გთხოვთ მიუთითოთ 280 ან 380"
                        )
                        continue

                    user["step"] = "name"

                    send_message(
                        sender_id,
                        "მიუთითეთ სახელი და გვარი"
                    )

                elif user.get("step") == "name":

                    user["name"] = text
                    user["step"] = "phone"

                    send_message(
                        sender_id,
                        "მიუთითეთ ტელეფონის ნომერი"
                    )

                elif user.get("step") == "phone":

                    user["phone"] = text
                    user["step"] = "address"

                    send_message(
                        sender_id,
                        "მიუთითეთ მისამართი"
                    )

                elif user.get("step") == "address":

                    user["address"] = text

                    order = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "product": user["product"],
                        "name": user["name"],
                        "phone": user["phone"],
                        "address": user["address"]
                    }

                    with open(
                        "orders.txt",
                        "a",
                        encoding="utf-8"
                    ) as f:

                        f.write(
                            json.dumps(
                                order,
                                ensure_ascii=False
                            ) + "\n"
                        )

                    telegram_text = f"""
🛒 ახალი შეკვეთა

პროდუქტი:
{user['product']}

სახელი:
{user['name']}

ტელეფონი:
{user['phone']}

მისამართი:
{user['address']}
"""

                    send_telegram(telegram_text)

                    send_message(
                        sender_id,
                        "✅ შეკვეთა მიღებულია.\n\n"
                        "ჩვენი ოპერატორი მალე დაგიკავშირდებათ."
                    )

                    user_state.pop(sender_id, None)

                elif "განსხვავ" in msg:

                    send_message(
                        sender_id,
                        "280 ლარიანი მოდელი განკუთვნილია "
                        "ჩვეულებრივი გამოყენებისთვის.\n\n"
                        "380 ლარიანს აქვს უფრო ძლიერი "
                        "და გამძლე ძრავი."
                    )

                else:

                    send_message(
                        sender_id,
                        "გამარჯობა 👋\n\n"
                        "სარბენი ბილიკის ფასებისთვის "
                        "მომწერეთ:\n"
                        "სარბენი ბილიკი"
                    )

    except Exception as e:
        print(e)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
