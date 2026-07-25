document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  if (!chatForm || !chatInput || !chatMessages) return;

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;

    // Append user message
    appendChatMessage('user', msg);
    chatInput.value = '';

    // Typing indicator
    const typingId = appendTypingIndicator();

    try {
      const res = await API.post('/api/v1/mentor-chat', { message: msg });
      removeTypingIndicator(typingId);
      if (res.status === 'success') {
        appendChatMessage('assistant', res.reply);
      } else {
        appendChatMessage('assistant', 'Sorry, I encountered an issue processing your request. Please try again.');
      }
    } catch (err) {
      removeTypingIndicator(typingId);
      appendChatMessage('assistant', 'Network error. Please check your connection.');
    }
  });
});

function appendChatMessage(role, text) {
  const container = document.getElementById('chat-messages');
  const msgDiv = document.createElement('div');
  msgDiv.className = `d-flex mb-3 ${role === 'user' ? 'justify-content-end' : 'justify-content-start'}`;

  const innerDiv = document.createElement('div');
  innerDiv.className = `glass-card p-3 rounded-4 ${role === 'user' ? 'bg-primary text-white' : ''}`;
  innerDiv.style.maxWidth = '75%';
  innerDiv.innerHTML = `
    <div class="fw-bold mb-1 fs-7">${role === 'user' ? 'You' : '🤖 AI Startup Mentor'}</div>
    <div style="white-space: pre-line;">${text}</div>
  `;

  msgDiv.appendChild(innerDiv);
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function appendTypingIndicator() {
  const container = document.getElementById('chat-messages');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.id = id;
  div.className = 'd-flex mb-3 justify-content-start';
  div.innerHTML = `
    <div class="glass-card p-3 rounded-4">
      <span class="loading-spinner"></span> <em>AI Mentor is typing...</em>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}
