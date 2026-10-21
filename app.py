from flask import Flask, request
from openai import OpenAI
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "irakli123"

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

CHAT_ID = "7937718581"

user_history = {}

def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

def send_message(recipient_id, text):

    url = "https://graph.facebook.com/v23.0/me/messages"

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

def ask_ai(user_id, message):

    if user_id not in user_history:

        user_history[user_id] = [
            {
                "role": "system",
                "content": """
შენ ხარ პროფესიონალი ონლაინ მაღაზიის კონსულტანტი.

ყოველთვის უპასუხე ქართულად.

პროდუქტი:

სარბენი ბილიკი

ფასი:

280 ლარი - სტანდარტული მოდელი. 3 შრიანი მატრასით. საჭიროებს 20 წუთში ერთხელ შესვენებას

380 ლარი - ულიმიტო, უნახშირო ძრავით. 3 შრიანი კერამო მატასით. არ საჭიროებს შესვენებას და აქვს ალუმინის მსუბუქი კარკასი

მიწოდება:

280 ლარიანი მოდელის 30 ლარი
380 ლარიანი მოდელის 20 ლარი

თუ კლიენტი ყიდვას აპირებს, ეტაპობრივად აიღე:

1. სახელი და გვარი
2. ტელეფონი
3. მისამართი

არ მოსთხოვო ყველაფერი ერთად.

ესაუბრე მოკლედ და ბუნებრივად.

თუ შეკვეთა დასრულდა, პასუხის ბოლოს მიუწერე:

ORDER_COMPLETE
"""
            }
        ]

    user_history[user_id].append(
        {
            "role": "user",
            "content": message
        }
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=user_history[user_id]
    )

    answer = response.choices[0].message.content

    user_history[user_id].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer

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

                reply = ask_ai(sender_id, text)

                send_message(
                    sender_id,
                    reply.replace("ORDER_COMPLETE", "")
                )

                if "ORDER_COMPLETE" in reply:

                    send_telegram(
                        f"🛒 ახალი შეკვეთა\n\n{reply}"
                    )

    except Exception as e:
        print(e)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
