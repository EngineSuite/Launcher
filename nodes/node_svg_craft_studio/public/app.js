// SVGCraft Studio Client Engine
document.addEventListener('DOMContentLoaded', () => {
  const svgInput = document.getElementById('svgInput');
  const codeOutput = document.getElementById('codeOutput');
  const optimizeBtn = document.getElementById('optimizeBtn');
  const loadSampleBtn = document.getElementById('loadSampleBtn');
  const copyCodeBtn = document.getElementById('copyCodeBtn');
  const downloadSvgBtn = document.getElementById('downloadSvgBtn');
  const statsBadge = document.getElementById('statsBadge');
  const previewContainer = document.getElementById('svgPreviewContainer');
  const tabBtns = document.querySelectorAll('.tab-btn');

  const optMetadata = document.getElementById('optMetadata');
  const optViewbox = document.getElementById('optViewbox');
  const optDecimals = document.getElementById('optDecimals');
  const optCurrentColor = document.getElementById('optCurrentColor');

  const checkoutModal = document.getElementById('checkoutModal');
  const upgradeBtn = document.getElementById('upgradeBtn');
  const proOrderBtn = document.getElementById('proOrderBtn');
  const closeModalBtn = document.getElementById('closeModalBtn');

  let currentTab = 'tabSvg';
  let currentOptimizedSvg = '';

  const sampleSvg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64.000000" height="64.000000" viewBox="0 0 64.000000 64.000000">
  <!-- Generator: Figma to Web Export 2026 -->
  <metadata><title>Sample Icon</title></metadata>
  <g id="layer1">
    <path fill="#38bdf8" d="M32.000000 4.000000 L56.000000 16.000000 L56.000000 40.000000 L32.000000 52.000000 L8.000000 40.000000 L8.000000 16.000000 Z" stroke="#0284c7" stroke-width="2.500000"/>
    <path fill="#ffffff" d="M32.000000 20.000000 L44.000000 26.000000 L44.000000 38.000000 L32.000000 44.000000 L20.000000 38.000000 L20.000000 26.000000 Z"/>
  </g>
</svg>`;

  loadSampleBtn.addEventListener('click', () => {
    svgInput.value = sampleSvg;
    runOptimization();
  });

  optimizeBtn.addEventListener('click', runOptimization);

  function runOptimization() {
    const raw = svgInput.value.trim();
    if (!raw) return;

    const originalSize = new Blob([raw]).size;
    let clean = raw;

    // 1. Strip comments and metadata
    if (optMetadata.checked) {
      clean = clean.replace(/<!--[\s\S]*?-->/g, '');
      clean = clean.replace(/<metadata[\s\S]*?<\/metadata>/gi, '');
      clean = clean.replace(/<title[\s\S]*?<\/title>/gi, '');
      clean = clean.replace(/<desc[\s\S]*?<\/desc>/gi, '');
      clean = clean.replace(/xmlns:xlink="[^"]*"/gi, '');
    }

    // 2. Enforce responsive viewBox & strip fixed width/height
    if (optViewbox.checked) {
      clean = clean.replace(/\s+width="[^"]*"/i, '');
      clean = clean.replace(/\s+height="[^"]*"/i, '');
    }

    // 3. Round path decimals
    if (optDecimals.checked) {
      clean = clean.replace(/\b(\d+\.\d{3,})\b/g, (match, p1) => {
        return parseFloat(p1).toFixed(2);
      });
    }

    // 4. Convert fills to currentColor if requested
    if (optCurrentColor.checked) {
      clean = clean.replace(/fill="#?[a-f0-9]+"/gi, 'fill="currentColor"');
    }

    // 5. Clean extra whitespace
    clean = clean.replace(/\s{2,}/g, ' ').replace(/>\s+</g, '><').trim();

    currentOptimizedSvg = clean;
    const cleanSize = new Blob([clean]).size;
    const savings = Math.max(0, Math.round(((originalSize - cleanSize) / originalSize) * 100));

    statsBadge.textContent = `${originalSize} B -> ${cleanSize} B (-${savings}% reduction)`;

    // Safe DOM injection using DOMParser
    try {
      const parser = new DOMParser();
      const doc = parser.parseFromString(clean, 'image/svg+xml');
      const importedSvg = doc.querySelector('svg');
      if (importedSvg) {
        previewContainer.replaceChildren(importedSvg);
      }
    } catch (e) {
      console.warn('DOM parser warning:', e);
    }

    updateOutputTab();
  }

  function updateOutputTab() {
    if (!currentOptimizedSvg) return;

    if (currentTab === 'tabSvg') {
      codeOutput.value = currentOptimizedSvg;
    } else if (currentTab === 'tabReact') {
      const jsx = `export function Icon(props) {\n  return (\n    ${currentOptimizedSvg.replace('xmlns="http://www.w3.org/2000/svg"', 'xmlns="http://www.w3.org/2000/svg" {...props}')}\n  );\n}`;
      codeOutput.value = jsx;
    } else if (currentTab === 'tabVue') {
      const vue = `<template>\n  ${currentOptimizedSvg.replace('<svg', '<svg v-bind="$attrs"')}\n</template>`;
      codeOutput.value = vue;
    }
  }

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTab = btn.getAttribute('data-tab');
      updateOutputTab();
    });
  });

  copyCodeBtn.addEventListener('click', () => {
    if (!codeOutput.value) return;
    navigator.clipboard.writeText(codeOutput.value);
    const orig = copyCodeBtn.textContent;
    copyCodeBtn.textContent = '✔ Copied!';
    setTimeout(() => { copyCodeBtn.textContent = orig; }, 1500);
  });

  downloadSvgBtn.addEventListener('click', () => {
    if (!currentOptimizedSvg) return;
    const blob = new Blob([currentOptimizedSvg], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'icon-optimized.svg';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Modal Controls
  [upgradeBtn, proOrderBtn].forEach(b => {
    if (b) b.addEventListener('click', () => checkoutModal.classList.add('open'));
  });
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => checkoutModal.classList.remove('open'));
  }
  checkoutModal.addEventListener('click', (e) => {
    if (e.target === checkoutModal) checkoutModal.classList.remove('open');
  });

  // Initial load
  loadSampleBtn.click();
});
