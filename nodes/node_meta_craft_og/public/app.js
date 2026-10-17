// MetaCraft OG - High-Performance Canvas Card Engine
(function() {
  const canvas = document.getElementById('ogCanvas');
  const ctx = canvas.getContext('2d');

  const titleInput = document.getElementById('postTitle');
  const subInput = document.getElementById('postSub');
  const tagInput = document.getElementById('postTag');
  const authorInput = document.getElementById('postAuthor');
  const themeBtns = document.querySelectorAll('.theme-btn');
  const exportBtn = document.getElementById('exportPngBtn');

  const upgradeBtn = document.getElementById('upgradeBtn');
  const buyProBtn = document.getElementById('buyProBtn');
  const orderModal = document.getElementById('orderModal');
  const closeModal = document.getElementById('closeModal');
  const copyEmailBtn = document.getElementById('copyEmailBtn');

  let currentTheme = 'midnight';

  const themes = {
    midnight: { bg1: '#0f172a', bg2: '#1e1b4b', accent: '#38bdf8', tagBg: 'rgba(56, 189, 248, 0.2)', tagText: '#38bdf8' },
    cyber: { bg1: '#022c22', bg2: '#083344', accent: '#34d399', tagBg: 'rgba(52, 211, 153, 0.2)', tagText: '#34d399' },
    sunset: { bg1: '#450a0a', bg2: '#431407', accent: '#fb923c', tagBg: 'rgba(251, 146, 60, 0.2)', tagText: '#fb923c' },
    slate: { bg1: '#18181b', bg2: '#27272a', accent: '#a1a1aa', tagBg: 'rgba(161, 161, 170, 0.2)', tagText: '#f4f4f5' }
  };

  function drawCard() {
    const theme = themes[currentTheme];
    const width = 1200;
    const height = 630;

    // 1. Draw Background Gradient
    const grad = ctx.createLinearGradient(0, 0, width, height);
    grad.addColorStop(0, theme.bg1);
    grad.addColorStop(1, theme.bg2);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);

    // 2. Draw Decorative Border & Grid Accent
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 1;
    ctx.strokeRect(30, 30, width - 60, height - 60);

    // 3. Category Tag Badge
    const tag = (tagInput.value || 'ARTICLE').toUpperCase();
    ctx.font = 'bold 20px -apple-system, sans-serif';
    const tagMetrics = ctx.measureText(tag);
    const tagW = tagMetrics.width + 24;
    const tagH = 36;
    
    ctx.fillStyle = theme.tagBg;
    ctx.beginPath();
    ctx.roundRect(70, 70, tagW, tagH, 6);
    ctx.fill();

    ctx.fillStyle = theme.tagText;
    ctx.fillText(tag, 82, 95);

    // 4. Headline (Wrapped)
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 56px -apple-system, sans-serif';
    const titleText = titleInput.value || 'Enter your card title...';
    wrapText(ctx, titleText, 70, 200, 1060, 68);

    // 5. Subtitle
    ctx.fillStyle = '#94a3b8';
    ctx.font = '400 28px -apple-system, sans-serif';
    const subText = subInput.value || '';
    wrapText(ctx, subText, 70, 430, 1060, 38);

    // 6. Footer / Author Accent
    const author = authorInput.value || 'yourbrand.com';
    ctx.fillStyle = theme.accent;
    ctx.font = '600 24px -apple-system, sans-serif';
    ctx.fillText(author, 70, 560);
  }

  function wrapText(context, text, x, y, maxWidth, lineHeight) {
    const words = text.split(' ');
    let line = '';
    let currY = y;

    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = context.measureText(testLine);
      if (metrics.width > maxWidth && n > 0) {
        context.fillText(line, x, currY);
        line = words[n] + ' ';
        currY += lineHeight;
      } else {
        line = testLine;
      }
    }
    context.fillText(line, x, currY);
  }

  // Event Listeners for Live Updates
  [titleInput, subInput, tagInput, authorInput].forEach(inp => {
    inp.addEventListener('input', drawCard);
  });

  themeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      themeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTheme = btn.getAttribute('data-theme');
      drawCard();
    });
  });

  // Export PNG Action
  exportBtn.addEventListener('click', () => {
    const dataUrl = canvas.toDataURL('image/png');
    const a = document.createElement('a');
    a.href = dataUrl;
    const cleanTitle = (titleInput.value || 'social-card').toLowerCase().replace(/[^a-z0-9]/g, '-').slice(0, 30);
    a.download = `og-${cleanTitle}.png`;
    a.click();
  });

  // Modal Handlers
  function openModal() { orderModal.classList.add('open'); }
  function closeModalFn() { orderModal.classList.remove('open'); }

  upgradeBtn.addEventListener('click', openModal);
  buyProBtn.addEventListener('click', openModal);
  closeModal.addEventListener('click', closeModalFn);
  window.addEventListener('click', (e) => { if (e.target === orderModal) closeModalFn(); });

  // Copy Email Handler
  copyEmailBtn.addEventListener('click', () => {
    navigator.clipboard.writeText('businessbloke957@gmail.com').then(() => {
      const orig = copyEmailBtn.textContent;
      copyEmailBtn.textContent = '✓ Copied!';
      copyEmailBtn.style.background = '#10b981';
      copyEmailBtn.style.color = '#fff';
      setTimeout(() => {
        copyEmailBtn.textContent = orig;
        copyEmailBtn.style.background = '';
        copyEmailBtn.style.color = '';
      }, 2500);
    });
  });

  // Initial draw
  drawCard();
})();
