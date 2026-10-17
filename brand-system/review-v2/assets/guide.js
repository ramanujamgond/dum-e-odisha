'use strict';
const notice = document.querySelector('[role="status"]');
let messageTimer;
document.querySelectorAll('[data-copy]').forEach(button => {
 button.addEventListener('click', async () => {
  try {
   await navigator.clipboard.writeText(button.dataset.copy);
   notice.textContent = `${button.dataset.copy} copied`;
  } catch { notice.textContent = `Color value: ${button.dataset.copy}`; }
  clearTimeout(messageTimer);
  messageTimer = setTimeout(() => { notice.textContent = ''; }, 4000);
 });
});
