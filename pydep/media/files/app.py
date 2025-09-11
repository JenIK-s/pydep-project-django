from flask import Flask, request, jsonify

app = Flask(__name__)


def analyze_password(password: str) -> dict:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    issues = []
    score = 0

    if len(password) < 6:
        issues.append("too short")
    else:
        score += 1

    if any(c.islower() for c in password):
        score += 1
    else:
        issues.append("no lowercase")

    if any(c.isupper() for c in password):
        score += 1
    else:
        issues.append("no uppercase")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        issues.append("no digits")

    if any(c in "!@#$%^&*()_+-=" for c in password):
        score += 1
    else:
        issues.append("no special characters")

    if score <= 2:
        strength = "weak"
    elif score == 3 or score == 4:
        strength = "medium"
    else:
        strength = "strong"

    return {
        "length": len(password),
        "issues": issues,
        "strength": strength,
        "score": score
    }


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    password = data.get("password")
    try:
        result = analyze_password(password)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
