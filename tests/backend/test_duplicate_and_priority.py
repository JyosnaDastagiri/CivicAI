import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from app.services.duplicate_service import haversine_distance_meters, text_similarity
from app.services.priority_service import SEVERITY_POINTS
from app.models.complaint import Severity


def test_haversine_zero_distance():
    assert haversine_distance_meters(17.38, 78.48, 17.38, 78.48) == 0


def test_haversine_known_distance():
    # Roughly 1 degree latitude ~ 111km
    d = haversine_distance_meters(0, 0, 1, 0)
    assert 110000 < d < 112000


def test_tfidf_cosine_similarity_identical_text():
    sim = text_similarity("large pothole near gate", "large pothole near gate")
    assert sim > 0.99


def test_tfidf_cosine_similarity_different_text():
    sim = text_similarity("large pothole near gate", "garbage overflowing near market")
    assert sim < 0.3


def test_severity_points_ordering():
    assert SEVERITY_POINTS[Severity.CRITICAL] > SEVERITY_POINTS[Severity.HIGH] > SEVERITY_POINTS[Severity.MEDIUM] > SEVERITY_POINTS[Severity.LOW]
