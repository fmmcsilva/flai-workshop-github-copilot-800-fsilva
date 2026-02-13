import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/workouts/`
      : 'http://localhost:8000/api/workouts/';
    
    console.log('Workouts - Fetching from API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts - Processed data:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts - Error fetching data:', error);
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
          <p className="mt-3">Loading workouts...</p>
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
          <h1>Workouts</h1>
          <p className="lead mb-0">Personalized workout suggestions and routines</p>
        </div>
      </div>
      <div className="container mt-4">
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th>Workout Name</th>
                <th>Description</th>
                <th>Duration</th>
                <th>Difficulty</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody>
              {workouts.length === 0 ? (
                <tr>
                  <td colSpan="5" className="text-center py-4">
                    <p className="text-muted mb-0">No workouts found.</p>
                  </td>
                </tr>
              ) : (
                workouts.map((workout) => (
                  <tr key={workout.id}>
                    <td className="fw-semibold">{workout.name || workout.workout_type}</td>
                    <td>{workout.description || <span className="text-muted">No description</span>}</td>
                    <td>{workout.duration ? `${workout.duration} min` : <span className="text-muted">N/A</span>}</td>
                    <td>
                      {workout.difficulty ? (
                        <span className={`badge ${
                          workout.difficulty.toLowerCase() === 'easy' ? 'bg-success' :
                          workout.difficulty.toLowerCase() === 'medium' ? 'bg-warning' :
                          workout.difficulty.toLowerCase() === 'hard' ? 'bg-danger' : 'bg-secondary'
                        }`}>
                          {workout.difficulty}
                        </span>
                      ) : (
                        <span className="text-muted">N/A</span>
                      )}
                    </td>
                    <td>{workout.category || <span className="text-muted">N/A</span>}</td>
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

export default Workouts;
