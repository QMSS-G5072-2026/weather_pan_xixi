"""Weather station utilities."""

import math

import pandas as pd


ABSOLUTE_ZERO_C = -273.15
MIN_PLAUSIBLE_C = -90.0
MAX_PLAUSIBLE_C = 60.0


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from degrees Celsius to degrees Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.

    Raises:
        TypeError: If celsius is not a number.
        ValueError: If celsius is below absolute zero.
    """
    if isinstance(celsius, bool) or not isinstance(celsius, (int, float)):
        raise TypeError("celsius must be a number")

    if celsius < ABSOLUTE_ZERO_C:
        raise ValueError("temperature cannot be below absolute zero")

    return celsius * 9 / 5 + 32


def summarize_temperatures(temps: list[float]) -> dict[str, float]:
    """Summarize temperature readings, ignoring missing values.

    Args:
        temps: Temperature readings, possibly containing NaN.

    Returns:
        A dictionary with mean, min, max, and n_missing.

    Raises:
        ValueError: If no valid temperature readings exist.
    """
    valid = [t for t in temps if not math.isnan(t)]

    if not valid:
        raise ValueError("no valid temperature readings")

    return {
        "mean": sum(valid) / len(valid),
        "min": min(valid),
        "max": max(valid),
        "n_missing": len(temps) - len(valid),
    }


def clean_readings(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw weather station readings.

    Steps:
        1. Remove rows with missing temperatures.
        2. Remove temperatures outside the plausible range.
        3. Add Fahrenheit temperatures.
        4. Sort by station and date.

    Args:
        df: DataFrame containing station, date, and temp_c columns.

    Returns:
        A cleaned DataFrame.
    """
    cleaned = df.dropna(subset=["temp_c"])
    in_range = cleaned["temp_c"].between(
        MIN_PLAUSIBLE_C,
        MAX_PLAUSIBLE_C,
    )

    cleaned = cleaned[in_range].copy()

    cleaned["temp_f"] = cleaned["temp_c"] * 9 / 5 + 32

    return cleaned.sort_values(
        ["station", "date"]
    ).reset_index(drop=True)