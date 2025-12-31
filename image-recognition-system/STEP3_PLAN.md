# Step 3: Graph Database + Outlet Recommendation System

## Overview

Add a graph database to model product relationships and implement outlet/shop recommendation system. This enables:
- **Related Products**: Find products similar to search results
- **Product Relationships**: Material-based, type-based, style-based connections
- **Outlet Matching**: Match products to physical shops/outlets
- **Route Planning**: Find shops selling similar products

## Components to Build

### 1. Graph Database Service (Neo4j)
- **Purpose**: Store product relationships
- **Relationships**:
  - `SIMILAR_TO` (based on features)
  - `SAME_MATERIAL` (material match)
  - `SAME_TYPE` (object type match)
  - `SOLD_AT` (product → outlet)
  - `NEARBY` (outlet → outlet)

### 2. Outlet/Shop Data Model
- Shop metadata (name, location, coordinates, category)
- Product-shop associations
- Shop inventory

### 3. Outlet Recommendation Service
- Match products to shops
- Find shops selling similar products
- Calculate distances/routes
- Rank by relevance + proximity

### 4. API Endpoints
- `GET /api/v1/products/{id}/related` - Get related products
- `GET /api/v1/products/{id}/outlets` - Find shops selling product
- `GET /api/v1/search/{query_id}/outlets` - Find shops for search results
- `POST /api/v1/outlets` - Add new outlet
- `GET /api/v1/outlets/nearby` - Find nearby shops

## Implementation Steps

### Step 3.1: Setup Neo4j (Optional - Can use in-memory graph for MVP)
- Install Neo4j driver OR use NetworkX for MVP
- Create graph service wrapper
- Define node and relationship schemas

### Step 3.2: Build Graph Service
- Create product nodes
- Create relationship edges
- Query related products
- Build product similarity graph

### Step 3.3: Outlet Data Model
- Define outlet schema
- Create outlet storage (can use JSON/PostgreSQL)
- Add product-outlet associations

### Step 3.4: Outlet Recommendation Engine
- Match products to outlets
- Calculate recommendation scores
- Filter by location (if coordinates provided)
- Rank by relevance

### Step 3.5: Integrate with Search API
- Add related products to search results
- Add outlet recommendations
- Update response models

## Alternative: Lightweight MVP Approach

For faster implementation, we can use:
- **NetworkX** (Python graph library) instead of Neo4j
- **JSON file** for outlet data (instead of full database)
- **Simple distance calculation** (if coordinates provided)

This keeps dependencies minimal while still demonstrating the concept.

## Expected Outcomes

After Step 3:
- ✅ Product relationship graph
- ✅ Related products API
- ✅ Outlet recommendation API
- ✅ Shop matching for search results
- ✅ Foundation for route planning

## Next Steps After Step 3

- Step 4: Frontend UI (React/Vue)
- Step 5: Advanced filtering & sorting
- Step 6: User feedback & retraining pipeline


