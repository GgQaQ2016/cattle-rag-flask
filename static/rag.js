async function sendQuery() {
  const q = document.getElementById('query').value;
  const resp = await fetch('/rag/query', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: q})
  });
  const data = await resp.json();
  document.getElementById('answer').innerText = data.answer;
}
