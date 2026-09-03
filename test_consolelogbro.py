"""
Comprehensive tests for consolelogbro.py console.log parser
"""

import pytest
from io import StringIO
import sys
# Import the module by executing the code
import consolelogbro


def capture_output(func, *args, **kwargs):
    """Helper to capture print output"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        result = func(*args, **kwargs)
        output = sys.stdout.getvalue()
        return result, output
    finally:
        sys.stdout = old_stdout


class TestNumberParsing:
    """Test number parsing functionality"""
    
    def test_parse_integer(self):
        """Test parsing simple integers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 42')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 42
        consolelogbro.reset_variables()
    
    def test_parse_float(self):
        """Test parsing floating point numbers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 3.14')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 3.14
        consolelogbro.reset_variables()
    
    def test_parse_negative_number(self):
        """Test parsing negative numbers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = -10')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == -10
        consolelogbro.reset_variables()
    
    def test_parse_positive_sign(self):
        """Test parsing numbers with positive sign"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = +5')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 5
        consolelogbro.reset_variables()


class TestStringParsing:
    """Test string parsing functionality"""
    
    def test_parse_simple_string(self):
        """Test parsing simple strings"""
        result, _ = capture_output(consolelogbro.interpret, 'let msg = "hello"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "hello"
        consolelogbro.reset_variables()
    
    def test_parse_string_with_spaces(self):
        """Test parsing strings with spaces"""
        result, _ = capture_output(consolelogbro.interpret, 'let msg = "hello world"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "hello world"
        consolelogbro.reset_variables()
    
    def test_parse_escaped_quotes(self):
        """Test parsing strings with escaped quotes"""
        result, _ = capture_output(consolelogbro.interpret, r'let msg = "say \"hi\""')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == 'say "hi"'
        consolelogbro.reset_variables()
    
    def test_parse_escaped_newline(self):
        """Test parsing strings with escaped newlines"""
        result, _ = capture_output(consolelogbro.interpret, r'let msg = "line1\nline2"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "line1\nline2"
        consolelogbro.reset_variables()
    
    def test_parse_escaped_tab(self):
        """Test parsing strings with escaped tabs"""
        result, _ = capture_output(consolelogbro.interpret, r'let msg = "hello\tworld"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "hello\tworld"
        consolelogbro.reset_variables()


class TestBooleanParsing:
    """Test boolean parsing functionality"""
    
    def test_parse_true(self):
        """Test parsing true boolean"""
        result, _ = capture_output(consolelogbro.interpret, 'let flag = true')
        assert consolelogbro.BroThatsJS_VARIABLES.get('flag') is True
        consolelogbro.reset_variables()
    
    def test_parse_false(self):
        """Test parsing false boolean"""
        result, _ = capture_output(consolelogbro.interpret, 'let flag = false')
        assert consolelogbro.BroThatsJS_VARIABLES.get('flag') is False
        consolelogbro.reset_variables()


class TestArithmetic:
    """Test arithmetic operations"""
    
    def test_addition_numbers(self):
        """Test adding numbers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 5 + 3')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 8
        consolelogbro.reset_variables()
    
    def test_subtraction(self):
        """Test subtracting numbers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 10 - 3')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 7
        consolelogbro.reset_variables()
    
    def test_multiplication(self):
        """Test multiplying numbers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 4 * 5')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 20
        consolelogbro.reset_variables()
    
    def test_division(self):
        """Test dividing numbers"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 20 / 4')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 5.0
        consolelogbro.reset_variables()
    
    def test_modulo(self):
        """Test modulo operation"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 10 % 3')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 1
        consolelogbro.reset_variables()
    
    def test_order_of_operations(self):
        """Test order of operations (multiplication before addition)"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 2 + 3 * 4')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 14
        consolelogbro.reset_variables()


class TestStringConcatenation:
    """Test string concatenation"""
    
    def test_string_concatenation(self):
        """Test concatenating strings"""
        result, _ = capture_output(consolelogbro.interpret, 'let msg = "hello" + "world"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "helloworld"
        consolelogbro.reset_variables()
    
    def test_string_number_concatenation(self):
        """Test concatenating string and number"""
        result, _ = capture_output(consolelogbro.interpret, 'let msg = "value: " + 42')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "value: 42"
        consolelogbro.reset_variables()
    
    def test_number_string_concatenation(self):
        """Test concatenating number and string"""
        result, _ = capture_output(consolelogbro.interpret, 'let msg = 42 + " is the answer"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('msg') == "42 is the answer"
        consolelogbro.reset_variables()


class TestConsoleLog:
    """Test console.log functionality"""
    
    def test_console_log_string(self):
        """Test console.log with string"""
        _, output = capture_output(consolelogbro.interpret, 'console.log("hello")')
        assert output.strip() == "hello"
        consolelogbro.reset_variables()
    
    def test_console_log_number(self):
        """Test console.log with number"""
        _, output = capture_output(consolelogbro.interpret, 'console.log(42)')
        assert output.strip() == "42"
        consolelogbro.reset_variables()
    
    def test_console_log_boolean(self):
        """Test console.log with boolean"""
        _, output = capture_output(consolelogbro.interpret, 'console.log(true)')
        assert output.strip() == "true"
        consolelogbro.reset_variables()
    
    def test_console_log_multiple_args(self):
        """Test console.log with multiple arguments"""
        _, output = capture_output(consolelogbro.interpret, 'console.log("a", "b", "c")')
        assert output.strip() == "a b c"
        consolelogbro.reset_variables()
    
    def test_console_log_empty(self):
        """Test console.log with no arguments"""
        _, output = capture_output(consolelogbro.interpret, 'console.log()')
        assert output.strip() == ""
        consolelogbro.reset_variables()
    
    def test_console_log_variable(self):
        """Test console.log with variable"""
        consolelogbro.interpret('let x = 100')
        _, output = capture_output(consolelogbro.interpret, 'console.log(x)')
        assert output.strip() == "100"
        consolelogbro.reset_variables()


class TestVariableAssignment:
    """Test variable assignment"""
    
    def test_let_declaration(self):
        """Test let variable declaration"""
        consolelogbro.interpret('let x = 50')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 50
        consolelogbro.reset_variables()
    
    def test_variable_reassignment(self):
        """Test reassigning variable"""
        consolelogbro.interpret('let x = 10')
        consolelogbro.interpret('x = 20')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 20
        consolelogbro.reset_variables()
    
    def test_variable_in_expression(self):
        """Test using variable in expression"""
        consolelogbro.interpret('let x = 5')
        consolelogbro.interpret('let y = x + 3')
        assert consolelogbro.BroThatsJS_VARIABLES.get('y') == 8
        consolelogbro.reset_variables()


class TestParentheses:
    """Test parentheses grouping"""
    
    def test_parentheses_override_order(self):
        """Test parentheses override order of operations"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = (2 + 3) * 4')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 20
        consolelogbro.reset_variables()
    
    def test_nested_parentheses(self):
        """Test nested parentheses"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = ((2 + 3) * (4 - 1))')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 15
        consolelogbro.reset_variables()


class TestErrors:
    """Test error handling"""
    
    def test_division_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ZeroDivisionError):
            consolelogbro.interpret('let x = 10 / 0')
        consolelogbro.reset_variables()
    
    def test_modulo_by_zero(self):
        """Test modulo by zero raises error"""
        with pytest.raises(ZeroDivisionError):
            consolelogbro.interpret('let x = 10 % 0')
        consolelogbro.reset_variables()
    
    def test_undefined_variable(self):
        """Test using undefined variable raises error"""
        with pytest.raises(NameError):
            consolelogbro.interpret('console.log(undefined_var)')
        consolelogbro.reset_variables()
    
    def test_invalid_number(self):
        """Test invalid number raises error"""
        with pytest.raises(SyntaxError):
            consolelogbro.interpret('let x = 3.14.15')
        consolelogbro.reset_variables()
    
    def test_unterminated_string(self):
        """Test unterminated string raises error"""
        with pytest.raises(SyntaxError):
            consolelogbro.interpret('let x = "unterminated')
        consolelogbro.reset_variables()
    
    def test_invalid_variable_name(self):
        """Test invalid variable name raises error"""
        with pytest.raises(SyntaxError):
            consolelogbro.interpret('let 123var = 5')
        consolelogbro.reset_variables()
    
    def test_reassign_undefined_variable(self):
        """Test reassigning undefined variable raises error"""
        with pytest.raises(NameError):
            consolelogbro.interpret('undefined_var = 5')
        consolelogbro.reset_variables()


class TestMultipleStatements:
    """Test multiple statements"""
    
    def test_semicolon_separated_statements(self):
        """Test multiple statements separated by semicolons"""
        consolelogbro.interpret('let x = 10; let y = 20')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 10
        assert consolelogbro.BroThatsJS_VARIABLES.get('y') == 20
        consolelogbro.reset_variables()
    
    def test_newline_separated_statements(self):
        """Test multiple statements separated by newlines"""
        consolelogbro.interpret('let x = 10\nlet y = 20')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 10
        assert consolelogbro.BroThatsJS_VARIABLES.get('y') == 20
        consolelogbro.reset_variables()
    
    def test_mixed_statements(self):
        """Test mixed variable assignments and console.log"""
        consolelogbro.interpret('let x = 5; let y = 3; let z = x + y')
        assert consolelogbro.BroThatsJS_VARIABLES.get('z') == 8
        consolelogbro.reset_variables()


class TestShowVariables:
    """Test show_variables function"""
    
    def test_show_variables_empty(self):
        """Test show_variables with no variables"""
        consolelogbro.reset_variables()
        _, output = capture_output(consolelogbro.show_variables)
        assert "No variables" in output
    
    def test_show_variables_with_data(self):
        """Test show_variables with variables"""
        consolelogbro.interpret('let x = 42')
        consolelogbro.interpret('let msg = "hello"')
        _, output = capture_output(consolelogbro.show_variables)
        assert "x = 42" in output
        assert "msg = hello" in output
        consolelogbro.reset_variables()


class TestEdgeCases:
    """Test edge cases"""
    
    def test_float_division_result(self):
        """Test that division returns float"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 5 / 2')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == 2.5
        consolelogbro.reset_variables()
    
    def test_zero_operations(self):
        """Test operations with zero"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = 0; let y = x + 5')
        assert consolelogbro.BroThatsJS_VARIABLES.get('y') == 5
        consolelogbro.reset_variables()
    
    def test_boolean_js_string_true(self):
        """Test boolean true converts to JS string correctly"""
        _, output = capture_output(consolelogbro.interpret, 'console.log(true)')
        assert output.strip() == "true"
        consolelogbro.reset_variables()
    
    def test_boolean_js_string_false(self):
        """Test boolean false converts to JS string correctly"""
        _, output = capture_output(consolelogbro.interpret, 'console.log(false)')
        assert output.strip() == "false"
        consolelogbro.reset_variables()
    
    def test_string_with_quotes_in_expression(self):
        """Test complex expression with quoted strings"""
        result, _ = capture_output(consolelogbro.interpret, 'let x = "a" + "b" + "c"')
        assert consolelogbro.BroThatsJS_VARIABLES.get('x') == "abc"
        consolelogbro.reset_variables()
