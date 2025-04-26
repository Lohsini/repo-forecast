import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_FORECAST_URL = '/api/forecast';
const API_BUCKET_URL = '/api/bucket';

function App() {
  const [responseData, setResponseData] = useState({});
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [expandedGroups, setExpandedGroups] = useState({});
  const [dataSource, setDataSource] = useState('');
  const [highlighted, setHighlighted] = useState('');
  const groupRefs = useRef({});

  const fetchFromBucket = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_BUCKET_URL);
      const json = await res.json();
      setResponseData(json.data || {});
      setDataSource('GCS Bucket');
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const fetchFromNotebook = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_FORECAST_URL);
      const json = await res.json();
      setResponseData(json.data || {});
      setDataSource('Notebook (Live)');
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchFromBucket();
  }, []);

  const toggleExpand = (key) => {
    setExpandedGroups((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const handleDotClick = (key) => {
    const element = groupRefs.current[key];
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setHighlighted(key);
      setTimeout(() => setHighlighted(''), 2000);
    }
  };

  const getOrderedCategories = (categories) => {
    const priority = ['charts', 'Tensorflow_LSTM', 'Prophet', 'StatsModel'];
    return categories.sort((a, b) => {
      const ai = priority.indexOf(a);
      const bi = priority.indexOf(b);
      return (ai === -1 ? priority.length : ai) - (bi === -1 ? priority.length : bi);
    });
  };

  const getOrderedGroupKeys = (groupObj) => {
    const priority = [
      'issues_created_weekday_forecast',
      'issues_closed_weekday_forecast',
      'issues_closed_monthly_forecast',
      'created_issues_forecast',
      'closed_issues_forecast',
      'pull_requests_forecast',
      'monthly_commits_forecast',
      'monthly_branches_forecast',
      'monthly_contributors_forecast',
      'monthly_releases_forecast',
    ];
    const keys = Object.keys(groupObj);
    return keys
      .map((key) => {
        const cleanKey = key.replace('.png', '');
        const match = priority.find((p) => cleanKey.includes(p));
        const index = match ? priority.indexOf(match) : priority.length;
        return [key, index];
      })
      .sort((a, b) => a[1] - b[1]);
  };

  const categories = getOrderedCategories(Object.keys(responseData));
  const displayedData = selectedCategory === 'All' ? responseData : { [selectedCategory]: responseData[selectedCategory] };

  return (
    <div className="container">
      <h1>GitHub Repo Activity Forecast Dashboard</h1>
      {/* <p style={{ fontStyle: 'italic', color: '#888', marginBottom: '1rem' }}>
        Data Source: <strong>{dataSource}</strong>
      </p> */}
      {/* <button onClick={fetchFromNotebook} disabled={loading} style={{ marginBottom: '1rem' }}>
        {loading ? 'Generating...' : 'Regenerate Forecast'}
      </button> */}

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="category">Filter by Category: </label>
        <select id="category" onChange={(e) => setSelectedCategory(e.target.value)} value={selectedCategory}>
          <option value="All">All</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat === 'charts' ? 'Basic charts' : cat}
            </option>
          ))}
        </select>
      </div>

      {loading && (
        <div className="spinner-container">
          <div className="spinner"></div>
          <p>Loading images...</p>
        </div>
      )}

      {!loading &&
        Object.entries(displayedData).map(([model, groups]) => {
          const orderedGroupKeys = getOrderedGroupKeys(groups);
          return (
            <div key={model} className="model-section">
              
              <div className="group-content">
                <h2>{model === 'charts' ? 'Basic charts' : model}</h2>
                {orderedGroupKeys.map(([groupKey], i) => {
                  const { main, children } = groups[groupKey];
                  const refKey = `${model}-${groupKey}`;
                  return (
                    <div
                      key={groupKey}
                      className={`group-block ${highlighted === refKey ? 'highlighted' : ''}`}
                      ref={(el) => (groupRefs.current[refKey] = el)}
                    >
                      <h3>{`${i + 1}. ${groupKey.replace('.png', '').replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}`}</h3>
                      {main && (
                        <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                          <img src={main} alt={groupKey} style={{ maxWidth: '100%' }} />
                        </div>
                      )}
                      {Object.keys(children).length > 0 && (
                        <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                          <button onClick={() => toggleExpand(refKey)} style={{ fontSize: '0.8rem' }}>
                            {expandedGroups[refKey] ? 'Hide Details' : 'Show Details'}
                          </button>
                        </div>
                      )}
                      {expandedGroups[refKey] && (
                        <div className="image-grid">
                          {Object.entries(children).map(([suffix, url]) => (
                            <div key={suffix} style={{ textAlign: 'center' }}>
                              <img src={url} alt={suffix} style={{ maxWidth: '100%', marginBottom: '0.5rem' }} />
                              <p style={{ fontSize: '0.9rem', color: '#777' }}>{suffix.replace(/_/g, ' ')}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="progress-sidebar">
                {orderedGroupKeys.map(([groupKey], i) => (
                  <div
                    key={groupKey}
                    className={`progress-dot ${highlighted === `${model}-${groupKey}` ? 'active' : ''}`}
                    onClick={() => handleDotClick(`${model}-${groupKey}`)}
                  >
                    {i + 1}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default App;
