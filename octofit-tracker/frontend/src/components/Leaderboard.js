import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
      : 'http://localhost:8000/api/leaderboard/';
    
    console.log('Leaderboard - Fetching from API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard - Processed data:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger alert-custom" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div className="container">
          <h1>Leaderboard</h1>
          <p className="lead mb-0">See who's leading the fitness challenge</p>
        </div>
      </div>
      <div className="container mt-4">
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th style={{width: '100px'}}>Rank</th>
                <th>User</th>
                <th>Points</th>
                <th>Activities</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.length === 0 ? (
                <tr>
                  <td colSpan="4" className="text-center py-4">
                    <p className="text-muted mb-0">No leaderboard data found.</p>
                  </td>
                </tr>
              ) : (
                leaderboard.map((entry, index) => (
                  <tr key={entry.id || index}>
                    <td>
                      {index < 3 ? (
                        <span className={`badge ${index === 0 ? 'bg-warning' : index === 1 ? 'bg-secondary' : 'bg-danger'}`}>
                          #{index + 1}
                        </span>
                      ) : (
                        <span className="fw-bold">#{index + 1}</span>
                      )}
                    </td>
                    <td className="fw-semibold">{entry.user_name || entry.username || 'Unknown'}</td>
                    <td><span className="badge bg-success">{entry.total_points || entry.points || 0} pts</span></td>
                    <td>{entry.activity_count || entry.activities || 0}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
