// SchemaCraft Pro - Interactive JSON-LD Client Engine
(function() {
  const schemaTypeSelect = document.getElementById('schemaType');
  const dynamicFields = document.getElementById('dynamicFields');
  const jsonOutput = document.getElementById('jsonOutput');
  const copyBtn = document.getElementById('copyBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const validateBtn = document.getElementById('validateBtn');
  const upgradeBtn = document.getElementById('upgradeBtn');
  const buyProBtn = document.getElementById('buyProBtn');
  const proModal = document.getElementById('proModal');
  const closeModal = document.getElementById('closeModal');

  // Schema form definitions
  const schemaDefinitions = {
    LocalBusiness: [
      { id: 'name', label: 'Business Name', type: 'text', default: 'Apex Dental Care' },
      { id: 'businessType', label: 'Category', type: 'text', default: 'Dentist' },
      { id: 'url', label: 'Website URL', type: 'url', default: 'https://apexdentalcare.example.com' },
      { id: 'telephone', label: 'Phone Number', type: 'tel', default: '+1-555-019-2834' },
      { id: 'street', label: 'Street Address', type: 'text', default: '100 Main St, Suite 200' },
      { id: 'city', label: 'City', type: 'text', default: 'Austin' },
      { id: 'region', label: 'State / Region', type: 'text', default: 'TX' },
      { id: 'postalCode', label: 'Postal Code', type: 'text', default: '78701' },
      { id: 'country', label: 'Country Code (e.g. US)', type: 'text', default: 'US' },
      { id: 'priceRange', label: 'Price Range', type: 'text', default: '$$' }
    ],
    Organization: [
      { id: 'name', label: 'Organization Name', type: 'text', default: 'CloudFlow Technologies' },
      { id: 'url', label: 'Website URL', type: 'url', default: 'https://cloudflow.example.com' },
      { id: 'logo', label: 'Logo Image URL', type: 'url', default: 'https://cloudflow.example.com/logo.png' },
      { id: 'description', label: 'Description', type: 'textarea', default: 'Leading developer tools for autonomous cloud infrastructure.' },
      { id: 'sameAs', label: 'Social Media Profiles (comma-separated)', type: 'text', default: 'https://twitter.com/cloudflow, https://linkedin.com/company/cloudflow' }
    ],
    Product: [
      { id: 'name', label: 'Product Name', type: 'text', default: 'Autonomous Workflow Engine' },
      { id: 'description', label: 'Product Description', type: 'textarea', default: 'Self-correcting AI orchestrator for micro-SaaS deployment.' },
      { id: 'image', label: 'Product Image URL', type: 'url', default: 'https://example.com/product.png' },
      { id: 'brand', label: 'Brand Name', type: 'text', default: 'Engine Corp' },
      { id: 'price', label: 'Price (USD)', type: 'number', default: '19.00' },
      { id: 'currency', label: 'Currency', type: 'text', default: 'USD' },
      { id: 'ratingValue', label: 'Rating (1 to 5)', type: 'number', default: '4.9' },
      { id: 'reviewCount', label: 'Review Count', type: 'number', default: '128' }
    ],
    FAQPage: [
      { id: 'q1', label: 'Question 1', type: 'text', default: 'What is JSON-LD schema markup?' },
      { id: 'a1', label: 'Answer 1', type: 'textarea', default: 'JSON-LD is a structured data format recognized by Google to enable rich snippets in search results.' },
      { id: 'q2', label: 'Question 2', type: 'text', default: 'How long until rich snippets appear on Google?' },
      { id: 'a2', label: 'Answer 2', type: 'textarea', default: 'Typically Google recrawls pages within 3 to 14 days and displays snippets once verified.' }
    ],
    HowTo: [
      { id: 'name', label: 'Guide Title', type: 'text', default: 'How to Implement JSON-LD for Local SEO' },
      { id: 'description', label: 'Description', type: 'textarea', default: 'Step-by-step procedure to add structured data to your website.' },
      { id: 'step1', label: 'Step 1 Title & Description', type: 'textarea', default: 'Generate Schema: Use SchemaCraft Pro to create your business schema.' },
      { id: 'step2', label: 'Step 2 Title & Description', type: 'textarea', default: 'Embed Code: Insert the script into your website head section.' }
    ],
    Article: [
      { id: 'headline', label: 'Headline', type: 'text', default: 'Autonomous Revenue Streams: The 2026 Playbook' },
      { id: 'author', label: 'Author Name', type: 'text', default: 'The Engine Research Group' },
      { id: 'datePublished', label: 'Date Published (YYYY-MM-DD)', type: 'text', default: '2026-10-17' },
      { id: 'image', label: 'Featured Image URL', type: 'url', default: 'https://example.com/banner.png' },
      { id: 'publisher', label: 'Publisher Name', type: 'text', default: 'SchemaCraft Publications' }
    ],
    Event: [
      { id: 'name', label: 'Event Name', type: 'text', default: 'Global AI Founders Summit 2026' },
      { id: 'startDate', label: 'Start Date & Time (ISO 8601)', type: 'text', default: '2026-11-15T09:00:00Z' },
      { id: 'locationName', label: 'Venue Name', type: 'text', default: 'Moscone Center' },
      { id: 'locationAddress', label: 'Venue Address', type: 'text', default: '747 Howard St, San Francisco, CA' },
      { id: 'price', label: 'Ticket Price', type: 'number', default: '0.00' }
    ],
    JobPosting: [
      { id: 'title', label: 'Job Title', type: 'text', default: 'Senior Autonomous Systems Engineer' },
      { id: 'description', label: 'Job Description', type: 'textarea', default: 'Design and deploy self-correcting multi-agent architectures.' },
      { id: 'company', label: 'Hiring Company', type: 'text', default: 'The Engine Lab' },
      { id: 'location', label: 'Location (or Remote)', type: 'text', default: 'Remote' },
      { id: 'salary', label: 'Base Salary (Annual USD)', type: 'text', default: '180000' }
    ]
  };

  // Render input fields based on schema type
  function renderFields(type) {
    const fields = schemaDefinitions[type] || [];
    dynamicFields.innerHTML = '';
    fields.forEach(field => {
      const group = document.createElement('div');
      group.className = 'form-group';
      const label = document.createElement('label');
      label.setAttribute('for', field.id);
      label.textContent = field.label;

      let input;
      if (field.type === 'textarea') {
        input = document.createElement('textarea');
        input.className = 'form-textarea';
      } else {
        input = document.createElement('input');
        input.type = field.type;
        input.className = 'form-input';
      }
      input.id = field.id;
      input.value = field.default;
      input.addEventListener('input', generateSchema);

      group.appendChild(label);
      group.appendChild(input);
      dynamicFields.appendChild(group);
    });
    generateSchema();
  }

  // Generate JSON-LD payload
  function generateSchema() {
    const type = schemaTypeSelect.value;
    const values = {};
    const inputs = dynamicFields.querySelectorAll('.form-input, .form-textarea');
    inputs.forEach(input => { values[input.id] = input.value.trim(); });

    let schemaObject = {
      "@context": "https://schema.org"
    };

    if (type === 'LocalBusiness') {
      schemaObject["@type"] = values.businessType || "LocalBusiness";
      schemaObject["name"] = values.name;
      schemaObject["url"] = values.url;
      schemaObject["telephone"] = values.telephone;
      schemaObject["priceRange"] = values.priceRange;
      schemaObject["address"] = {
        "@type": "PostalAddress",
        "streetAddress": values.street,
        "addressLocality": values.city,
        "addressRegion": values.region,
        "postalCode": values.postalCode,
        "addressCountry": values.country
      };
    } else if (type === 'Organization') {
      schemaObject["@type"] = "Organization";
      schemaObject["name"] = values.name;
      schemaObject["url"] = values.url;
      schemaObject["logo"] = values.logo;
      schemaObject["description"] = values.description;
      if (values.sameAs) {
        schemaObject["sameAs"] = values.sameAs.split(',').map(s => s.trim()).filter(Boolean);
      }
    } else if (type === 'Product') {
      schemaObject["@type"] = "Product";
      schemaObject["name"] = values.name;
      schemaObject["description"] = values.description;
      schemaObject["image"] = values.image;
      schemaObject["brand"] = { "@type": "Brand", "name": values.brand };
      schemaObject["offers"] = {
        "@type": "Offer",
        "price": values.price,
        "priceCurrency": values.currency || "USD",
        "availability": "https://schema.org/InStock"
      };
      if (values.ratingValue) {
        schemaObject["aggregateRating"] = {
          "@type": "AggregateRating",
          "ratingValue": values.ratingValue,
          "reviewCount": values.reviewCount || "1"
        };
      }
    } else if (type === 'FAQPage') {
      schemaObject["@type"] = "FAQPage";
      schemaObject["mainEntity"] = [
        {
          "@type": "Question",
          "name": values.q1,
          "acceptedAnswer": { "@type": "Answer", "text": values.a1 }
        },
        {
          "@type": "Question",
          "name": values.q2,
          "acceptedAnswer": { "@type": "Answer", "text": values.a2 }
        }
      ];
    } else if (type === 'HowTo') {
      schemaObject["@type"] = "HowTo";
      schemaObject["name"] = values.name;
      schemaObject["description"] = values.description;
      schemaObject["step"] = [
        { "@type": "HowToStep", "text": values.step1 },
        { "@type": "HowToStep", "text": values.step2 }
      ];
    } else if (type === 'Article') {
      schemaObject["@type"] = "Article";
      schemaObject["headline"] = values.headline;
      schemaObject["author"] = { "@type": "Person", "name": values.author };
      schemaObject["datePublished"] = values.datePublished;
      schemaObject["image"] = values.image;
      schemaObject["publisher"] = { "@type": "Organization", "name": values.publisher };
    } else if (type === 'Event') {
      schemaObject["@type"] = "Event";
      schemaObject["name"] = values.name;
      schemaObject["startDate"] = values.startDate;
      schemaObject["location"] = {
        "@type": "Place",
        "name": values.locationName,
        "address": values.locationAddress
      };
      schemaObject["offers"] = {
        "@type": "Offer",
        "price": values.price,
        "priceCurrency": "USD"
      };
    } else if (type === 'JobPosting') {
      schemaObject["@type"] = "JobPosting";
      schemaObject["title"] = values.title;
      schemaObject["description"] = values.description;
      schemaObject["hiringOrganization"] = { "@type": "Organization", "name": values.company };
      schemaObject["jobLocation"] = { "@type": "Place", "address": values.location };
      schemaObject["baseSalary"] = {
        "@type": "MonetaryAmount",
        "currency": "USD",
        "value": { "@type": "QuantitativeValue", "value": values.salary, "unitText": "YEAR" }
      };
    }

    const scriptTag = `<script type="application/ld+json">\n${JSON.stringify(schemaObject, null, 2)}\n</script>`;
    jsonOutput.textContent = scriptTag;
  }

  // Copy to clipboard
  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(jsonOutput.textContent).then(() => {
      const orig = copyBtn.textContent;
      copyBtn.textContent = '✓ Copied!';
      copyBtn.style.color = '#10b981';
      setTimeout(() => { copyBtn.textContent = orig; copyBtn.style.color = ''; }, 2000);
    });
  });

  // Download .json
  downloadBtn.addEventListener('click', () => {
    const rawCode = jsonOutput.textContent;
    const blob = new Blob([rawCode], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `schema-${schemaTypeSelect.value.toLowerCase()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Mode Switching
  const modeSingle = document.getElementById('modeSingle');
  const modeBulk = document.getElementById('modeBulk');
  const singleSection = document.getElementById('singleSection');
  const bulkSection = document.getElementById('bulkSection');
  const loadSampleCsvBtn = document.getElementById('loadSampleCsvBtn');
  const uploadCsvBtn = document.getElementById('uploadCsvBtn');
  const csvFileInput = document.getElementById('csvFileInput');
  const bulkPreview = document.getElementById('bulkPreview');

  modeSingle.addEventListener('click', () => {
    modeSingle.classList.add('active');
    modeBulk.classList.remove('active');
    singleSection.style.display = 'block';
    bulkSection.style.display = 'none';
    generateSchema();
  });

  modeBulk.addEventListener('click', () => {
    modeBulk.classList.add('active');
    modeSingle.classList.remove('active');
    singleSection.style.display = 'none';
    bulkSection.style.display = 'block';
  });

  const sampleCsvData = [
    { name: "Apex Dental Care - Downtown", category: "Dentist", url: "https://apexdental.example.com/downtown", phone: "+1-512-555-0101", street: "100 Congress Ave Ste 400", city: "Austin", region: "TX", postal_code: "78701", rating: "4.9", review_count: "142" },
    { name: "Apex Dental Care - North Hills", category: "Dentist", url: "https://apexdental.example.com/north", phone: "+1-512-555-0102", street: "9400 Research Blvd", city: "Austin", region: "TX", postal_code: "78759", rating: "4.8", review_count: "98" },
    { name: "Apex Dental Care - South Congress", category: "Dentist", url: "https://apexdental.example.com/south", phone: "+1-512-555-0103", street: "1600 S Congress Ave", city: "Austin", region: "TX", postal_code: "78704", rating: "4.9", review_count: "215" },
    { name: "Horizon Legal Group", category: "Attorney", url: "https://horizonlegal.example.com", phone: "+1-312-555-0199", street: "200 W Madison St Ste 1200", city: "Chicago", region: "IL", postal_code: "60606", rating: "5.0", review_count: "64" },
    { name: "Blue Wave Plumbing Pros", category: "Plumber", url: "https://bluewaveplumbing.example.com", phone: "+1-602-555-0182", street: "4500 E Camelback Rd", city: "Phoenix", region: "AZ", postal_code: "85018", rating: "4.7", review_count: "310" },
    { name: "Prestige Real Estate Advisors", category: "RealEstateAgent", url: "https://prestigerealty.example.com", phone: "+1-305-555-0144", street: "1111 Brickell Ave", city: "Miami", region: "FL", postal_code: "33131", rating: "4.9", review_count: "89" },
    { name: "Summit Auto Repair Center", category: "AutoRepair", url: "https://summitautorepair.example.com", phone: "+1-303-555-0177", street: "1420 17th St", city: "Denver", region: "CO", postal_code: "80202", rating: "4.8", review_count: "175" },
    { name: "Green Leaf Veterinary Hospital", category: "VeterinaryCare", url: "https://greenleafvet.example.com", phone: "+1-206-555-0122", street: "2200 4th Ave", city: "Seattle", region: "WA", postal_code: "98121", rating: "4.9", review_count: "280" },
    { name: "Oasis Wellness Physical Therapy", category: "MedicalClinic", url: "https://oasiswellness.example.com", phone: "+1-415-555-0163", street: "500 Sutter St", city: "San Francisco", region: "CA", postal_code: "94102", rating: "4.9", review_count: "112" },
    { name: "Ironclad Roofing Specialists", category: "RoofingContractor", url: "https://ironcladroofs.example.com", phone: "+1-214-555-0155", street: "2001 Ross Ave", city: "Dallas", region: "TX", postal_code: "75201", rating: "4.8", review_count: "190" }
  ];

  function processAndDisplayLocations(locations) {
    let tableHtml = `<table class="bulk-table">
      <thead>
        <tr><th>Location Name</th><th>Type</th><th>City, State</th><th>Rating</th></tr>
      </thead>
      <tbody>`;
    
    const graphNodes = [];
    locations.forEach(loc => {
      tableHtml += `<tr>
        <td><strong>${loc.name}</strong></td>
        <td>${loc.category || 'LocalBusiness'}</td>
        <td>${loc.city || ''}, ${loc.region || ''}</td>
        <td>⭐ ${loc.rating || '4.9'} (${loc.review_count || '100'})</td>
      </tr>`;

      graphNodes.push({
        "@type": loc.category || "LocalBusiness",
        "name": loc.name,
        "url": loc.url,
        "telephone": loc.phone,
        "address": {
          "@type": "PostalAddress",
          "streetAddress": loc.street || "",
          "addressLocality": loc.city || "",
          "addressRegion": loc.region || "",
          "postalCode": loc.postal_code || "",
          "addressCountry": "US"
        },
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": loc.rating || "4.9",
          "reviewCount": loc.review_count || "100"
        }
      });
    });

    tableHtml += `</tbody></table>`;
    bulkPreview.innerHTML = tableHtml;

    // Output unified Schema.org @graph
    const fullGraph = {
      "@context": "https://schema.org",
      "@graph": graphNodes
    };
    jsonOutput.textContent = `<script type="application/ld+json">\n${JSON.stringify(fullGraph, null, 2)}\n</script>`;
  }

  loadSampleCsvBtn.addEventListener('click', () => {
    processAndDisplayLocations(sampleCsvData);
  });

  uploadCsvBtn.addEventListener('click', () => {
    csvFileInput.click();
  });

  csvFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(evt) {
      const text = evt.target.result;
      const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
      if (lines.length < 2) return;
      const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
      const parsed = [];
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        const row = {};
        headers.forEach((h, idx) => { row[h] = values[idx] || ''; });
        if (row.name) parsed.push(row);
      }
      processAndDisplayLocations(parsed);
    };
    reader.readAsText(file);
  });

  // Validation Test link to Google's official Rich Results Test
  validateBtn.addEventListener('click', () => {
    window.open('https://search.google.com/test/rich-results', '_blank');
  });

  // Pro Modal handlers
  function openModal() { proModal.classList.add('open'); }
  function closeModalFn() { proModal.classList.remove('open'); }

  upgradeBtn.addEventListener('click', openModal);
  buyProBtn.addEventListener('click', openModal);
  closeModal.addEventListener('click', closeModalFn);
  window.addEventListener('click', (e) => { if (e.target === proModal) closeModalFn(); });

  schemaTypeSelect.addEventListener('change', () => {
    renderFields(schemaTypeSelect.value);
  });

  // Initialize with default LocalBusiness
  renderFields('LocalBusiness');
})();
