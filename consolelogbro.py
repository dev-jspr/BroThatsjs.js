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
        dots = 0

        while self.pos < len(self.text):
            c = self.text[self.pos]

            if c.isdigit():
                self.pos += 1
            elif c == ".":
                dots += 1
                if dots > 1:
                    break
                self.pos += 1
            else:
                break

        if start == self.pos:
            return None

        value = self.text[start:self.pos]

        if value == ".":
            raise SyntaxError("Invalid number")

        return float(value) if "." in value else int(value)

    def string(self):
        self.skip()

        if self.pos >= len(self.text) or self.text[self.pos] != '"':
            return None

        self.pos += 1
        result = ""

        escapes = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            '"': '"',
            "\\": "\\"
        }

        while self.pos < len(self.text):
            c = self.text[self.pos]

            if c == '"':
                self.pos += 1
                return result

            if c == "\\":
                self.pos += 1

                if self.pos >= len(self.text):
                    raise SyntaxError("Unterminated string")

                c = self.text[self.pos]
                result += escapes.get(c, c)
            else:
                result += c

            self.pos += 1

        raise SyntaxError("Unterminated string")

    def boolean(self):
        self.skip()

        if self.text.startswith("true", self.pos):
            end = self.pos + 4
            if end == len(self.text) or not (
                self.text[end].isalnum() or self.text[end] == "_"
            ):
                self.pos = end
                return True

        if self.text.startswith("false", self.pos):
            end = self.pos + 5
            if end == len(self.text) or not (
                self.text[end].isalnum() or self.text[end] == "_"
            ):
                self.pos = end
                return False

        return None

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

        value = self.boolean()
        if value is not None:
            return value

        value = self.number()
        if value is not None:
            return value

        raise SyntaxError("Expected value")

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
                right = self.unary()

                if right == 0:
                    raise ZeroDivisionError("Division by zero")

                left = left % right

            else:
                break

        return left

    def expression(self):
        left = self.multiplication()

        while True:
            if self.match("+"):
                right = self.multiplication()

                if isinstance(left, str) or isinstance(right, str):
                    left = self.js_string(left) + self.js_string(right)
                else:
                    left = left + right

            elif self.match("-"):
                left = left - self.multiplication()

            else:
                break

        return left

    def js_string(self, value):
        if value is True:
            return "true"

        if value is False:
            return "false"

        return str(value)

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


def split_arguments(text):
    arguments = []
    start = 0
    depth = 0
    in_string = False
    escaped = False

    for i, c in enumerate(text):

        if in_string:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                in_string = False

        else:
            if c == '"':
                in_string = True

            elif c == "(":
                depth += 1

            elif c == ")":
                depth -= 1

            elif c == "," and depth == 0:
                part = text[start:i].strip()

                if not part:
                    raise SyntaxError("Missing argument")

                arguments.append(part)
                start = i + 1

    if in_string:
        raise SyntaxError("Unterminated string")

    if depth != 0:
        raise SyntaxError("Unbalanced parentheses")

    final = text[start:].strip()

    if final:
        arguments.append(final)
    elif arguments:
        raise SyntaxError("Missing argument")

    return arguments


def interpret(code):
    code = code.strip()

    if not code.startswith("console.log(") or not code.endswith(")"):
        raise SyntaxError("Unknown statement: " + code)

    inside = code[len("console.log("):-1]
    arguments = split_arguments(inside)

    values = [eval_expr(arg) for arg in arguments]

    output = " ".join(
        Parser("").js_string(value)
        for value in values
    )

    print(output)
''')
