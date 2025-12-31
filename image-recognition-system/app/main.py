"""
FastAPI main application for Image Recognition System
MVP: CLIP-based image similarity search
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from typing import Dict, List

from app.models.search import SearchResponse, SearchResult
from app.models.graph import RelatedProductsResponse, OutletRecommendationResponse, RelatedProduct, Outlet
from app.services.image_processor import ImageProcessor
from app.services.clip_encoder import CLIPEncoder
from app.services.vector_store import VectorStore
from app.services.enhanced_vector_store import EnhancedVectorStore
from app.services.feature_extractors.master_extractor import MasterFeatureExtractor
from app.services.graph_service import GraphService

app = FastAPI(
    title="Handicraft Image Recognition API",
    description="Image similarity search system for Sri Lankan handicrafts",
    version="0.1.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve product images statically from /images
app.mount("/images", StaticFiles(directory="images"), name="images")

# Initialize services (lazy loading in production)
image_processor = None
clip_encoder = None
vector_store = None
enhanced_vector_store = None
feature_extractor = None
graph_service = None
use_enhanced_features = True  # Toggle to use enhanced features


@app.on_event("startup")
async def startup_event():
    """Initialize models and services on startup"""
    global image_processor, clip_encoder, vector_store, enhanced_vector_store, feature_extractor, graph_service, use_enhanced_features
    
    print("[INFO] Initializing Image Recognition System...")
    
    # Initialize services
    image_processor = ImageProcessor()
    clip_encoder = CLIPEncoder()
    
    # Initialize feature extractor
    feature_extractor = MasterFeatureExtractor()
    
    # Initialize vector stores
    vector_store = VectorStore()
    enhanced_vector_store = EnhancedVectorStore()
    
    # Initialize graph service
    graph_service = GraphService()
    
    # Load or create indexes
    vector_store.load_or_create_index(clip_encoder, create_sample_data=False)
    
    # Try to load enhanced store, fallback to basic if no features exist
    try:
        enhanced_vector_store.load_or_create_index(clip_encoder, create_sample_data=False)
        if len(enhanced_vector_store.features) == 0:
            print("[INFO] No enhanced features found. Using basic CLIP search.")
            print("[INFO] Run: python scripts/reindex_with_features.py to enable multi-feature search")
            use_enhanced_features = False
        else:
            print(f"[OK] Enhanced features loaded for {len(enhanced_vector_store.features)} products")
            use_enhanced_features = True
    except Exception as e:
        print(f"[INFO] Enhanced vector store not available: {e}")
        print("[INFO] Using basic CLIP search.")
        use_enhanced_features = False
    
    print("[OK] System ready!")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Handicraft Image Recognition API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check with system status"""
    return {
        "status": "healthy",
        "services": {
            "image_processor": image_processor is not None,
            "clip_encoder": clip_encoder is not None,
            "vector_store": vector_store is not None
        }
    }


