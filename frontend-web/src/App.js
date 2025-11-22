import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend);

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [currentUser, setCurrentUser] = useState('');
  const [token, setToken] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDatasetDetail = useCallback(async (datasetId, authToken) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets/${datasetId}/`, {
        headers: { Authorization: `Token ${authToken || token}` }
      });
      setCurrentDataset(response.data);
    } catch (err) {
      console.error('Error fetching dataset detail:', err);
    }
  }, [token]);

  const fetchDatasets = useCallback(async (authToken) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets/`, {
        headers: { Authorization: `Token ${authToken}` }
      });
      setDatasets(response.data);
      setLastUpdate(new Date());
      if (response.data.length > 0 && !currentDataset) {
        fetchDatasetDetail(response.data[0].id, authToken);
      }
    } catch (err) {
      console.error('Error fetching datasets:', err);
    }
  }, [currentDataset, fetchDatasetDetail]);

  useEffect(() => {
    // Check for saved token
    const savedToken = localStorage.getItem('token');
    const savedUsername = localStorage.getItem('username');
    if (savedToken && savedUsername) {
      setToken(savedToken);
      setCurrentUser(savedUsername);
      setIsAuthenticated(true);
      fetchDatasets(savedToken);
    }
  }, [fetchDatasets]);

  // Auto-refresh datasets every 5 seconds
  useEffect(() => {
    if (!isAuthenticated || !token || !autoRefresh) return;

    const interval = setInterval(() => {
      console.log('Auto-refreshing datasets...');
      fetchDatasets(token);
    }, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);
  }, [isAuthenticated, token, autoRefresh, fetchDatasets]);

  const handleAuth = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      const endpoint = authMode === 'login' ? 'auth/login/' : 'auth/register/';
      const payload = authMode === 'login' 
        ? { username, password }
        : { username, password, email };
      
      const response = await axios.post(`${API_BASE_URL}/${endpoint}`, payload);
      
      setToken(response.data.token);
      setCurrentUser(response.data.username);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('username', response.data.username);
      setIsAuthenticated(true);
      setSuccess(authMode === 'login' ? 'Login successful!' : 'Registration successful!');
      fetchDatasets(response.data.token);
    } catch (err) {
      setError(err.response?.data?.error || 'Authentication failed');
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken('');
    setCurrentUser('');
    setCurrentDataset(null);
    setDatasets([]);
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post(`${API_BASE_URL}/datasets/upload_csv/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${token}`
        }
      });

      setCurrentDataset(response.data);
      setSuccess('File uploaded successfully!');
      fetchDatasets(token);
      setSelectedFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!currentDataset) return;

    try {
      const response = await axios.get(
        `${API_BASE_URL}/datasets/${currentDataset.id}/generate_report/`,
        {
          headers: { Authorization: `Token ${token}` },
          responseType: 'blob'
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${currentDataset.name}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setSuccess('Report downloaded successfully!');
    } catch (err) {
      setError('Failed to download report');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="App">
        <div className="container">
          <div className="header">
            <h1>🧪 Chemical Equipment Visualizer</h1>
            <p>Hybrid Web + Desktop Application</p>
          </div>

          <div className="auth-section">
            <h2>{authMode === 'login' ? 'Login' : 'Register'}</h2>
            
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
            
            <form onSubmit={handleAuth} className="auth-form">
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              {authMode === 'register' && (
                <input
                  type="email"
                  placeholder="Email (optional)"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              )}
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="submit">
                {authMode === 'login' ? 'Login' : 'Register'}
              </button>
            </form>
            
            <div className="auth-toggle">
              {authMode === 'login' ? (
                <p>
                  Don't have an account?{' '}
                  <button onClick={() => setAuthMode('register')}>Register</button>
                </p>
              ) : (
                <p>
                  Already have an account?{' '}
                  <button onClick={() => setAuthMode('login')}>Login</button>
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const getEquipmentTypeChartData = () => {
    if (!currentDataset) return null;

    const labels = Object.keys(currentDataset.equipment_types);
    const data = Object.values(currentDataset.equipment_types);

    return {
      labels,
      datasets: [{
        label: 'Equipment Count',
        data,
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
      }]
    };
  };

  const getParametersChartData = () => {
    if (!currentDataset || !currentDataset.equipment_items) return null;

    const labels = currentDataset.equipment_items.map(item => item.equipment_name);
    
    return {
      labels,
      datasets: [
        {
          label: 'Flowrate',
          data: currentDataset.equipment_items.map(item => item.flowrate),
          borderColor: 'rgb(102, 126, 234)',
          backgroundColor: 'rgba(102, 126, 234, 0.5)',
        },
        {
          label: 'Pressure',
          data: currentDataset.equipment_items.map(item => item.pressure),
          borderColor: 'rgb(118, 75, 162)',
          backgroundColor: 'rgba(118, 75, 162, 0.5)',
        },
        {
          label: 'Temperature',
          data: currentDataset.equipment_items.map(item => item.temperature),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
        }
      ]
    };
  };

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <h1>🧪 Chemical Equipment Visualizer</h1>
          <p>Hybrid Web + Desktop Application</p>
        </div>

        <div className="user-info">
          <span>Welcome, {currentUser}!</span>
          <span style={{ marginLeft: '20px', fontSize: '14px', color: '#666' }}>
            {autoRefresh ? '🔄' : '⏸️'} 
            {lastUpdate ? `Updated: ${lastUpdate.toLocaleTimeString()}` : 'Loading...'}
          </span>
          <button 
            onClick={() => setAutoRefresh(!autoRefresh)} 
            className="refresh-btn"
            style={{ 
              marginLeft: '10px',
              backgroundColor: autoRefresh ? '#43e97b' : '#fa709a',
              color: autoRefresh ? 'black' : 'white'
            }}
          >
            {autoRefresh ? '🔄 Auto-Refresh: ON' : '⏸️ Auto-Refresh: OFF'}
          </button>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>

        <div className="upload-section">
          <h2>📤 Upload CSV Data</h2>
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}
          
          <div className="file-input-wrapper">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="file-input"
            />
          </div>
          
          <button onClick={handleUpload} disabled={!selectedFile || loading} className="upload-btn">
            {loading ? 'Uploading...' : 'Upload & Analyze'}
          </button>
          
          {currentDataset && (
            <button onClick={handleDownloadReport} className="download-btn">
              📄 Download PDF Report
            </button>
          )}
        </div>

        {currentDataset && (
          <>
            <div className="summary-section">
              <h2>📊 Summary Statistics</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Total Equipment</h3>
                  <p>{currentDataset.total_count}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Flowrate</h3>
                  <p>{currentDataset.avg_flowrate.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Pressure</h3>
                  <p>{currentDataset.avg_pressure.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Temperature</h3>
                  <p>{currentDataset.avg_temperature.toFixed(2)}</p>
                </div>
              </div>
            </div>

            <div className="charts-section">
              <h2>📈 Visualizations</h2>
              <div className="charts-grid">
                <div className="chart-container">
                  <h3>Equipment Type Distribution</h3>
                  {getEquipmentTypeChartData() && <Pie data={getEquipmentTypeChartData()} />}
                </div>
                <div className="chart-container">
                  <h3>Equipment Type Count</h3>
                  {getEquipmentTypeChartData() && <Bar data={getEquipmentTypeChartData()} />}
                </div>
              </div>
              
              {currentDataset.equipment_items && currentDataset.equipment_items.length > 0 && (
                <div style={{ marginTop: '30px' }}>
                  <h3>Parameters Comparison</h3>
                  <div style={{ height: '400px', background: '#f9f9f9', padding: '20px', borderRadius: '10px' }}>
                    <Line 
                      data={getParametersChartData()} 
                      options={{ 
                        responsive: true, 
                        maintainAspectRatio: false,
                        plugins: {
                          legend: { position: 'top' }
                        }
                      }} 
                    />
                  </div>
                </div>
              )}
            </div>

            <div className="data-table-section">
              <h2>📋 Equipment Data</h2>
              {currentDataset.equipment_items && currentDataset.equipment_items.length > 0 ? (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Equipment Name</th>
                      <th>Type</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentDataset.equipment_items.map((item, index) => (
                      <tr key={index}>
                        <td>{item.equipment_name}</td>
                        <td>{item.equipment_type}</td>
                        <td>{item.flowrate}</td>
                        <td>{item.pressure}</td>
                        <td>{item.temperature}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className="no-data">No equipment data available</p>
              )}
            </div>
          </>
        )}

        {datasets.length > 0 && (
          <div className="history-section">
            <h2>📜 Upload History (Last 5 - Your Uploads Only)</h2>
            <div className="history-list">
              {datasets.map((dataset) => (
                <div
                  key={dataset.id}
                  className={`history-item ${currentDataset?.id === dataset.id ? 'active' : ''}`}
                  onClick={() => fetchDatasetDetail(dataset.id)}
                >
                  <h3>{dataset.name}</h3>
                  <p>Uploaded: {new Date(dataset.uploaded_at).toLocaleString()}</p>
                  <p>Count: {dataset.total_count} | Avg Flowrate: {dataset.avg_flowrate.toFixed(2)}</p>
                  <p style={{ fontSize: '12px', color: '#888' }}>By: {dataset.uploaded_by_username || 'You'}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {!currentDataset && !loading && (
          <div className="no-data">
            <p>Upload a CSV file to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
