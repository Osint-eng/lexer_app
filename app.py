from flask import Flask, request, jsonify, render_template
from lexer import lex   # your lexer file

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json["code"]

    tokens = []
    for tok in lex(code):
        tokens.append({
            "type": tok.type,
            "value": tok.value,
            "line": tok.line,
            "column": tok.column
        })

    return jsonify(tokens)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
