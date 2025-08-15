(async function(){
  const res = await fetch('{{ "/search.json" | relative_url }}');
  const data = await res.json();
  const idx = lunr(function () {
    this.ref('url'); this.field('title'); this.field('content');
    data.forEach(d => this.add(d));
  });
  const q = document.getElementById('q');
  const ul = document.getElementById('results');
  q.addEventListener('input', () => {
    const results = idx.search(q.value);
    ul.innerHTML = results.map(r => {
      const item = data.find(d => d.url === r.ref);
      return `<li><a href="${item.url}">${item.title}</a></li>`;
    }).join('');
  });
})();
