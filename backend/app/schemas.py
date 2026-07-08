from dataclasses import dataclass
from typing import List


@dataclass
class InquiryResult:
    category: str
    subcategory: str
    urgency: str
    needs_human: bool
    confidence: float
    matched_keywords: List[str]