@app.post("/api/v1/search", response_model=SearchResponse)
async def search_image(file: UploadFile = File(...)):
    """
    Search for similar handicraft products by uploading an image
    
    Uses multi-feature similarity if enhanced features are available,
    otherwise falls back to CLIP-only search.
    
    Args:
        file: Image file (JPG, PNG, etc.)
        
    Returns:
        SearchResponse with top matches, similarity scores, and per-feature breakdown
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read uploaded image
        image_bytes = await file.read()
        
        # Preprocess image
        processed_image = image_processor.preprocess(image_bytes)
        
        # Extract CLIP embedding
        query_clip = clip_encoder.encode_image(processed_image)
        
        # Check if enhanced features are available
        global enhanced_vector_store, feature_extractor, use_enhanced_features
        
        # Debug: Check feature availability
        has_features = enhanced_vector_store and len(enhanced_vector_store.features) > 0
        
        if use_enhanced_features and has_features:
            # Use enhanced multi-feature search
            query_features = feature_extractor.extract_all(processed_image)
            
            # Prepare features for similarity computation
            query_features_dict = {
                'geometric': query_features['geometric'],
                'color': query_features['color'],
                'texture': query_features['texture'],
                'pattern': query_features['pattern'],
                'material': query_features['material'],
                'object_type': query_features['object_type'],
                'clip': query_clip
            }
            
            results = enhanced_vector_store.search_with_features(
                query_clip, query_features_dict, top_k=5
            )
            
            # Include query features in response
            query_features_summary = {
                'material': query_features['material']['predicted_material'],
                'object_type': query_features['object_type']['predicted_type'],
                'edge_count': query_features['geometric']['edge_count'],
                'dominant_colors': len(query_features['color']['dominant_colors'])
            }
        else:
            # Fallback to basic CLIP search
            results = vector_store.search(query_clip, top_k=5)
            query_features_summary = None
        
        return SearchResponse(
            query_id=file.filename or "upload",
            results=results,
            total_matches=len(results),
            query_features=query_features_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/api/v1/upload-product")
async def upload_product(
    file: UploadFile = File(...),
    product_id: str = None,
    title: str = None,
    description: str = None
):
    """
    Add a product image to the vector database (for indexing products)
    
    This endpoint allows you to add new product images to the search index
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image
        image_bytes = await file.read()
        
        # Preprocess
        processed_image = image_processor.preprocess(image_bytes)
        
        # Extract embedding
        embedding = clip_encoder.encode_image(processed_image)
        
        # Add to vector store
        product_id = product_id or f"product_{len(vector_store.products)}"
        vector_store.add_product(
            product_id=product_id,
            embedding=embedding,
            metadata={
                "title": title or "Unknown Product",
                "description": description or "",
                "filename": file.filename
            }
        )
        
        return {
            "status": "success",
            "product_id": product_id,
            "message": "Product added to index"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding product: {str(e)}")


@app.get("/api/v1/products/{product_id}/related", response_model=RelatedProductsResponse)
async def get_related_products(product_id: str, max_results: int = 5):
    """
    Get products related to a specific product
    
    Uses graph relationships to find similar products based on:
    - Same material
    - Same object type
    - Feature similarity
    """
    if not graph_service:
        raise HTTPException(status_code=503, detail="Graph service not available")
    
    related = graph_service.get_related_products(product_id, max_results)
    
    # Enrich with metadata from vector store
    enriched_related = []
    for rel in related:
        # Try to get product metadata
        product_meta = None
        if enhanced_vector_store:
            for p in enhanced_vector_store.products:
                if p['id'] == rel['product_id']:
                    product_meta = p.get('metadata', {})
                    break
        
        filename = None
        image_url = None
        if product_meta:
            filename = product_meta.get('filename')
            if filename:
                image_url = f"/images/{filename}"
        
        enriched_related.append(RelatedProduct(
            product_id=rel['product_id'],
            relationship=rel['relationship'],
            weight=rel['weight'],
            material=rel.get('metadata', {}).get('material'),
            object_type=rel.get('metadata', {}).get('object_type'),
            title=rel.get('metadata', {}).get('title') or (product_meta.get('title') if product_meta else None),
            image_filename=filename,
            image_url=image_url
        ))
    
    return RelatedProductsResponse(
        product_id=product_id,
        related_products=enriched_related,
        total_related=len(enriched_related)
    )


@app.get("/api/v1/products/{product_id}/outlets", response_model=OutletRecommendationResponse)
async def get_product_outlets(product_id: str):
    """
    Get outlets/shops selling a specific product
    """
    if not graph_service:
        raise HTTPException(status_code=503, detail="Graph service not available")
    
    outlets_data = graph_service.get_outlets_for_product(product_id)
    
    outlets = [
        Outlet(
            outlet_id=oid,
            name=outlet['name'],
            location=outlet['location'],
            coordinates=outlet.get('coordinates'),
            products=outlet.get('products', [])
        )
        for oid, outlet in outlets_data.items()
    ]
    
    return OutletRecommendationResponse(
        product_id=product_id,
        outlets=outlets,
        total_outlets=len(outlets)
    )


@app.get("/api/v1/search/{query_id}/outlets", response_model=Dict[str, List[Outlet]])
async def get_search_outlets(query_id: str):
    """
    Get outlets for all products in a search result
    
    This endpoint would typically be called after a search to find
    where the matched products can be purchased.
    """
    if not graph_service:
        raise HTTPException(status_code=503, detail="Graph service not available")
    
    # In a real implementation, you'd store search results temporarily
    # For now, this is a placeholder that shows the concept
    return {
        "message": "Search result outlets endpoint",
        "note": "This would return outlets for products from a previous search"
    }


@app.post("/api/v1/outlets")
async def add_outlet(
    outlet_id: str,
    name: str,
    location: str,
    latitude: float = None,
    longitude: float = None,
    products: List[str] = None
):
    """
    Add a new outlet/shop
    
    Args:
        outlet_id: Unique identifier for the outlet
        name: Shop name
        location: Address or location description
        latitude: Latitude coordinate (optional)
        longitude: Longitude coordinate (optional)
        products: List of product IDs sold at this outlet
    """
    if not graph_service:
        raise HTTPException(status_code=503, detail="Graph service not available")
    
    coordinates = None
    if latitude is not None and longitude is not None:
        coordinates = (latitude, longitude)
    
    graph_service.add_outlet(
        outlet_id=outlet_id,
        name=name,
        location=location,
        coordinates=coordinates,
        products=products or []
    )
    
    return {
        "status": "success",
        "outlet_id": outlet_id,
        "message": "Outlet added successfully"
    }


@app.get("/api/v1/graph/stats")
async def get_graph_stats():
    """Get graph database statistics"""
    if not graph_service:
        raise HTTPException(status_code=503, detail="Graph service not available")
    
    return graph_service.get_statistics()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

