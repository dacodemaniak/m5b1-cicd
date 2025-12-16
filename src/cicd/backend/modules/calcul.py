from pydantic import validate_call

@validate_call
def square(number: int) -> int:
    return number * number