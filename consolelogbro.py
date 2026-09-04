exec(r'''
class Parser:
    def __init__(self, text, variables):
        self.text = text
        self.pos = 0
        self.variables = variables

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

        if self.pos >= len(self.text):
            return None

        if self.text[self.pos] != '"':
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

                escaped = self.text[self.pos]
                result += escapes.get(escaped, escaped)

            else:
                result += c

            self.pos += 1

        raise SyntaxError("Unterminated string")

    def boolean(self):
        self.skip()

        if self.text.startswith("true", self.pos):
            end = self.pos + 4

            if (
                end == len(self.text)
                or not (
                    self.text[end].isalnum()
                    or self.text[end] == "_"
                )
            ):
                self.pos = end
                return True

        if self.text.startswith("false", self.pos):
            end = self.pos + 5

            if (
                end == len(self.text)
                or not (
                    self.text[end].isalnum()
                    or self.text[end] == "_"
                )
            ):
                self.pos = end
                return False

        return None

    def identifier(self):
        self.skip()

        if self.pos >= len(self.text):
            return None

        first = self.text[self.pos]

        if not (first.isalpha() or first == "_"):
            return None

        start = self.pos
        self.pos += 1

        while self.pos < len(self.text):
            c = self.text[self.pos]

            if c.isalnum() or c == "_":
                self.pos += 1
            else:
                break

        name = self.text[start:self.pos]

        if name not in self.variables:
            raise NameError(name + " is not defined")

        return self.variables[name]

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

        value = self.identifier()
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


def eval_expr(expr, variables):
    return Parser(expr, variables).parse()


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

                if depth == 0:
                    raise SyntaxError("Unexpected ')'")

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


def valid_identifier(name):
    if not name:
        return False

    if not (name[0].isalpha() or name[0] == "_"):
        return False

    for c in name[1:]:
        if not (c.isalnum() or c == "_"):
            return False

    return True


def interpret_console_log(code, variables):
    prefix = "console.log("

    if not code.startswith(prefix):
        raise SyntaxError("Invalid console.log statement")

    if not code.endswith(")"):
        raise SyntaxError("Invalid console.log statement")

    inside = code[len(prefix):-1]

    arguments = split_arguments(inside)

    if not arguments:
        print()
        return

    values = [
        eval_expr(argument, variables)
        for argument in arguments
    ]

    output = " ".join(
        Parser("", variables).js_string(value)
        for value in values
    )

    print(output)


def interpret_statement(code, variables):
    code = code.strip()

    if not code:
        return

    if code.startswith("console.log("):
        interpret_console_log(code, variables)
        return

    if code.startswith("let "):

        declaration = code[4:].strip()

        if "=" not in declaration:
            raise SyntaxError(
                "Expected '=' in variable declaration"
            )

        name, expression = declaration.split("=", 1)

        name = name.strip()
        expression = expression.strip()

        if not valid_identifier(name):
            raise SyntaxError("Invalid variable name")

        if name in ("true", "false"):
            raise SyntaxError("Invalid variable name")

        if not expression:
            raise SyntaxError("Expected value")

        value = eval_expr(expression, variables)

        variables[name] = value
        return

    if "=" in code:

        name, expression = code.split("=", 1)

        name = name.strip()
        expression = expression.strip()

        if not valid_identifier(name):
            raise SyntaxError("Invalid variable name")

        if name not in variables:
            raise NameError(name + " is not defined")

        if not expression:
            raise SyntaxError("Expected value")

        value = eval_expr(expression, variables)

        variables[name] = value
        return

    raise SyntaxError("Unknown statement: " + code)


def split_statements(code):
    statements = []

    start = 0
    depth = 0
    in_string = False
    escaped = False

    for i, c in enumerate(code):

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

                if depth == 0:
                    raise SyntaxError("Unexpected ')'")

                depth -= 1

            elif (c == ";" or c == "\n") and depth == 0:

                part = code[start:i].strip()

                if part:
                    statements.append(part)

                start = i + 1

    if in_string:
        raise SyntaxError("Unterminated string")

    if depth != 0:
        raise SyntaxError("Unbalanced parentheses")

    final = code[start:].strip()

    if final:
        statements.append(final)

    return statements


# Persistent JavaScript environment
BroThatsJS_VARIABLES = {}


def interpret(code):
    statements = split_statements(code)

    for statement in statements:
        interpret_statement(
            statement,
            BroThatsJS_VARIABLES
        )

    return BroThatsJS_VARIABLES


def reset_variables():
    BroThatsJS_VARIABLES.clear()
    print("Variables cleared.")


def show_variables():
    if not BroThatsJS_VARIABLES:
        print("No variables.")
        return

    for name, value in BroThatsJS_VARIABLES.items():
        print(
            name + " = "
            + Parser("", BroThatsJS_VARIABLES).js_string(value)
        )


print("BroThatsjs.js JS interpreter loaded.")
print("Use: interpret('let x = 10')")
print("Then: interpret('console.log(x)')")
print("Use show_variables() to see variables.")
print("Use reset_variables() to clear them.")
print("yea theres more commands,trust me")
''')
