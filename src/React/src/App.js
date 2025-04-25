import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = '/api/forecast';

function App() {
  const [responseData, setResponseData] = useState({});
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [expandedGroups, setExpandedGroups] = useState({});
  const SHOW_REGENERATE_BUTTON = true;

  const fetchImages = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_URL);
      const json = await res.json();
      setResponseData(json.data || {});
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchImages();
  }, []);

  const toggleExpand = (key) => {
    setExpandedGroups((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
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
      'monthly_releases_forecast'
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
  const displayedData = selectedCategory === 'All'
    ? responseData
    : { [selectedCategory]: responseData[selectedCategory] };

  return (
    <div className="container">
      <h1>GitHub Repo Activity Forecast Dashboard</h1>

      {SHOW_REGENERATE_BUTTON && (
        <button onClick={fetchImages} disabled={loading} style={{ marginBottom: '1rem' }}>
          {loading ? 'Generating...' : 'Regenerate Forecast'}
        </button>
      )}

      {categories.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="category">Filter by Category: </label>
          <select
            id="category"
            onChange={(e) => setSelectedCategory(e.target.value)}
            value={selectedCategory}
          >
            <option value="All">All</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat === 'charts' ? 'Basic charts' : cat}
              </option>
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

      {!loading &&
        Object.entries(displayedData).map(([model, groups]) => (
          <div key={model} style={{ marginBottom: '2rem' }}>
            <h2>{model === 'charts' ? 'Basic charts' : model}</h2>
            {getOrderedGroupKeys(groups).map(([groupKey], i) => {
              const { main, children } = groups[groupKey];
              const isExpanded = expandedGroups[`${model}-${groupKey}`];
              return (
                <div key={groupKey} className="group-block">
                  <h3 style={{ marginBottom: '1rem' }}>
                    {`${i + 1}. ${groupKey
                      .replace('.png', '')
                      .replace(/_/g, ' ')
                      .replace(/\b\w/g, (c) => c.toUpperCase())}`}
                  </h3>
                  {main && (
                    <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                      <img src={main} alt={groupKey} style={{ maxWidth: '100%' }} />
                    </div>
                  )}
                  {Object.keys(children).length > 0 && (
                    <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                      <button
                        onClick={() => toggleExpand(`${model}-${groupKey}`)}
                        style={{ fontSize: '0.8rem' }}
                      >
                        {isExpanded ? 'Hide Details' : 'Show Details'}
                      </button>
                    </div>
                  )}
                  {isExpanded && (
                    <div className="image-grid">
                      {Object.entries(children).map(([suffix, url]) => (
                        <div key={suffix} style={{ textAlign: 'center' }}>
                          <img src={url} alt={suffix} style={{ maxWidth: '100%', marginBottom: '0.5rem' }} />
                          <p style={{ fontSize: '0.9rem', color: '#777' }}>
                            {suffix.replace(/_/g, ' ') || 'Unknown'}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ))}
    </div>
  );
}

export default App;
