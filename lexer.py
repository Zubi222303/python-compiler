import re
from collections import namedtuple

Token = namedtuple('Token', ['value', 'type', 'line', 'column'])

TOKEN_SPEC = [
    ('COMMENT',        r'#.*'),
    ('STRING',         r'"[^"\n]*"'),
    ('NUMBER_FLOAT',   r'\d+\.\d+'),
    ('NUMBER_INT',     r'\d+'),
    ('KEYWORD',        r'\b(Rakho|Ginti|PointWala|Baat|HaaNaa|Agar|WarnaAgar|Warna|JabTak|Kaam|Wapis|Dikhao|Pucho|Bas|Sahi|Ghalat)\b'),
    ('OPERATOR',       r'==|!=|<=|>=|&&|\|\||[+\-*/%<>!]'),
    ('ASSIGN',         r'='),
    ('SEPARATOR',      r'[();{},]'),
    ('IDENTIFIER',     r'\b[a-zA-Z_]\w*\b'),
    ('NEWLINE',        r'\n'),
    ('SKIP',           r'[ \t]+'),
    ('MISMATCH',       r'.'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise Exception(f"Unrecognized token '{value}' at line {line_num}, column {column}")
        else:
            tokens.append(Token(value, kind, line_num, column))
    
    return tokens