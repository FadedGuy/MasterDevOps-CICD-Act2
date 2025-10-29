import app
from math import sqrt, log10


class InvalidPermissions(Exception):
    pass


class Calculator:
    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def substract(self, x, y):
        self.check_types(x, y)
        return x - y

    def multiply(self, x, y, user):
        if not app.util.validate_permissions(f"{x} * {y}", user):
            raise InvalidPermissions('User has no permissions')

        self.check_types(x, y)
        return x * y

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("Division by zero is not possible")

        return x / y

    def power(self, x, y):
        self.check_types(x, y)
        return x ** y

    def sqrt(self, x): 
        self.check_types(x)
        if x < 0:
            raise TypeError("Cannot calculate square root of a negative number")
        
        return sqrt(x)
    
    def log10(self, x):
        self.check_types(x)
        if x <= 0:
            raise TypeError("Log10 undefined for zero or negative numbers")

        return log10(x)

    def check_types(self, *args):
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise TypeError("Parameters must be numbers")


if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)
