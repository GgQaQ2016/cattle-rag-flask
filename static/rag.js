// JavaScript for RAG interaction page

function collectSelectedChunks() {
  return Array.from(document.querySelectorAll('input[name="chunks"]:checked')).map(cb => cb.value);
}

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('rag-form');
  const resultBox = document.getElementById('rag-results');
  if (!form) return;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    resultBox.textContent = 'Generating...';
    const query = form.querySelector('input[name="query"]').value;
    const chunks = collectSelectedChunks();

    try {
      const resp = await fetch('/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, chunks })
      });
      const data = await resp.json();
      resultBox.textContent = data.answer || data.error || 'No response';
    } catch (err) {
      resultBox.textContent = 'Request failed';
      console.error(err);
    }
  });
});
