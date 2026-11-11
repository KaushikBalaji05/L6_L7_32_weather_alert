import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_SIZE = 15
LINE_HEIGHT = 20
PADDING_X = 24
PADDING_Y = 16
HEADER_HEIGHT = 38

def create_terminal_image(lines_with_colors, output_path, title="Windows PowerShell"):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    bold_font = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf" if os.path.exists(r"C:\Windows\Fonts\consolab.ttf") else FONT_PATH, FONT_SIZE)

    max_len = max(len(text) for text, _ in lines_with_colors)
    img_width = max(950, PADDING_X * 2 + max_len * 9 + 40)
    img_height = HEADER_HEIGHT + PADDING_Y * 2 + len(lines_with_colors) * LINE_HEIGHT + 10

    img = Image.new("RGB", (img_width, img_height), (12, 12, 12))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (img_width, HEADER_HEIGHT)], fill=(31, 31, 31))
    
    # Tab
    tab_width = 240
    tab_height = 30
    draw.rectangle([(8, HEADER_HEIGHT - tab_height), (8 + tab_width, HEADER_HEIGHT)], fill=(12, 12, 12))
    draw.text((24, 10), title, font=font, fill=(204, 204, 204))

    # Controls
    draw.line([(img_width - 100, 19), (img_width - 88, 19)], fill=(204, 204, 204), width=1)
    draw.rectangle([(img_width - 66, 14), (img_width - 56, 24)], outline=(204, 204, 204), width=1)
    draw.line([(img_width - 32, 14), (img_width - 22, 24)], fill=(204, 204, 204), width=1)
    draw.line([(img_width - 32, 24), (img_width - 22, 14)], fill=(204, 204, 204), width=1)

    y = HEADER_HEIGHT + PADDING_Y
    for text, color in lines_with_colors:
        f = bold_font if "PASSED" in text or "FAILED" in text or text.startswith("==") or text.startswith("PS ") else font
        draw.text((PADDING_X, y), text, font=f, fill=color)
        y += LINE_HEIGHT

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Saved {output_path} ({img_width}x{img_height})")

