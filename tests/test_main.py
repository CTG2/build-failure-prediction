from app.main import calculate_build_risk, get_build_status


def test_calculate_build_risk():
    result = calculate_build_risk(3, 10)

    assert result == 0.3


def test_low_risk():
    assert get_build_status(0.30) == "LOW"


def test_medium_risk():
    assert get_build_status(0.50) == "MEDIUM"


def test_high_risk():
    assert get_build_status(0.80) == "HIGH"