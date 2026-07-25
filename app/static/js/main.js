document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle Handler
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  if (themeToggleBtn) {
    updateThemeIcon(savedTheme);
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
});

function updateThemeIcon(theme) {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  if (themeToggleBtn) {
    themeToggleBtn.innerHTML = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
}

function showAlert(message, type = 'info') {
  const alertContainer = document.getElementById('global-alert-container');
  if (!alertContainer) return;

  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show glass-card mb-3`;
  alertDiv.role = 'alert';
  alertDiv.innerHTML = `
    <span>${message}</span>
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  alertContainer.appendChild(alertDiv);

  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

// Format raw AI text (removes **, ###, markdown list items and renders clean HTML)
function formatAIContent(text) {
    if (!text) return '';
    if (typeof text !== 'string') return text;

    let formatted = text
        .replace(/\$(\d+(?:\.\d+)?)\s*(Billion|B\b)/gi, '₹$1 Crores')
        .replace(/\$(\d+(?:\.\d+)?)\s*(Million|M\b)/gi, '₹$1 Lakhs')
        .replace(/\$(\d[\d,]*)/g, '₹$1')
        .replace(/#{1,6}\s*(.*$)/gim, '<h6 class="fw-bold text-primary mt-2 mb-1">$1</h6>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^\s*[\-\*]\s+(.*$)/gim, '<div class="d-flex align-items-start gap-2 mb-1"><i class="fa-solid fa-angle-right text-primary fs-7 mt-1"></i><span>$1</span></div>')
        .replace(/\n/g, '<br/>');

    return formatted;
}


// Global Active Startup Context Management
function getActiveStartupId() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('startup_id')) {
        const id = urlParams.get('startup_id');
        localStorage.setItem('active_startup_id', id);
        return id;
    }
    return localStorage.getItem('active_startup_id') || null;
}

function setActiveStartupId(id) {
    if (id) {
        localStorage.setItem('active_startup_id', id);
    }
}

async function renderStartupSelectorHeader(containerId, onSelectCallback) {
    const container = document.getElementById(containerId);
    if (!container) return;

    try {
        const res = await API.get('/api/v1/ideas');
        if (res.status === 'success' && res.ideas.length > 0) {
            const currentActiveId = getActiveStartupId() || res.ideas[0].id;
            setActiveStartupId(currentActiveId);

            const activeStartup = res.ideas.find(i => String(i.id) === String(currentActiveId)) || res.ideas[0];

            container.innerHTML = `
                <div class="glass-card p-3 mb-4 border-primary d-flex flex-wrap justify-content-between align-items-center gap-3">
                    <div class="d-flex align-items-center gap-3">
                        <div class="stat-icon p-2 bg-primary-subtle rounded-circle text-primary"><i class="fa-solid fa-rocket fs-4"></i></div>
                        <div>
                            <div class="text-muted fs-7 fw-semibold">ACTIVE STARTUP PROJECT</div>
                            <h5 class="fw-bold text-gradient mb-0">${activeStartup.startup_name} <span class="badge bg-primary text-white fs-7 ms-2">${activeStartup.domain}</span></h5>
                        </div>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                        <label class="form-label mb-0 fs-7 fw-bold text-muted text-nowrap">Switch Project:</label>
                        <select id="header-startup-selector" class="form-select form-select-glass form-select-sm" style="min-width: 200px;">
                            ${res.ideas.map(i => `<option value="${i.id}" ${String(i.id) === String(currentActiveId) ? 'selected' : ''}>${i.startup_name} (${i.domain})</option>`).join('')}
                        </select>
                        <button class="btn btn-outline-danger btn-sm text-nowrap ms-1" title="Delete Project" onclick="deleteStartup('${activeStartup.id}')">
                            <i class="fa-solid fa-trash-can me-1"></i> Delete
                        </button>
                    </div>
                </div>
            `;

            document.getElementById('header-startup-selector').addEventListener('change', (e) => {
                const newId = e.target.value;
                setActiveStartupId(newId);
                if (onSelectCallback) {
                    onSelectCallback(newId);
                } else {
                    window.location.reload();
                }
            });
        }
    } catch (e) {
        console.error("Error loading active startup header selector:", e);
    }
}

async function deleteStartup(startupId) {
    if (!startupId) {
        startupId = getActiveStartupId();
    }
    if (!startupId) {
        showAlert('No active startup project selected to delete.', 'warning');
        return;
    }

    if (!confirm('Are you sure you want to delete this startup project? All associated analysis and reports will be permanently deleted.')) {
        return;
    }

    try {
        const res = await API.delete(`/api/v1/startup/${startupId}`);
        if (res.status === 'success') {
            showAlert(res.message || 'Startup deleted successfully.', 'success');
            localStorage.removeItem('active_startup_id');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } else {
            showAlert(res.error || 'Failed to delete startup project.', 'danger');
        }
    } catch (e) {
        console.error(e);
        showAlert('Error deleting startup project.', 'danger');
    }
}

function downloadStartupReport(startupId) {
    if (!startupId) {
        const activeId = getActiveStartupId();
        if (activeId) startupId = activeId;
    }

    if (startupId) {
        showAlert('Compiling & Downloading ReportLab PDF Report...', 'info');
        window.location.href = `/api/v1/download-report-by-startup/${startupId}`;
    } else {
        showAlert('No startup project selected. Generate an idea first!', 'warning');
    }
}

