function checkPasswordStrengthUI(password) {
  const bar = document.getElementById('password-strength-bar');
  const text = document.getElementById('password-strength-text');
  if (!bar || !text) return;

  if (!password) {
    bar.style.width = '0%';
    text.innerText = '';
    return;
  }

  let score = 0;
  if (password.length >= 6) score += 30;
  if (password.length >= 10) score += 20;
  if (/[A-Z]/.test(password)) score += 25;
  if (/[0-9]/.test(password)) score += 25;

  bar.style.width = score + '%';

  if (score < 40) {
    bar.className = 'progress-bar bg-danger';
    text.innerText = 'Weak Password';
  } else if (score < 75) {
    bar.className = 'progress-bar bg-warning';
    text.innerText = 'Moderate Strength';
  } else {
    bar.className = 'progress-bar bg-success';
    text.innerText = 'Strong Password';
  }
}
