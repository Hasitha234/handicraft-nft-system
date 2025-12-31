import React from 'react';
import ProductCard from './ProductCard';

const SearchResults = ({ results, queryFeatures, queryImage }) => {
  if (!results || results.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No results found. Try uploading a different image.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {queryFeatures && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">Query Image Analysis:</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            {queryFeatures.edge_count && (
              <div>
                <span className="text-gray-600">Edge Count:</span>
                <span className="ml-2 font-medium">{queryFeatures.edge_count.toLocaleString()}</span>
              </div>
            )}
            {queryFeatures.dominant_colors && (
              <div>
                <span className="text-gray-600">Dominant Colors:</span>
                <span className="ml-2 font-medium">{queryFeatures.dominant_colors}</span>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-800">
          Search Results ({results.length} matches)
        </h2>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {results.map((product, index) => (
          <ProductCard
            key={product.product_id}
            product={product}
            rank={product.rank}
            queryImage={queryImage}
          />
        ))}
      </div>
    </div>
  );
};

export default SearchResults;


