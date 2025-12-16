import pytest
from pydantic import ValidationError
from cicd.backend.modules.calcul import square

# Valid test case
@pytest.mark.parametrize("input_val, expected_output", [
    (4, 16),
    (0, 0),
    (-5, 25),
    (100, 10000)
])
def test_square_valid_inputs(input_val: int, expected_output: int):
    assert square(input_val) == expected_output

# Invalid test case
@pytest.mark.parametrize("invalid_input", [
    "cinq",
    3.14,
    [1, 2],
    None
])
def test_square_invalid(invalid_input):
    with pytest.raises(ValidationError) as excinfo:
        square(invalid_input)
    
    error_message = str(excinfo.value)
    assert "Input should be a valid integer" in error_message or "is not a valid integer" in error_message