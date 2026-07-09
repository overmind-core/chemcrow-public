import json
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/v1/run', methods=['POST'])
def rxnfp():
    data = request.get_json()
    target = data.get("smiles") or data.get("target")
    if not target:
        return jsonify({"error": "Missing smiles field"}), 400

    command = ["aizynthcli", "--config", "config.yml", "--smiles", f"{target}"]

    print(command)
    result = subprocess.run(
        command, check=True, capture_output=True, text=True
    )
    print(result)

    # Read output trees.json
    with open("trees.json", "r") as f:
        tree = json.load(f)

    if isinstance(tree, list):
        return jsonify(tree)
    return jsonify([tree])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
