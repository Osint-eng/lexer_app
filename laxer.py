# lexer.py
import re
from dataclasses import dataclass
from typing import Iterator, Optional

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

# Define token specs (order matters for longest-match)
TOKEN_SPEC = [
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t\r]+"),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("STRING", r"'([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\""),
    ("OP", r"==|!=|<=|>=|[+\-*/%=<>]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA", r","),
    ("COLON", r":"),
    ("SEMICOLON", r";"),
    ("MISMATCH", r"."),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("HASH", r"#"),
    ("SEMICOLON", r";"),
]

MASTER_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC),
    re.MULTILINE,
)

KEYWORDS = {"if", "else", "while", "for", "def", "return", "true", "false", "None"}

def lex(text: str) -> Iterator[Token]:
    line = 1
    line_start = 0
    for m in MASTER_REGEX.finditer(text):
        kind = m.lastgroup
        value = m.group(kind)
        column = m.start() - line_start + 1

        if kind == "NEWLINE":
            line += 1
            line_start = m.end()
            continue
        if kind == "SKIP":
            continue
        if kind == "IDENT" and value in KEYWORDS:
            kind = value.upper()  # e.g. 'if' -> 'IF'
        if kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character {value!r} at line {line} col {column}")
        yield Token(kind, value, line, column)
