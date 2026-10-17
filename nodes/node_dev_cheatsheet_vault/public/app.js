// CloudZero Interactive Engine
(function() {
  const mauSlider = document.getElementById('mauSlider');
  const dbSlider = document.getElementById('dbSlider');
  const bwSlider = document.getElementById('bandwidthSlider');
  const mauVal = document.getElementById('mauVal');
  const dbVal = document.getElementById('dbVal');
  const bwVal = document.getElementById('bwVal');
  const awsCost = document.getElementById('awsCost');
  const annualSavings = document.getElementById('annualSavings');
  const matrixGrid = document.getElementById('matrixGrid');
  const tabBtns = document.querySelectorAll('.tab-btn');
  const upgradeBtn = document.getElementById('upgradeBtn');
  const buyNowBtn = document.getElementById('buyNowBtn');
  const checkoutModal = document.getElementById('checkoutModal');
  const closeModal = document.getElementById('closeModal');

  const services = [
    { name: "Cloudflare Pages", cat: "hosting", tier: "$0 Forever", desc: "Unlimited static site hosting & edge redirects.", limits: "Unlimited Bandwidth, 100 Custom Domains" },
    { name: "Oracle Always-Free", cat: "compute", tier: "$0 Forever", desc: "Full Ampere ARM virtual machines.", limits: "4 OCPUs, 24 GB RAM, 200 GB NVMe Storage" },
    { name: "Supabase Database", cat: "db", tier: "$0 Forever", desc: "Hosted PostgreSQL with real-time API.", limits: "500 MB DB, 50k Monthly Active Users Auth" },
    { name: "Cloudflare R2", cat: "hosting", tier: "$0 Forever", desc: "S3-compatible object storage with ZERO egress fees.", limits: "10 GB Storage / Month, Zero Egress Charges" },
    { name: "Upstash Redis", cat: "db", tier: "$0 Forever", desc: "Serverless Redis for caching & rate-limiting.", limits: "10,000 Commands / Day, Rest API" },
    { name: "Resend", cat: "compute", tier: "$0 Forever", desc: "Developer-first transactional email API.", limits: "3,000 Emails / Month, 100 Emails / Day" },
    { name: "Neon Serverless Postgres", cat: "db", tier: "$0 Forever", desc: "Branchable serverless PostgreSQL with auto-suspend.", limits: "0.5 GB Storage, Instant DB Branching" },
    { name: "Clerk Auth", cat: "auth", tier: "$0 Forever", desc: "Drop-in authentication & user management.", limits: "10,000 Monthly Active Users Free" },
    { name: "GitHub Actions", cat: "compute", tier: "$0 Forever", desc: "Automated CI/CD pipelines and cron runners.", limits: "2,000 Build Minutes / Month Free" }
  ];

  function renderMatrix(filterCat = 'all') {
    matrixGrid.innerHTML = '';
    const filtered = filterCat === 'all' ? services : services.filter(s => s.cat === filterCat);
    filtered.forEach(s => {
      const card = document.createElement('div');
      card.className = 'service-card';
      card.innerHTML = `
        <div>
          <div class="service-header">
            <span class="service-name">${s.name}</span>
            <span class="service-tier">${s.tier}</span>
          </div>
          <p class="service-desc">${s.desc}</p>
        </div>
        <div class="service-limits">${s.limits}</div>
      `;
      matrixGrid.appendChild(card);
    });
  }

  function updateSavings() {
    const mau = parseInt(mauSlider.value, 10);
    const db = parseInt(dbSlider.value, 10);
    const bw = parseInt(bwSlider.value, 10);

    mauVal.textContent = mau.toLocaleString();
    dbVal.textContent = db + ' GB';
    bwVal.textContent = bw + ' GB';

    // Estimate AWS bill
    const awsMonthly = Math.round(35 + (mau * 0.005) + (db * 1.5) + (bw * 0.09));
    const annual = awsMonthly * 12;

    awsCost.textContent = '$' + awsMonthly.toLocaleString() + '.00/mo';
    annualSavings.textContent = '$' + annual.toLocaleString() + '.00/year';
  }

  mauSlider.addEventListener('input', updateSavings);
  dbSlider.addEventListener('input', updateSavings);
  bwSlider.addEventListener('input', updateSavings);

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderMatrix(btn.getAttribute('data-cat'));
    });
  });

  function openCheckout() { checkoutModal.classList.add('open'); }
  function closeCheckout() { checkoutModal.classList.remove('open'); }

  upgradeBtn.addEventListener('click', openCheckout);
  buyNowBtn.addEventListener('click', openCheckout);
  closeModal.addEventListener('click', closeCheckout);
  window.addEventListener('click', (e) => { if (e.target === checkoutModal) closeCheckout(); });

  updateSavings();
  renderMatrix();
})();
