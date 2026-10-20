from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "irakli123"

@app.route("/")
def home():
    return "FB Bot Works!"

@app.route("/webhook")
def webhook_verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge

    return "Verification failed", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
