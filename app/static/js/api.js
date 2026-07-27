const API = {
  async get(endpoint) {
    try {
      const res = await fetch(endpoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      if (res.status === 401 && !window.location.pathname.includes('/login')) {
        window.location.href = '/login';
        return { status: 'error', error: 'Session expired. Please log in again.' };
      }
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        return { status: 'error', error: 'Server error or invalid response format.' };
      }
    } catch (err) {
      console.error('API GET Error:', err);
      return { status: 'error', error: err.message || 'Network error or server unreachable.' };
    }
  },

  async post(endpoint, data) {
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.status === 401 && !endpoint.includes('/login') && !endpoint.includes('/register')) {
        window.location.href = '/login';
        return { status: 'error', error: 'Session expired. Please log in again.' };
      }
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        return { status: 'error', error: 'Server error or invalid response format.' };
      }
    } catch (err) {
      console.error('API POST Error:', err);
      return { status: 'error', error: err.message || 'Network error or server unreachable.' };
    }
  },

  async put(endpoint, data) {
    try {
      const res = await fetch(endpoint, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.status === 401 && !window.location.pathname.includes('/login')) {
        window.location.href = '/login';
        return { status: 'error', error: 'Session expired. Please log in again.' };
      }
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        return { status: 'error', error: 'Server error or invalid response format.' };
      }
    } catch (err) {
      console.error('API PUT Error:', err);
      return { status: 'error', error: err.message || 'Network error or server unreachable.' };
    }
  },

  async delete(endpoint) {
    try {
      const res = await fetch(endpoint, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
      });
      if (res.status === 401 && !window.location.pathname.includes('/login')) {
        window.location.href = '/login';
        return { status: 'error', error: 'Session expired. Please log in again.' };
      }
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        return { status: 'error', error: 'Server error or invalid response format.' };
      }
    } catch (err) {
      console.error('API DELETE Error:', err);
      return { status: 'error', error: err.message || 'Network error or server unreachable.' };
    }
  }
};

