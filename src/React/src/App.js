// ReactForecastApp: Forecast UI for Flask-based API
import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = '/api/forecast';

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('All');

  const fetchImages = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: 'Failed to fetch images' });
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchImages();
  }, []);

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  const extractLabel = (url) => {
    const filename = url.split('/').pop().replace('.png', '').replace('.jpg', '');
    return filename.replace(/_/g, ' ');
  };

  const sortByNaturalNumber = (urls) => {
    return [...urls].sort((a, b) => {
      const nameA = a.split('/').pop().split('.')[0];
      const nameB = b.split('/').pop().split('.')[0];
      return nameA.localeCompare(nameB, undefined, { numeric: true, sensitivity: 'base' });
    });
  };

  const categories = response?.images ? Object.keys(response.images) : [];
  const filteredImages =
    selectedCategory === 'All'
      ? response?.images
      : { [selectedCategory]: response?.images[selectedCategory] };

  return (
    <div className="container">
      <h1>Forecast Image Gallery</h1>

      <button onClick={fetchImages} disabled={loading} style={{ marginBottom: '1rem' }}>
        {loading ? 'Generating...' : 'Regenerate Forecast'}
      </button>

      {categories.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="category">Filter by Category: </label>
          <select id="category" onChange={handleCategoryChange} value={selectedCategory}>
            <option value="All">All</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      )}

      {loading && (
        <div className="spinner-container">
          <div className="spinner"></div>
          <p>Loading images...</p>
        </div>
      )}

      {filteredImages && (
        <div className="results">
          {Object.entries(filteredImages).map(([model, urls]) => (
            <div key={model} style={{ marginBottom: '2rem' }}>
              <h2>{model}</h2>
              <div className="image-grid">
                {sortByNaturalNumber(urls).map((url, index) => (
                  <div key={index} style={{ textAlign: 'center' }}>
                    <img
                      src={url}
                      alt={`${model}-${index}`}
                      style={{ maxWidth: '100%', marginBottom: '0.5rem' }}
                    />
                    <p style={{ fontSize: '0.9rem', color: '#555' }}>{extractLabel(url)}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {response?.error && <p className="error">{response.error}</p>}
    </div>
  );
}

export default App;
