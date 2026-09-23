"""
Lightweight duplicate detection (Requirement #12).

Uses only:
  - TF-IDF vectorization (scikit-learn)
  - Cosine similarity
  - Haversine GPS distance
  - Category matching

No deep-learning embeddings are used.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from math import radians, sin, cos, asin, sqrt
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_location import ComplaintLocation
from app.models.complaint_duplicate import ComplaintDuplicate
from app.services.settings_service import get_setting_float

EARTH_RADIUS_METERS = 6371000


def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points, in meters."""
    lat1r, lon1r, lat2r, lon2r = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2r - lat1r
    dlon = lon2r - lon1r
    a = sin(dlat / 2) ** 2 + cos(lat1r) * cos(lat2r) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_METERS * c


def text_similarity(text_a: str, text_b: str) -> float:
    """TF-IDF + cosine similarity between two short texts."""
    if not text_a.strip() or not text_b.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform([text_a, text_b])
    except ValueError:
        return 0.0
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(sim)


def find_duplicates(db: Session, complaint: Complaint, lookback_days: int = 30) -> list[ComplaintDuplicate]:
    """
    Compares a new complaint against recent complaints of the same category
    within a lookback window, using TF-IDF text similarity + GPS distance.
    """
    threshold = get_setting_float(db, "TEXT_SIMILARITY_THRESHOLD")
    radius = get_setting_float(db, "DUPLICATE_RADIUS_METERS")

    since = datetime.utcnow() - timedelta(days=lookback_days)
    candidates = (
        db.query(Complaint)
        .filter(
            Complaint.id != complaint.id,
            Complaint.created_at >= since,
            Complaint.category == complaint.category,
        )
        .all()
    )

    my_location = db.query(ComplaintLocation).filter(ComplaintLocation.complaint_id == complaint.id).first()
    results: list[ComplaintDuplicate] = []

    for other in candidates:
        other_location = db.query(ComplaintLocation).filter(ComplaintLocation.complaint_id == other.id).first()
        if not my_location or not other_location:
            continue

        sim = text_similarity(
            f"{complaint.title} {complaint.description}", f"{other.title} {other.description}"
        )
        distance = haversine_distance_meters(
            my_location.latitude, my_location.longitude, other_location.latitude, other_location.longitude
        )
        category_match = complaint.category == other.category
        duplicate_score = round((sim * 0.7 + (1 - min(distance / max(radius, 1), 1)) * 0.3) * 100, 2)
        is_dup = sim >= threshold and distance <= radius and category_match

        record = ComplaintDuplicate(
            complaint_id=complaint.id,
            similar_complaint_id=other.id,
            text_similarity=round(sim, 4),
            distance_meters=round(distance, 2),
            category_match=category_match,
            duplicate_score=duplicate_score,
            is_potential_duplicate=is_dup,
        )
        db.add(record)
        results.append(record)

    if results:
        db.commit()
    return results
