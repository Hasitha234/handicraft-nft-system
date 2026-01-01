import React, { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import SearchResults from './components/SearchResults';
import { searchByImage, healthCheck } from './services/api';

function App() {
  const [results, setResults] = useState(null);
  const [queryFeatures, setQueryFeatures] = useState(null);
  const [queryImage, setQueryImage] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  React.useEffect(() => {
    // Check API health on mount
    healthCheck()
      .then(() => setApiStatus('online'))
      .catch(() => setApiStatus('offline'));
  }, []);

  const handleImageSelect = async (file) => {
    setError(null);
    setIsProcessing(true);
    setResults(null);
    setQueryFeatures(null);
    
    // Create preview URL
    const imageUrl = URL.createObjectURL(file);
    setQueryImage(imageUrl);

    try {
      const data = await searchByImage(file);
      setResults(data.results);
      setQueryFeatures(data.query_features);
    } catch (err) {
      console.error('Search error:', err);
      setError(err.response?.data?.detail || 'Failed to search. Make sure the API server is running.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Handicraft Image Recognition System
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                AI-powered similarity search for Sri Lankan handicrafts
              </p>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${
                apiStatus === 'online' ? 'bg-green-500' : 
                apiStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
              }`}></div>
              <span className="text-xs text-gray-600">
                API {apiStatus === 'online' ? 'Online' : apiStatus === 'offline' ? 'Offline' : 'Checking...'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!results && !isProcessing && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Upload an image to find similar handicraft products
            </h2>
            <ImageUploader onImageSelect={handleImageSelect} isProcessing={isProcessing} />
          </div>
        )}

        {isProcessing && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Analyzing image and searching database...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">{error}</p>
            <p className="text-sm text-red-600 mt-2">
              Make sure the backend server is running: <code className="bg-red-100 px-2 py-1 rounded">python run.py</code>
            </p>
          </div>
        )}

        {results && (
          <>
            {queryImage && (
              <div className="mb-6">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Uploaded Image:</h3>
                <img
                  src={queryImage}
                  alt="Query"
                  className="max-w-xs rounded-lg shadow-md"
                />
              </div>
            )}
            <SearchResults
              results={results}
              queryFeatures={queryFeatures}
              queryImage={queryImage}
            />
            <div className="mt-8 text-center">
              <button
                onClick={() => {
                  setResults(null);
                  setQueryImage(null);
                  setQueryFeatures(null);
                }}
                className="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
              >
                Search Another Image
              </button>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            4th Year IT Undergraduate Project - Handicraft Image Recognition System
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;


