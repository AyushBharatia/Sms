import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Set your Discord Webhook URL
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1344509190701449246/OZ70ob9rVVhR-BKnZDlhcHBnu8YL863E_8z-JYRqEzqC_lpxXWR_lUXyy51cKDU3GKqq")

@app.route("/", methods=["POST"])
def receive_sms():
    """Receives SMS from DaisySMS and forwards the 'code' to Discord."""
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({"error": "Invalid JSON input"}), 400

    # Extract the 'code' from the DaisySMS payload
    sms_code = data.get("code")

    if not sms_code:
        return jsonify({"error": "Missing 'code' field"}), 400

    # Format the message for Discord
    discord_message = f"📩 Incoming SMS Code: `{sms_code}`"

    # Send message to Discord
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to forward SMS code to Discord"}), 500

    return jsonify({"status": "SMS code forwarded to Discord"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
