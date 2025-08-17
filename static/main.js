const form = document.getElementById('shortenForm');
const urlInput = document.getElementById('urlInput');
const resultSection = document.getElementById('result');
const shortUrlLink = document.getElementById('shortUrl');
const infoBtn = document.getElementById('viewInfoBtn');
const infoBox = document.getElementById('infoBox');

let currentShortCode = '';

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  infoBox.textContent = '';
  resultSection.hidden = true;
  currentShortCode = '';

  const longUrl = urlInput.value.trim();
  if (!longUrl) return;

  try {
    const response = await fetch('/api/v1/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: longUrl })
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    currentShortCode = data.short_url;
    const shortUrlFull = `${window.location.origin}/${currentShortCode}`;
    shortUrlLink.textContent = shortUrlFull;
    shortUrlLink.href = shortUrlFull;

    resultSection.hidden = false;
  } catch (err) {
    infoBox.textContent = `Failed to generate short URL: ${err.message}`;
    infoBox.classList.add('error');
  }
});

shortUrlLink.addEventListener('click', (e) => {
  // Let the link behave normally (navigate)
});

infoBtn.addEventListener('click', async () => {
  infoBox.textContent = '';
  infoBox.classList.remove('error');

  if (!currentShortCode) {
    infoBox.textContent = 'No short URL generated yet.';
    return;
  }

  try {
    const response = await fetch(`/${currentShortCode}?info=true`);

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    infoBox.innerHTML = `Short URL: ${data.short_url}<br>` +
    `Original URL: <a href="${data.long_url}" target="_blank">${data.long_url}</a><br>` +
    `Created on: ${data.c_date}`;
 } catch (err) {
    infoBox.textContent = `Failed to fetch info: ${err.message}`;
    infoBox.classList.add('error');
  }
});
