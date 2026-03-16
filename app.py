from flask import Flask, request, jsonify, render_template
from lexer import lex
from buffer import InputBuffer   # import buffer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json["code"]

    # Run buffer
    buffer = InputBuffer(code)
    buffer_stream = []

    while True:
        ch = buffer.next_char()
        if ch is None:
            break
        buffer_stream.append(ch)

    # Run lexer
    tokens = []
    for tok in lex(code):
        tokens.append({
            "type": tok.type,
            "value": tok.value,
            "line": tok.line,
            "column": tok.column
        })

    # return both buffer + tokens
    return jsonify({
        "buffer": buffer_stream,
        "tokens": tokens
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
