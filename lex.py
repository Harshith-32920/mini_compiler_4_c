import re

# Token specifications
TOKENS = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('ASSIGN',   r'<-'),
    ('REL_OP',   r'==|!=|>=|<=|>|<'),
    ('OPERATOR', r'[+\-*/@#$^%]'),
    ('QUESTION', r'\?'),
    ('COLON',    r':'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS)


def lexical_analyzer(code):
    tokens = []
    position = 0

    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind in ['NUMBER', 'IDENTIFIER', 'OPERATOR', 'ASSIGN',
                    'REL_OP', 'QUESTION', 'COLON', 'LPAREN', 'RPAREN']:
            tokens.append((kind, value, position))
        elif kind == 'SKIP' or kind == 'NEWLINE':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')

        position += 1

    return tokens


def print_table(tokens):
    print("\nLEXICAL ANALYSIS TABLE\n")
    print(f"{'Index':<10}{'Token Type':<15}{'Lexeme':<15}")
    print("-" * 40)

    for idx, (tok_type, lexeme, pos) in enumerate(tokens):
        print(f"{idx:<10}{tok_type:<15}{lexeme:<15}")


if __name__ == "__main__":
    print("Enter your XLang code (end with ENTER):")
    code = input()

    tokens = lexical_analyzer(code)

    print_table(tokens)