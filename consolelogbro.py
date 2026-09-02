#bro that is js console log 
exec(r'''
class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def skip(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def match(self, char):
        self.skip()
        if self.pos < len(self.text) and self.text[self.pos] == char:
            self.pos += 1
            return True
        return False

    def number(self):
        self.skip()
        start = self.pos

        while self.pos < len(self.text) and (
            self.text[self.pos].isdigit() or self.text[self.pos] == "."
        ):
            self.pos += 1

        if start == self.pos:
            return None

        value = self.text[start:self.pos]
        return float(value) if "." in value else int(value)

    def string(self):
        self.skip()

        if self.pos >= len(self.text) or self.text[self.pos] != '"':
            return None

        self.pos += 1
        result = ""

        while self.pos < len(self.text):
            c = self.text[self.pos]

            if c == '"':
                self.pos += 1
                return result

            if c == "\\" and self.pos + 1 < len(self.text):
                self.pos += 1
                result += self.text[self.pos]
            else:
                result += c

            self.pos += 1

        raise SyntaxError("Unterminated string")

    def primary(self):
        self.skip()

        if self.match("("):
            value = self.expression()
            if not self.match(")"):
                raise SyntaxError("Expected ')'")
            return value

        value = self.string()
        if value is not None:
            return value

        value = self.number()
        if value is not None:
            return value

        raise SyntaxError("Expected number, string, or '('")

    def unary(self):
        self.skip()

        if self.match("-"):
            return -self.unary()

        if self.match("+"):
            return self.unary()

        return self.primary()

    def multiplication(self):
        left = self.unary()

        while True:
            if self.match("*"):
                left = left * self.unary()
            elif self.match("/"):
                right = self.unary()
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left = left / right
            elif self.match("%"):
                left = left % self.unary()
            else:
                break

        return left

    def expression(self):
        left = self.multiplication()

        while True:
            if self.match("+"):
                right = self.multiplication()

                # JavaScript-like string concatenation
                if isinstance(left, str) or isinstance(right, str):
                    left = str(left) + str(right)
                else:
                    left = left + right

            elif self.match("-"):
                left = left - self.multiplication()
            else:
                break

        return left

    def parse(self):
        value = self.expression()
        self.skip()

        if self.pos != len(self.text):
            raise SyntaxError(
                "Unexpected character: " + self.text[self.pos]
            )

        return value


def eval_expr(expr):
    return Parser(expr).parse()


def interpret(code):
    code = code.strip()

    if code.startswith("console.log(") and code.endswith(")"):
        expr = code[len("console.log("):-1]
        print(eval_expr(expr))
    else:
        raise SyntaxError("Unknown statement: " + code)
''')
#test.now
interpret('console.log(2 + 3)')
interpret('console.log(2 + 3 * 4)')
interpret('console.log("Hello " + "world")')
