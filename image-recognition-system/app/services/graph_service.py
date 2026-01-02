"""
Graph Database Service for Product Relationships
Uses NetworkX for lightweight graph operations (MVP approach)
Can be upgraded to Neo4j later for production
"""

import networkx as nx
import json
import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class GraphService:
    """Manages product relationships and outlet connections"""
    
    def __init__(self, graph_path: str = "data/product_graph.json"):
        """
        Initialize graph service
        
        Args:
            graph_path: Path to save/load graph data
        """
        self.graph_path = graph_path
        self.graph = nx.Graph()  # Undirected graph for product relationships
        self.outlets: Dict[str, Dict] = {}  # Outlet data: {outlet_id: {name, location, products}}
        self.product_outlets: Dict[str, List[str]] = {}  # product_id -> [outlet_ids]
        
        # Load existing graph if available
        self._load_graph()
    
    def _load_graph(self):
        """Load graph from disk"""
        if os.path.exists(self.graph_path):
            try:
                with open(self.graph_path, 'r') as f:
                    data = json.load(f)
                    
                    # Reconstruct graph
                    self.graph = nx.node_link_graph(data.get('graph', {}))
                    self.outlets = data.get('outlets', {})
                    self.product_outlets = data.get('product_outlets', {})
                    
                    print(f"[OK] Loaded graph with {len(self.graph.nodes)} products and {len(self.graph.edges)} relationships")
            except Exception as e:
                print(f"[INFO] Could not load graph: {e}. Starting fresh.")
                self.graph = nx.Graph()
    
    def _save_graph(self):
        """Save graph to disk"""
        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)
        
        data = {
            'graph': nx.node_link_data(self.graph),
            'outlets': self.outlets,
            'product_outlets': self.product_outlets
        }
        
        with open(self.graph_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_product(self, product_id: str, metadata: Dict):
        """
        Add a product node to the graph
        
        Args:
            product_id: Unique product identifier
            metadata: Product metadata (material, object_type, etc.)
        """
        if not self.graph.has_node(product_id):
            self.graph.add_node(product_id, **metadata)
            self._save_graph()
    
    def add_relationship(self, product_id1: str, product_id2: str, 
                        relationship_type: str = "SIMILAR_TO", weight: float = 1.0):
        """
        Add relationship between two products
        
        Args:
            product_id1: First product ID
            product_id2: Second product ID
            relationship_type: Type of relationship (SIMILAR_TO, SAME_MATERIAL, SAME_TYPE)
            weight: Relationship strength (0.0 to 1.0)
        """
        if self.graph.has_node(product_id1) and self.graph.has_node(product_id2):
            self.graph.add_edge(product_id1, product_id2, 
                              relationship=relationship_type, weight=weight)
            self._save_graph()
    
    def build_relationships_from_features(self, products: List[Dict], features: Dict[str, Dict]):
        """
        Build product relationships based on extracted features
        
        Args:
            products: List of product metadata
            features: Dict of {product_id: features}
        """
        print(f"[INFO] Building relationships for {len(products)} products...")
        
        # Add all products as nodes
        for product in products:
            product_id = product['id']
            product_features = features.get(product_id, {})
            
            metadata = {
                'material': product_features.get('material', {}).get('predicted_material', 'unknown'),
                'object_type': product_features.get('object_type', {}).get('predicted_type', 'unknown'),
                'title': product.get('metadata', {}).get('title', '')
            }
            self.add_product(product_id, metadata)
        
        # Build relationships
        product_ids = list(features.keys())
        relationship_count = 0
        
        for i, pid1 in enumerate(product_ids):
            for pid2 in product_ids[i+1:]:
                feat1 = features.get(pid1, {})
                feat2 = features.get(pid2, {})
                
                # Same material relationship
                mat1 = feat1.get('material', {}).get('predicted_material')
                mat2 = feat2.get('material', {}).get('predicted_material')
                if mat1 and mat2 and mat1 == mat2:
                    self.add_relationship(pid1, pid2, "SAME_MATERIAL", weight=0.8)
                    relationship_count += 1
                
                # Same object type relationship
                type1 = feat1.get('object_type', {}).get('predicted_type')
                type2 = feat2.get('object_type', {}).get('predicted_type')
                if type1 and type2 and type1 == type2:
                    self.add_relationship(pid1, pid2, "SAME_TYPE", weight=0.7)
                    relationship_count += 1
        
        print(f"[OK] Created {relationship_count} relationships")
        self._save_graph()
    
    def get_related_products(self, product_id: str, max_results: int = 5) -> List[Dict]:
        """
        Get products related to a given product
        
        Args:
            product_id: Product to find related items for
            max_results: Maximum number of results
            
        Returns:
            List of related product IDs with relationship info
        """
        if not self.graph.has_node(product_id):
            return []
        
        # Get neighbors (directly connected products)
        neighbors = list(self.graph.neighbors(product_id))
        
        results = []
        for neighbor_id in neighbors[:max_results]:
            edge_data = self.graph.get_edge_data(product_id, neighbor_id, {})
            results.append({
                'product_id': neighbor_id,
                'relationship': edge_data.get('relationship', 'SIMILAR_TO'),
                'weight': edge_data.get('weight', 1.0),
                'metadata': self.graph.nodes[neighbor_id]
            })
        
        # Sort by weight (strongest relationships first)
        results.sort(key=lambda x: x['weight'], reverse=True)
        
        return results
    
    def add_outlet(self, outlet_id: str, name: str, location: str, 
                   coordinates: Optional[Tuple[float, float]] = None,
                   products: Optional[List[str]] = None):
        """
        Add an outlet/shop
        
        Args:
            outlet_id: Unique outlet identifier
            name: Shop name
            location: Address or location description
            coordinates: (latitude, longitude) if available
            products: List of product IDs sold at this outlet
        """
        self.outlets[outlet_id] = {
            'name': name,
            'location': location,
            'coordinates': coordinates,
            'products': products or []
        }
        
        # Update product-outlet mapping
        for product_id in (products or []):
            if product_id not in self.product_outlets:
                self.product_outlets[product_id] = []
            if outlet_id not in self.product_outlets[product_id]:
                self.product_outlets[product_id].append(outlet_id)
        
        self._save_graph()
    
    def get_outlets_for_product(self, product_id: str) -> Dict[str, Dict]:
        """
        Get outlets selling a specific product
        
        Args:
            product_id: Product to find outlets for
            
        Returns:
            Dict mapping outlet_id -> outlet info
        """
        outlet_ids = self.product_outlets.get(product_id, [])
        result = {}
        for oid in outlet_ids:
            if oid in self.outlets:
                outlet_info = self.outlets[oid].copy()
                outlet_info['outlet_id'] = oid
                result[oid] = outlet_info
        return result
    
    def find_outlets_for_products(self, product_ids: List[str]) -> Dict[str, Dict[str, Dict]]:
        """
        Find outlets for multiple products
        
        Args:
            product_ids: List of product IDs
            
        Returns:
            Dict mapping product_id -> dict of {outlet_id: outlet_info}
        """
        result = {}
        for product_id in product_ids:
            result[product_id] = self.get_outlets_for_product(product_id)
        return result
    
    def get_statistics(self) -> Dict:
        """Get graph statistics"""
        return {
            'total_products': len(self.graph.nodes),
            'total_relationships': len(self.graph.edges),
            'total_outlets': len(self.outlets),
            'products_with_outlets': len(self.product_outlets)
        }

