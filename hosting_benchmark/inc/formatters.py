"""Text/number formatters."""


def format_timing(value: float) -> str:
    """Format a timing value, returning a human-friendly float representation.

    :param value: Timing value.
    """
    return f"{value:.4f} s"
