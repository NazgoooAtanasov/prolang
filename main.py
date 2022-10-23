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
            if word != "":
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
    PLUS = 0x0003


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
            elif operation == "+":
                op_token: Token = Token(OP_CODE.PLUS)
                op_tokens.append(op_token)
            else:
                assert False, f"'{operation}' is not implemented in Lexer"

        return (op_tokens, val_tokens)


class Interpreter:
    op_tokens: list[Token]
    val_stack: list[Token]

    def __init__(self, tokens: list[Token], val_stack: list[Token]):
        self.op_tokens = tokens
        self.val_stack = val_stack

    def normalize_numbrer(self, num):
        if isinstance(num, str):
            if "f" in num:
                return float(num.replace("f", ""))
            return int(num)

        return num

    def evaluate(self) -> None:
        while len(self.op_tokens) > 0:
            op_token: Token = self.op_tokens.pop(0)

            if op_token.op_code == OP_CODE.PRINT:
                value_token: Token = self.val_stack.pop(0)
                print(f"{value_token.value}")
            elif op_token.op_code == OP_CODE.PLUS:
                value_token_1: Token = self.val_stack.pop(0)
                value_token_2: Token = self.val_stack.pop(0)

                value1 = self.normalize_numbrer(value_token_1.value)
                value2 = self.normalize_numbrer(value_token_2.value)

                new_val_token: Token = None

                new_val_token = Token(OP_CODE.NOP, value1 + value2)

                self.val_stack.insert(0, new_val_token)
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
