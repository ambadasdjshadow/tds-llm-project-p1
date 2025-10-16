from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET = "s3cr3t-8f3a9b2c4d6e7f01"  # <-- replace with your own secret

@app.route('/predict', methods=['POST'])
def predict():
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {SECRET}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    prompt = data.get("prompt", "")
    return jsonify({"message": f"Hello from Flask! You said: {prompt}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)