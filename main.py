#!/usr/bin/python3

from enum import Enum
import re

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

        unparsed_tokens: list(str) = re.split(" |\n", self.file_contents)

        idx: int = 0
        while idx < len(unparsed_tokens):
            operation: str = unparsed_tokens[idx]

            if operation == "print":
                op_token: Token = Token(OP_CODE.PRINT)
                op_tokens.append(op_token)
            elif operation == "push":
                idx += 1
                print_arg: str = unparsed_tokens[idx]
                value_token: Token = Token(
                    OP_CODE.NOP,
                    print_arg.replace("\"", "")
                )
                val_tokens.append(value_token)
            else:
                assert False, f"'{operation}' is not implemented in Lexer"

            idx += 1

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
                value_token: Token = self.val_stack.pop()
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
