const API = {
  async get(endpoint) {
    const res = await fetch(endpoint, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    if (res.status === 401) {
      window.location.href = '/login';
      return { status: 'error', error: 'Session expired. Please log in again.' };
    }
    return res.json();
  },

  async post(endpoint, data) {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (res.status === 401) {
      window.location.href = '/login';
      return { status: 'error', error: 'Session expired. Please log in again.' };
    }
    return res.json();
  },

  async put(endpoint, data) {
    const res = await fetch(endpoint, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (res.status === 401) {
      window.location.href = '/login';
      return { status: 'error', error: 'Session expired. Please log in again.' };
    }
    return res.json();
  },

  async delete(endpoint) {
    const res = await fetch(endpoint, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    });
    if (res.status === 401) {
      window.location.href = '/login';
      return { status: 'error', error: 'Session expired. Please log in again.' };
    }
    return res.json();
  }
};

