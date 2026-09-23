"""
AIService abstraction (Requirement #35 / #9 / #10 / #11).

Two implementations are provided:
  - DemoAIService  : deterministic, offline, used when AI_MODE=demo or when
                     the live provider fails/has no key. Guarantees the app
                     NEVER crashes because of a missing AI key.
  - GeminiAIService: calls Google Gemini's multimodal API when AI_MODE=live
                     and GEMINI_API_KEY is configured.

Both implement the same interface: analyze_image() and generate_complaint().
"""
from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Optional

import httpx

from app.core.config import get_settings

settings = get_settings()

CATEGORY_KEYWORDS = {
    "Pothole": ["pothole", "hole", "crater"],
    "Road Damage": ["road", "crack", "asphalt", "pavement damage"],
    "Garbage": ["garbage", "trash", "waste", "dump", "litter"],
    "Broken Streetlight": ["streetlight", "street light", "lamp", "pole light"],
    "Water Leakage": ["water leak", "pipe burst", "leakage", "leaking"],
    "Drainage": ["drain", "sewage", "clogged", "overflow"],
    "Fallen Tree": ["tree", "branch", "fallen"],
    "Damaged Road Sign": ["sign", "signage", "signpost"],
}

SAFETY_KEYWORDS = ["danger", "accident", "risk", "unsafe", "falling", "collapse", "injur"]
HIGH_SEVERITY_KEYWORDS = ["large", "big", "huge", "severe", "major", "deep", "burst", "collapsed"]


def _guess_category(text: str) -> str:
    text_l = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in text_l for k in keywords):
            return category
    return "General Civic Issue"


def _guess_severity(text: str) -> str:
    text_l = text.lower()
    if any(k in text_l for k in HIGH_SEVERITY_KEYWORDS):
        return "HIGH"
    if any(k in text_l for k in SAFETY_KEYWORDS):
        return "HIGH"
    return "MEDIUM"


def _guess_safety_risk(text: str) -> bool:
    text_l = text.lower()
    return any(k in text_l for k in SAFETY_KEYWORDS) or any(
        k in text_l for k in ["pothole", "wire", "electric", "tree", "water"]
    )


class AIService(ABC):
    provider_name: str = "abstract"

    @abstractmethod
    def analyze_image(self, image_url: str, description: Optional[str] = None) -> dict:
        ...

    @abstractmethod
    def generate_complaint(
        self,
        citizen_description: str,
        category: str,
        severity: str,
        safety_risk: bool,
        address: Optional[str] = None,
    ) -> dict:
        ...


class DemoAIService(AIService):
    """Deterministic, offline AI simulation used for AI_MODE=demo."""

    provider_name = "demo"

    def analyze_image(self, image_url: str, description: Optional[str] = None) -> dict:
        basis = f"{description or ''} {image_url or ''}"
        category = _guess_category(basis)
        severity = _guess_severity(basis)
        safety_risk = _guess_safety_risk(basis)
        confidence = 0.91 if description else 0.75
        return {
            "category": category,
            "severity": severity,
            "safetyRisk": safety_risk,
            "description": f"{category} detected from the uploaded image and description.",
            "confidence": confidence,
            "provider": self.provider_name,
        }

    def generate_complaint(
        self,
        citizen_description: str,
        category: str,
        severity: str,
        safety_risk: bool,
        address: Optional[str] = None,
    ) -> dict:
        risk_phrase = (
            "poses a potential safety risk to the public and requires urgent inspection"
            if safety_risk
            else "requires inspection and timely repair"
        )
        location_phrase = f" near {address}" if address else ""
        title = f"{category} reported{location_phrase}"
        description = (
            f"{category} reported{location_phrase}. Based on the citizen's report, the issue "
            f"({citizen_description.strip().rstrip('.')}) {risk_phrase}. Severity has been assessed as "
            f"{severity.title()}."
        )
        return {
            "title": title[:200],
            "description": description,
            "category": category,
            "severity": severity,
            "safetyRisk": safety_risk,
            "provider": self.provider_name,
        }


class GeminiAIService(AIService):
    """Calls Google Gemini's generateContent endpoint. Falls back to Demo on any failure."""

    provider_name = "gemini"

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.fallback = DemoAIService()

    def _endpoint(self) -> str:
        return (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

    def _call(self, prompt: str, image_url: Optional[str] = None) -> Optional[str]:
        if not self.api_key:
            return None
        parts = [{"text": prompt}]
        try:
            with httpx.Client(timeout=20) as client:
                payload = {"contents": [{"parts": parts}]}
                resp = client.post(self._endpoint(), json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return None

    @staticmethod
    def _extract_json(text: str) -> Optional[dict]:
        if not text:
            return None
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    def analyze_image(self, image_url: str, description: Optional[str] = None) -> dict:
        prompt = (
            "You are a civic issue detection assistant. Analyze the described civic issue "
            f"image located at {image_url} with citizen note: '{description or ''}'. "
            'Respond ONLY with JSON: {"category":"...","severity":"LOW|MEDIUM|HIGH|CRITICAL",'
            '"safetyRisk":true|false,"description":"...","confidence":0.0}'
        )
        raw = self._call(prompt)
        parsed = self._extract_json(raw) if raw else None
        if not parsed:
            return self.fallback.analyze_image(image_url, description)
        parsed.setdefault("provider", self.provider_name)
        return parsed

    def generate_complaint(
        self,
        citizen_description: str,
        category: str,
        severity: str,
        safety_risk: bool,
        address: Optional[str] = None,
    ) -> dict:
        prompt = (
            "Convert the following citizen civic complaint into a professional structured "
            f"complaint. Citizen description: '{citizen_description}'. Category: {category}. "
            f"Severity: {severity}. Safety risk: {safety_risk}. Location: {address or 'unspecified'}. "
            'Respond ONLY with JSON: {"title":"...","description":"...","category":"...",'
            '"severity":"...","safetyRisk":true|false}'
        )
        raw = self._call(prompt)
        parsed = self._extract_json(raw) if raw else None
        if not parsed:
            return self.fallback.generate_complaint(citizen_description, category, severity, safety_risk, address)
        parsed.setdefault("provider", self.provider_name)
        return parsed


def get_ai_service() -> AIService:
    """Factory: returns the configured AI service. Never raises."""
    if settings.AI_MODE == "live" and settings.GEMINI_API_KEY:
        return GeminiAIService()
    return DemoAIService()
