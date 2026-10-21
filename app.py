from flask import Flask, request
from openai import OpenAI
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "irakli123"

PAGE_ACCESS_TOKEN = os.getenv("EAAWvGRv9Q9cBSwg5mBLpBgZBmortM1ZAHQYKvkzljb462xMgXQDIhCaYc4ciTz9uY9kulv3MaQeUenGFQpNd2LTQTdeO2ah5yxLmBcoJS2ULlsw0uIUZBVhNDWmJKqthhJ2IYogY3HJaZCPNvznOO9HVu2cImVzVsk5GziMW7mBpEX2cc08bahB3quVDUaiBiU6oIPqAAGuCpBc1GJCiXwZDZD
")
TELEGRAM_BOT_TOKEN = os.getenv("8800332184:AAGBfBfxje1lhiIWsQp5dhlof6XfPteCg2g")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

CHAT_ID = "7937718581"

def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

def send_message(recipient_id, text):

    url = f"https://graph.facebook.com/v23.0/me/messages"

    requests.post(
        url,
        params={
            "access_token": PAGE_ACCESS_TOKEN
        },
        json={
            "recipient": {"id": recipient_id},
            "message": {"text": text[:2000]}
        }
    )

def ask_ai(message):

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": """
შენ ხარ პროფესიონალი გამყიდველი.

ყოველთვის უპასუხე ქართულად.

პროდუქტი:
სარბენი ბილიკი

ფასები:
280 ლარი
380 ლარი (უფრო ძლიერი ძრავით)

მიწოდება:
30 ლარი

თუ კლიენტი ყიდვას აპირებს,
აუღე:

სახელი
ტელეფონი
მისამართი

როცა შეკვეთა დასრულდება,
ბოლოში დაწერე:

ORDER_COMPLETE
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content

@app.route("/")
def home():
    return "AI BOT ONLINE"

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

                if "message" not in messaging:
                    continue

                sender_id = messaging["sender"]["id"]

                text = messaging["message"].get("text", "")

                reply = ask_ai(text)

                send_message(
                    sender_id,
                    reply.replace("ORDER_COMPLETE", "")
                )

                if "ORDER_COMPLETE" in reply:

                    send_telegram(
                        f"🛒 ახალი შეკვეთა\n\n{text}"
                    )

    except Exception as e:
        print(e)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
