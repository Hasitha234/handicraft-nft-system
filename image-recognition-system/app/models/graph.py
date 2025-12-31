"""
Data models for graph and outlet API responses
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple


class RelatedProduct(BaseModel):
    """Related product information"""
    product_id: str
    relationship: str  # SIMILAR_TO, SAME_MATERIAL, SAME_TYPE
    weight: float
    material: Optional[str] = None
    object_type: Optional[str] = None
    title: Optional[str] = None
    image_filename: Optional[str] = None
    image_url: Optional[str] = None


class Outlet(BaseModel):
    """Outlet/shop information"""
    outlet_id: str
    name: str
    location: str
    coordinates: Optional[Tuple[float, float]] = None
    products: List[str] = []


class RelatedProductsResponse(BaseModel):
    """Response for related products endpoint"""
    product_id: str
    related_products: List[RelatedProduct]
    total_related: int


class OutletRecommendationResponse(BaseModel):
    """Response for outlet recommendations"""
    product_id: Optional[str] = None
    outlets: List[Outlet]
    total_outlets: int

