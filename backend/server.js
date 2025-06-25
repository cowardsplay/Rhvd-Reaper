// Import required libraries
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

// Initialize the Express app
const app = express();

// Enabled cors and json request parsing
app.use(cors());
app.use(express.json());

// Base URL for horitzon api (set in .env)
const BASE_URL = process.env.HORIZON_API_BASE;

// Server static frontend files from the frontend directory
app.use(express.static(path.join(__dirname, '../frontend')));

// Route: serve index.html at the root path "/"
app.get('/', (req, res) => { 
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Function to generate auth header dynamically
function createAuthHeader(apiUser, apiPass) {
  return {
    headers: {
      Authorization: `Basic ${Buffer.from(`${apiUser}:${apiPass}`).toString('base64')}`,
      'Content-Type': 'application/json',
      Accept: 'application/json'
    }
  };
}

// api endpoint: put an Active Directory user on forensic hold
app.post('/api/hold-user', async (req, res) => {
  const { userSid, apiUser, apiPass } = req.body;
  if (!apiUser || !apiPass) return res.status(401).json({ error: 'Missing credentials' });
  if (!userSid) return res.status(400).json({ error: 'Missing user SID' });

  try {
    const auth = createAuthHeader(apiUser, apiPass);
    const response = await axios.post(`${BASE_URL}/external/v1/ad-users-or-groups/action/hold`, {
      securityIdentifiers: [userSid]
    }, auth);
    res.json(response.data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: err.message });
  }
});
// api endpoint: archive a virutal machine by VM ID
app.post('/api/archive-vm', async (req, res) => {
  const { vmId, apiUser, apiPass } = req.body;
  if (!apiUser || !apiPass) return res.status(401).json({ error: 'Missing credentials' });
  if (!vmId) return res.status(400).json({ error: 'Missing VM ID' });

  try {
    const auth = createAuthHeader(apiUser, apiPass);
    const response = await axios.post(`${BASE_URL}/inventory/v1/machines/action/archive`, {
      ids: [vmId]
    }, auth);
    res.json(response.data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: err.message });
  }
});
// api endpoint: release a user from forensic hold
app.post('/api/release-hold', async (req, res) => {
  const { userSid, apiUser, apiPass } = req.body;
  if (!apiUser || !apiPass) return res.status(401).json({ error: 'Missing credentials' });
  if (!userSid) return res.status(400).json({ error: 'Missing user SID' });

  try {
    const auth = createAuthHeader(apiUser, apiPass);
    const response = await axios.post(`${BASE_URL}/external/v1/ad-users-or-groups/action/release-hold`, {
      securityIdentifiers: [userSid]
    }, auth);
    res.json(response.data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: err.message });
  }
});
// api endpoint: list all currently held users
app.get('/api/held-users', async (req, res) => {
  const authHeader = req.headers['authorization'];
  if (!authHeader) return res.status(401).json({ error: 'Missing Authorization header' });

  try {
    const response = await axios.get(`${BASE_URL}/external/v1/ad-users-or-groups/held-users-or-groups`, {
      headers: {
        Authorization: authHeader,
        Accept: 'application/json'
      }
    });
    res.json(response.data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: err.message });
  }
});
// start the backend server on port from .env or 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`backend running on http://localhost:${PORT}`);
    });
