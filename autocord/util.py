from typing import Tuple


def expand_time_string(item: str) -> Tuple[int, int, int]:
    """Expand a string from the format `HH`, `HH:MM`, or `HH:MM:SS` into
    numbers.
    """
    values = [int(v) for v in item.split(":")[:3]]

    def clamp(number: int, _min: int, _max: int) -> int:
        if number < _min:
            return _min
        elif number > _max:
            return _max
        else:
            return number

    return (
        clamp(values[0] if len(values) > 0 else 0, 0, 23),
        clamp(values[1] if len(values) > 1 else 0, 0, 59),
        clamp(values[2] if len(values) > 2 else 0, 0, 59),
    )
