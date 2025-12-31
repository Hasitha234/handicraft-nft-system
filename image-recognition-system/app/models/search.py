"""
Data models for search API responses
"""

from pydantic import BaseModel
from typing import List, Dict, Optional


class SearchResult(BaseModel):
    """Single search result item"""
    product_id: str
    title: str
    description: str
    similarity_score: float  # 0.0 to 1.0 (final weighted score)
    rank: int
    per_feature_scores: Optional[Dict[str, float]] = None  # Per-feature similarity scores
    predicted_material: Optional[str] = None
    predicted_object_type: Optional[str] = None
    image_filename: Optional[str] = None  # Original image filename
    image_url: Optional[str] = None       # URL to access the image (served by backend)


class SearchResponse(BaseModel):
    """Response model for image search endpoint"""
    query_id: str
    results: List[SearchResult]
    total_matches: int
    query_features: Optional[Dict] = None  # Extracted features from query image



