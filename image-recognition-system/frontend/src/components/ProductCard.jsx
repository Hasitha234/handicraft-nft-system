import React, { useState } from 'react';
import FeatureBreakdown from './FeatureBreakdown';
import { getRelatedProducts, getProductOutlets } from '../services/api';

const ProductCard = ({ product, rank, queryImage }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [relatedProducts, setRelatedProducts] = useState(null);
  const [outlets, setOutlets] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleShowDetails = async () => {
    if (showDetails) {
      setShowDetails(false);
      return;
    }

    setLoading(true);
    setShowDetails(true);

    try {
      const [related, outletData] = await Promise.all([
        getRelatedProducts(product.product_id),
        getProductOutlets(product.product_id),
      ]);
      setRelatedProducts(related);
      setOutlets(outletData);
    } catch (error) {
      console.error('Error fetching details:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4 gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                #{rank}
              </span>
            </div>
          </div>

          {product.image_url && (
            <div className="w-24 h-24 flex-shrink-0 rounded-md overflow-hidden border border-gray-200 bg-gray-50">
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-full object-cover"
              />
            </div>
          )}

          <div className="text-right">
            <div className="text-2xl font-bold text-blue-600">
              {(product.similarity_score * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-500">Similarity</div>
          </div>
        </div>

        <FeatureBreakdown scores={product.per_feature_scores} />

        <button
          onClick={handleShowDetails}
          className="mt-4 w-full py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm font-medium"
        >
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>

        {showDetails && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            {loading ? (
              <div className="text-center py-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              </div>
            ) : (
              <>
                {relatedProducts && relatedProducts.related_products.length > 0 && (
                  <div className="mb-4">
                    <h5 className="text-sm font-semibold text-gray-700 mb-2">
                      Related Products ({relatedProducts.total_related}):
                    </h5>
                    <div className="space-y-2">
                      {relatedProducts.related_products.slice(0, 5).map((rel) => (
                        <div
                          key={rel.product_id}
                          className="text-xs bg-gray-50 p-2 rounded flex items-center gap-2"
                        >
                          {rel.image_url && (
                            <img
                              src={rel.image_url}
                              alt={rel.title || rel.product_id}
                              className="w-10 h-10 rounded object-cover flex-shrink-0 border border-gray-200"
                            />
                          )}
                          <div className="flex-1 min-w-0">
                            <div className="flex justify-between gap-2">
                              <span className="font-medium truncate">
                                {rel.title || rel.product_id}
                              </span>
                              <span className="text-gray-500 ml-2 whitespace-nowrap">
                                {rel.relationship}
                              </span>
                            </div>
                            {(rel.material || rel.object_type) && (
                              <div className="mt-1 flex flex-wrap gap-1">
                                {rel.material && (
                                  <span className="px-1.5 py-0.5 bg-green-100 text-green-800 rounded">
                                    {rel.material}
                                  </span>
                                )}
                                {rel.object_type && (
                                  <span className="px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded">
                                    {rel.object_type}
                                  </span>
                                )}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {outlets && outlets.outlets.length > 0 && (
                  <div>
                    <h5 className="text-sm font-semibold text-gray-700 mb-2">
                      Available At ({outlets.total_outlets} shops):
                    </h5>
                    <div className="space-y-2">
                      {outlets.outlets.map((outlet) => (
                        <div
                          key={outlet.outlet_id}
                          className="text-xs bg-blue-50 p-2 rounded"
                        >
                          <div className="font-medium">{outlet.name}</div>
                          <div className="text-gray-600">{outlet.location}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {(!relatedProducts || relatedProducts.related_products.length === 0) &&
                 (!outlets || outlets.outlets.length === 0) && (
                  <p className="text-xs text-gray-500 text-center py-2">
                    No additional details available
                  </p>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;