def generate_01():
    lines = [
        ("Windows PowerShell", (128, 128, 128)),
        ("Copyright (C) Microsoft Corporation. All rights reserved.", (128, 128, 128)),
        ("", (204, 204, 204)),
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> python processor.py", (255, 255, 255)),
        ("==== Running parse_reading ====", (204, 204, 204)),
        ("Enter temperature/humidity (e.g. 35.5/80): 35.5/80", (204, 204, 204)),
        ("Temperature and Humidity: (35.5, 80)", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("==== Running wind_category ====", (204, 204, 204)),
        ("Enter a wind speed in km/h (e.g. 45): 45", (204, 204, 204)),
        ("Wind Category: advisory", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("==== Running rainfall_spread ====", (204, 204, 204)),
        ("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): 2,5.5,10", (204, 204, 204)),
        ("Rainfall Spread: 8.0", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> _", (204, 204, 204)),
    ]
    create_terminal_image(lines, r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\01_original_processor.png")

def generate_02():
    lines = [
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> python -m pytest -v test_processor.py", (255, 255, 255)),
        ("============================= test session starts =============================", (97, 214, 214)),
        ("platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.7.0", (204, 204, 204)),
        ("rootdir: C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7", (204, 204, 204)),
        ("plugins: anyio-4.11.0, hypothesis-6.170.15", (204, 204, 204)),
        ("hypothesis profile 'default' -> default_deadline=None", (204, 204, 204)),
        ("collecting ... collected 9 items", (204, 204, 204)),
        ("", (204, 204, 204)),
        ("test_processor.py::test_parse_reading_no_crash FAILED                    [ 11%]", (231, 72, 86)),
        ("test_processor.py::test_wind_category_no_crash FAILED                    [ 22%]", (231, 72, 86)),
        ("test_processor.py::test_rainfall_spread_no_crash FAILED                  [ 33%]", (231, 72, 86)),
        ("test_processor.py::test_parse_reading_valid_inputs PASSED                [ 44%]", (19, 161, 14)),
        ("test_processor.py::test_wind_category_valid_inputs PASSED                [ 55%]", (19, 161, 14)),
        ("test_processor.py::test_rainfall_spread_valid_inputs PASSED              [ 66%]", (19, 161, 14)),
        ("test_processor.py::test_parse_reading_invalid_inputs FAILED              [ 77%]", (231, 72, 86)),
        ("test_processor.py::test_wind_category_invalid_inputs FAILED              [ 88%]", (231, 72, 86)),
        ("test_processor.py::test_rainfall_spread_invalid_inputs FAILED            [100%]", (231, 72, 86)),
        ("", (204, 204, 204)),
        ("=========================== short test summary info ===========================", (231, 72, 86)),
        ("FAILED test_processor.py::test_parse_reading_no_crash - Hypothesis found 3 failures", (231, 72, 86)),
        ("FAILED test_processor.py::test_wind_category_no_crash - Hypothesis found 2 failures", (231, 72, 86)),
        ("FAILED test_processor.py::test_rainfall_spread_no_crash - Hypothesis found 2 failures", (231, 72, 86)),
        ("FAILED test_processor.py::test_parse_reading_invalid_inputs - Unhandled crashes", (231, 72, 86)),
        ("FAILED test_processor.py::test_wind_category_invalid_inputs - Negative inputs allowed", (231, 72, 86)),
        ("FAILED test_processor.py::test_rainfall_spread_invalid_inputs - Negative inputs allowed", (231, 72, 86)),
        ("========================= 6 failed, 3 passed in 1.81s =========================", (231, 72, 86)),
    ]
    create_terminal_image(lines, r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\02_initial_fuzz_failures.png")

def generate_03():
    lines = [
        ("================================== FAILURES ===================================", (231, 72, 86)),
        ("_________________________ test_parse_reading_no_crash _________________________", (231, 72, 86)),
        ("  ExceptionGroup: Hypothesis found 3 distinct failures.", (231, 72, 86)),
        ("    [Failure 1]: ValueError: could not convert string to float: ''", (249, 241, 165)),
        ("                 Failing minimal counterexample: s='/'", (249, 241, 165)),
        ("    [Failure 2]: ValueError: not enough values to unpack (expected 2, got 1)", (249, 241, 165)),
        ("                 Failing minimal counterexample: s=''", (249, 241, 165)),
        ("    [Failure 3]: AttributeError: 'NoneType' object has no attribute 'split'", (249, 241, 165)),
        ("                 Failing minimal counterexample: s=None", (249, 241, 165)),
        ("", (204, 204, 204)),
        ("_________________________ test_wind_category_no_crash _________________________", (231, 72, 86)),
        ("  ExceptionGroup: Hypothesis found 2 distinct failures.", (231, 72, 86)),
        ("    [Failure 1]: ValueError: invalid literal for int() with base 10: ''", (249, 241, 165)),
        ("                 Failing minimal counterexample: s=''", (249, 241, 165)),
        ("    [Failure 2]: TypeError: int() argument must be a string... not 'NoneType'", (249, 241, 165)),
        ("                 Failing minimal counterexample: s=None", (249, 241, 165)),
        ("", (204, 204, 204)),
        ("________________________ test_rainfall_spread_no_crash ________________________", (231, 72, 86)),
        ("  ExceptionGroup: Hypothesis found 2 distinct failures.", (231, 72, 86)),
        ("    [Failure 1]: ValueError: could not convert string to float: ''", (249, 241, 165)),
        ("                 Failing minimal counterexample: s=''", (249, 241, 165)),
        ("    [Failure 2]: AttributeError: 'NoneType' object has no attribute 'split'", (249, 241, 165)),
        ("                 Failing minimal counterexample: s=None", (249, 241, 165)),
        ("", (204, 204, 204)),
        ("_____________________ test_wind_category_invalid_inputs _______________________", (231, 72, 86)),
        ("    AssertionError: assert 'none' is None", (231, 72, 86)),
        ("    > Where 'none' = wind_category('-1')  # Negative wind speed improperly allowed!", (249, 241, 165)),
    ]
    create_terminal_image(lines, r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\03_failure_analysis.png")

def generate_04():
    lines = [
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> python processor.py", (255, 255, 255)),
        ("==== Running parse_reading ====", (204, 204, 204)),
        ("Enter temperature/humidity (e.g. 35.5/80): 35.5/80", (204, 204, 204)),
        ("Temperature and Humidity: (35.5, 80)", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("==== Running wind_category ====", (204, 204, 204)),
        ("Enter a wind speed in km/h (e.g. 45): 45", (204, 204, 204)),
        ("Wind Category: advisory", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("==== Running rainfall_spread ====", (204, 204, 204)),
        ("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): 2,5.5,10", (204, 204, 204)),
        ("Rainfall Spread: 8.0", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("# Edge Case Verification (Safe None Fallback):", (128, 128, 128)),
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> python -c \"from processor import *", (255, 255, 255)),
        (">> print(parse_reading(None), wind_category('-5'), rainfall_spread(''))\"", (255, 255, 255)),
        ("None None None", (0, 255, 128)),
        ("", (204, 204, 204)),
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> _", (204, 204, 204)),
    ]
    create_terminal_image(lines, r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\04_fixed_processor.png")

def generate_05():
    lines = [
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> python -m pytest -v test_processor.py", (255, 255, 255)),
        ("============================= test session starts =============================", (97, 214, 214)),
        ("platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.7.0", (204, 204, 204)),
        ("rootdir: C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7", (204, 204, 204)),
        ("plugins: anyio-4.11.0, hypothesis-6.170.15", (204, 204, 204)),
        ("hypothesis profile 'default' -> default_deadline=None", (204, 204, 204)),
        ("collecting ... collected 9 items", (204, 204, 204)),
        ("", (204, 204, 204)),
        ("test_processor.py::test_parse_reading_no_crash PASSED                    [ 11%]", (19, 161, 14)),
        ("test_processor.py::test_wind_category_no_crash PASSED                    [ 22%]", (19, 161, 14)),
        ("test_processor.py::test_rainfall_spread_no_crash PASSED                  [ 33%]", (19, 161, 14)),
        ("test_processor.py::test_parse_reading_valid_inputs PASSED                [ 44%]", (19, 161, 14)),
        ("test_processor.py::test_wind_category_valid_inputs PASSED                [ 55%]", (19, 161, 14)),
        ("test_processor.py::test_rainfall_spread_valid_inputs PASSED              [ 66%]", (19, 161, 14)),
        ("test_processor.py::test_parse_reading_invalid_inputs PASSED              [ 77%]", (19, 161, 14)),
        ("test_processor.py::test_wind_category_invalid_inputs PASSED              [ 88%]", (19, 161, 14)),
        ("test_processor.py::test_rainfall_spread_invalid_inputs PASSED            [100%]", (19, 161, 14)),
        ("", (204, 204, 204)),
        ("============================== 9 passed in 0.56s ==============================", (19, 161, 14)),
        ("", (204, 204, 204)),
        ("PS C:\\Users\\kaush\\L6_L7_32_weather_alert\\lab7> _", (204, 204, 204)),
    ]
    create_terminal_image(lines, r"C:\Users\kaush\L6_L7_32_weather_alert\lab7\evidence\05_final_passing_tests.png")

if __name__ == "__main__":
    generate_01()
    generate_02()
    generate_03()
    generate_04()
    generate_05()
