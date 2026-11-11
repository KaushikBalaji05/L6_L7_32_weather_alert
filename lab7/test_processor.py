"""Hypothesis property-based tests for Lab 7 processor.py."""

import math
from hypothesis import given, strategies as st
from processor import parse_reading, wind_category, rainfall_spread


# =====================================================================
# 1. Robustness / No-Crash Fuzz Tests
# =====================================================================

@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    """Fuzz test: parse_reading must not crash on arbitrary text or None."""
    try:
        result = parse_reading(s)
        if result is not None:
            assert isinstance(result, tuple)
            assert len(result) == 2
            temp, hum = result
            assert isinstance(temp, (int, float))
            assert isinstance(hum, int)
            assert not math.isnan(temp)
    except Exception as e:
        assert False, f"parse_reading crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    """Fuzz test: wind_category must not crash on arbitrary text or None."""
    try:
        result = wind_category(s)
        if result is not None:
            assert result in ("warning", "advisory", "none")
    except Exception as e:
        assert False, f"wind_category crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    """Fuzz test: rainfall_spread must not crash on arbitrary text or None."""
    try:
        result = rainfall_spread(s)
        if result is not None:
            assert isinstance(result, (float, int))
            assert result >= 0
            assert not math.isnan(result)
    except Exception as e:
        assert False, f"rainfall_spread crashed with {type(e).__name__}: {e}"


# =====================================================================
# 2. Correctness Property Tests on Valid Inputs
# =====================================================================

@given(
    st.floats(min_value=-50.0, max_value=60.0, allow_nan=False, allow_infinity=False),
    st.integers(min_value=0, max_value=100)
)
def test_parse_reading_valid_inputs(temp, humidity):
    """Correctness test: valid temperature and humidity return parsed numbers."""
    formatted = f"{temp:.2f}/{humidity}"
    result = parse_reading(formatted)
    assert result is not None
    res_temp, res_hum = result
    assert math.isclose(res_temp, float(f"{temp:.2f}"), abs_tol=1e-4)
    assert res_hum == humidity


@given(st.integers(min_value=0, max_value=300))
def test_wind_category_valid_inputs(speed):
    """Correctness test: valid non-negative speeds map to correct category."""
    result = wind_category(str(speed))
    if speed >= 89:
        assert result == "warning"
    elif speed >= 39:
        assert result == "advisory"
    else:
        assert result == "none"


@given(st.lists(
    st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    min_size=1, max_size=20
))
def test_rainfall_spread_valid_inputs(readings):
    """Correctness test: valid non-negative rainfall numbers compute spread."""
    formatted = ",".join(f"{r:.2f}" for r in readings)
    parsed_vals = [float(f"{r:.2f}") for r in readings]
    expected = max(parsed_vals) - min(parsed_vals)
    result = rainfall_spread(formatted)
    assert result is not None
    assert math.isclose(result, expected, abs_tol=1e-4)


# =====================================================================
# 3. Invalid Input Rejection Tests
# =====================================================================

@given(st.sampled_from(["", "abc", "25/", "/80", "25//80", "25/80/90", "25/abc", "abc/80", None, "   "]))
def test_parse_reading_invalid_inputs(s):
    """Validation test: malformed reading inputs are rejected safely with None."""
    assert parse_reading(s) is None


@given(st.sampled_from(["", "abc", "-1", "-50", "45.5", None, "   ", "warning"]))
def test_wind_category_invalid_inputs(s):
    """Validation test: non-integer or negative speeds are rejected safely with None."""
    assert wind_category(s) is None


@given(st.sampled_from(["", "abc", "1,2,abc", "1,,3", "-5,10", None, "   "]))
def test_rainfall_spread_invalid_inputs(s):
    """Validation test: malformed CSV or negative values are rejected safely with None."""
    assert rainfall_spread(s) is None
