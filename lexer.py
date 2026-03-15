import re
from dataclasses import dataclass
from typing import Iterator

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

TOKEN_SPEC = [

    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t\r]+"),

    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r"'([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\""),

    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),

    ("OP", r"==|!=|<=|>=|[+\-*/%=<>]"),

    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),

    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),

    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),

    ("COMMA", r","),
    ("COLON", r":"),
    ("SEMICOLON", r";"),
    ("DOT", r"\."),

    ("HASH", r"#"),

    ("MISMATCH", r"."),  # always LAST
]

MASTER_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC),
    re.MULTILINE,
)

KEYWORDS = {
    "if","else","while","for","def","return",
    "true","false","None",
    "int","float","class","public","static"
}

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
            kind = value.upper()

        if kind == "MISMATCH":
            raise SyntaxError(
                f"Unexpected character {value!r} at line {line} col {column}"
            )

        yield Token(kind, value, line, column)
