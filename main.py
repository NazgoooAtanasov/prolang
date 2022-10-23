#!/usr/bin/python3

from enum import Enum
import re

def custom_split(str_buf: str) -> list[str]:
    str_split: list[str] = []
    stop_space_parse: bool = False

    word = ""
    for char in str_buf:
        if char == "\"":
            if stop_space_parse:
                stop_space_parse = False
            else:
                stop_space_parse = True
            continue

        if (char == " " or char == "\n") and not stop_space_parse:
            str_split.append(word)
            word = ""
        else: 
            word = f"{word}{char}"

    # required since the char iteration finishes before we are able to put the last word in.
    if word != "":
        str_split.append(word)

    return str_split

class OP_CODE(Enum):
    NOP = 0x0000
    PRINT = 0x0001
    PUSH = 0x0002


class Token:
    op_code: OP_CODE
    value = None

    def __init__(self, op_code: OP_CODE, value=None):
        self.op_code = op_code
        self.value = value


class Lexer:
    file_contents: str

    def __init__(self, file_contents: str):
        self.file_contents = file_contents

    def parse(self) -> list[Token]:
        op_tokens: list[Token] = []
        val_tokens: list[Token] = []

        unparsed_tokens: list[str] = custom_split(self.file_contents)

        while len(unparsed_tokens) > 0:
            operation: str = unparsed_tokens.pop(0)

            if operation == "print":
                op_token: Token = Token(OP_CODE.PRINT)
                op_tokens.append(op_token)
            elif operation == "push":
                print_arg: str = unparsed_tokens.pop(0)
                value_token: Token = Token(
                    OP_CODE.NOP,
                    print_arg
                )
                val_tokens.append(value_token)
            else:
                assert False, f"'{operation}' is not implemented in Lexer"

        return (op_tokens, val_tokens)


class Interpreter:
    op_tokens: list[Token]
    val_stack: list[Token]

    def __init__(self, tokens: list[Token], val_stack: list[Token]):
        self.op_tokens = tokens
        self.val_stack = val_stack

    def evaluate(self) -> None:
        while len(self.op_tokens) > 0:
            op_token: Token = self.op_tokens.pop()

            if op_token.op_code == OP_CODE.PRINT:
                value_token: Token = self.val_stack.pop(0)
                print(f"{value_token.value}")
            else:
                assert False, f"{op_token.op_code} is not implemented in Interpreter"


def start() -> None:
    fd = open("./hello_world.prol", "r")
    file: str = fd.read()
    fd.close()

    lexer: Lexer = Lexer(file.strip())
    (op_tokens, val_tokens) = lexer.parse()

    interpreter: Interpreter = Interpreter(op_tokens, val_tokens)
    interpreter.evaluate()


start()
