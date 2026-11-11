"""Lab 7: Weather Alert Data Processor with Input Validation and Defensive Hardening."""

import math


def parse_reading(text):
    """
    Parses a temperature and humidity reading string in the format 'temp/humidity'.

    Args:
        text (str): Input string, e.g. "35.5/80".

    Returns:
        tuple[float, int] | None: (temperature, humidity) if valid, None otherwise.
    """
    if not isinstance(text, str):
        return None

    text = text.strip()
    if '/' not in text:
        return None

    parts = text.split('/')
    if len(parts) != 2:
        return None

    temp_str, hum_str = parts[0].strip(), parts[1].strip()
    if not temp_str or not hum_str:
        return None

    try:
        temp = float(temp_str)
        if math.isnan(temp) or math.isinf(temp):
            return None
    except (ValueError, TypeError):
        return None

    try:
        hum = int(hum_str)
        if not (0 <= hum <= 100):
            return None
    except (ValueError, TypeError):
        return None

    # Realistic meteorological temperature range (-100C to 100C)
    if not (-100.0 <= temp <= 100.0):
        return None

    return (temp, hum)


def wind_category(speed_text):
    """
    Classifies wind speed into categories: 'warning', 'advisory', or 'none'.

    Args:
        speed_text (str | int): Wind speed in km/h.

    Returns:
        str | None: Category string ('warning', 'advisory', 'none') if valid, None otherwise.
    """
    if speed_text is None:
        return None

    if isinstance(speed_text, (int, float)):
        if isinstance(speed_text, bool):
            return None
        if isinstance(speed_text, float) and not speed_text.is_integer():
            return None
        speed = int(speed_text)
    elif isinstance(speed_text, str):
        cleaned = speed_text.strip()
        if not cleaned:
            return None
        if cleaned.startswith('+'):
            cleaned = cleaned[1:]
        if not cleaned.isdigit():
            return None
        try:
            speed = int(cleaned)
        except (ValueError, TypeError):
            return None
    else:
        return None

    if speed < 0 or speed > 500:
        return None

    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'


def rainfall_spread(readings_csv):
    """
    Computes the spread (max - min) of comma-separated hourly rainfall readings in mm.

    Args:
        readings_csv (str): Comma-separated rainfall numbers, e.g. "2,5.5,10".

    Returns:
        float | None: Spread (max - min) rounded to 4 decimals if valid, None otherwise.
    """
    if not isinstance(readings_csv, str):
        return None

    readings_csv = readings_csv.strip()
    if not readings_csv:
        return None

    parts = readings_csv.split(',')
    readings = []
    for part in parts:
        part_clean = part.strip()
        if not part_clean:
            return None
        try:
            val = float(part_clean)
            if math.isnan(val) or math.isinf(val):
                return None
            if val < 0.0 or val > 2000.0:  # Physical rainfall limits in mm
                return None
            readings.append(val)
        except (ValueError, TypeError):
            return None

    if not readings:
        return None

    spread = max(readings) - min(readings)
    return round(spread, 4)


def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result)


if __name__ == "__main__":
    main()
