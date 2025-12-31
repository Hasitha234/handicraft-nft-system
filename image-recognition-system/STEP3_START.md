# Step 3: Graph Database + Outlet Recommendations 🚀

## What's Been Built

### ✅ Graph Service (`app/services/graph_service.py`)
- Product relationship graph using NetworkX
- Stores relationships: `SAME_MATERIAL`, `SAME_TYPE`, `SIMILAR_TO`
- Outlet/shop management
- Product-outlet associations

### ✅ Graph API Endpoints
- `GET /api/v1/products/{id}/related` - Get related products
- `GET /api/v1/products/{id}/outlets` - Find shops selling product
- `POST /api/v1/outlets` - Add new outlet/shop
- `GET /api/v1/graph/stats` - Graph statistics

### ✅ Graph Builder Script
- `scripts/build_graph.py` - Builds relationships from indexed products

## Next Steps to Complete Step 3

### 1. Install NetworkX
```bash
cd image-recognition-system
venv\Scripts\activate
pip install networkx
```

### 2. Build the Graph
```bash
python scripts/build_graph.py
```

This will:
- Load all indexed products
- Create relationships based on material and object type
- Save graph to `data/product_graph.json`

### 3. Add Sample Outlets
You can add outlets via API or create a script. Example:

```python
# Via API
POST /api/v1/outlets
{
  "outlet_id": "shop_001",
  "name": "Traditional Handicrafts Shop",
  "location": "Kandy, Sri Lanka",
  "latitude": 7.2906,
  "longitude": 80.6337,
  "products": ["1", "2", "3", "15"]
}
```

### 4. Test Graph Endpoints

```bash
# Get related products
curl http://localhost:8000/api/v1/products/1/related

# Get outlets for a product
curl http://localhost:8000/api/v1/products/1/outlets

# Get graph statistics
curl http://localhost:8000/api/v1/graph/stats
```

## What This Enables

1. **Related Products**: After a search, users can explore similar products
2. **Outlet Discovery**: Find where products are sold
3. **Product Relationships**: Understand connections between handicrafts
4. **Foundation for Routes**: Can add route planning later

## Integration with Search

The graph can be integrated into search results:
- Add "related products" to each search result
- Add "available at" outlets for each product
- Enable product exploration beyond initial search

## Current Status

- ✅ Graph service implemented
- ✅ API endpoints created
- ✅ Graph builder script ready
- ⏳ Need to: Install NetworkX, build graph, add outlets

Ready to proceed! 🎯


