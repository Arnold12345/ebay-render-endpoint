from flask import Flask, request, Response
import hashlib
import json
import os

app = Flask(__name__)

VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN", "mein_token_1234567890_1234567890")
ENDPOINT = os.getenv("ENDPOINT", "https://ebay-render-endpoint.onrender.com/ebay-notify")

@app.route("/")
def home():
    return "OK", 200

@app.route("/ebay-notify", methods=["GET", "POST"])
def ebay_notify():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code", "")
        message = challenge_code + VERIFICATION_TOKEN + ENDPOINT
        challenge_response = hashlib.sha256(message.encode("utf-8")).hexdigest()
        body = json.dumps({"challengeResponse": challenge_response}, separators=(",", ":"))
        return Response(body, status=200, mimetype="application/json")

    print(request.get_data(as_text=True))
    return "", 200
