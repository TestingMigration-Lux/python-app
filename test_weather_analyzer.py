import pytest
from weather_analyzer import WeatherAnalyzer


@pytest.fixture
def analyzer():
    a = WeatherAnalyzer()
    a.add_record(20, 60, 10, "2024-01-01T10:00:00")
    a.add_record(22, 65, 12, "2024-01-01T11:00:00")
    a.add_record(35, 80, 15, "2024-01-01T12:00:00")
    a.add_record(21, 92, 40, "2024-01-01T13:00:00")
    return a


def test_add_record_valido(analyzer):
    assert len(analyzer.records) == 4


def test_temperatura_non_valida():
    a = WeatherAnalyzer()
    with pytest.raises(ValueError):
        a.add_record(100, 50, 10)


def test_umidita_non_valida():
    a = WeatherAnalyzer()
    with pytest.raises(ValueError):
        a.add_record(20, 150, 10)


def test_vento_non_valido():
    a = WeatherAnalyzer()
    with pytest.raises(ValueError):
        a.add_record(20, 50, -5)


def test_statistiche(analyzer):
    stats = analyzer.get_statistics()
    assert stats["temperature"]["min"] == 20
    assert stats["temperature"]["max"] == 35
    assert stats["temperature"]["avg"] == 24.5
    assert stats["total_records"] == 4


def test_statistiche_vuote():
    a = WeatherAnalyzer()
    assert a.get_statistics() == {}


def test_anomalie(analyzer):
    anomalies = analyzer.detect_anomalies()
    types = [a["type"] for a in anomalies]
    assert "high_temperature" in types
    assert "high_humidity" in types
    assert "high_wind" in types


def test_anomalie_vuote():
    a = WeatherAnalyzer()
    assert a.detect_anomalies() == []


def test_report(analyzer):
    report = analyzer.generate_report()
    assert "generated_at" in report
    assert "statistics" in report
    assert "anomalies" in report
    assert report["anomaly_count"] > 0
