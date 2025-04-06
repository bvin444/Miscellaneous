# Code to understand the use of decorators


def my_decorator(func):
    def wrapper():
        print("Hello")
        func()
        print("Benjamin")
    return wrapper

@my_decorator
def test_Input_Function():
    print("Mr.")

test_Input_Function()