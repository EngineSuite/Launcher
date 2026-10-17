# SchemaCraft Agency Pro Pack

Welcome to **SchemaCraft Agency Pro**. This package contains everything digital agencies, freelancers, and multi-location businesses need to automate Schema.org structured data and dominate Google Rich Snippets.

---

## 📦 What's Inside This Pack

1. **`bulk_generator.py`**: Standalone Python CLI utility to process 100+ business locations from a single spreadsheet into Google-compliant JSON-LD in seconds.
2. **`sample_locations.csv`**: Ready-to-use template spreadsheet with all Schema.org fields mapped out.
3. **`templates/`**: 25 pre-made, Google-validated JSON-LD templates for high-ticket industries (Dentists, Lawyers, Plumbers, Medical Clinics, Real Estate, Restaurants, SaaS, and more).
4. **`embed_widget.js`**: Whitelabel JavaScript snippet for client websites (Webflow, WordPress, Shopify, Custom).
5. **`LICENSE.txt`**: Unlimited commercial agency license.

---

## ⚡ Quickstart Guide

### 1. Generating Bulk Schemas from CSV
Place your location data in `sample_locations.csv` (or export your own CSV), then run:

```bash
# Output individual schema files for each location into ./output/
python bulk_generator.py sample_locations.csv --output-dir ./output/

# OR output a single master @graph feed containing all locations
python bulk_generator.py sample_locations.csv --combined-feed ./all_locations.json
```

### 2. Using the Whitelabel Embed Widget
Add this single line inside your client's website `<head>` tag:
```html
<script src="embed_widget.js" data-schema-src="https://yourdomain.com/schema.json" async></script>
```

### 3. Validating with Google
Test any generated output immediately at Google's official tool:
[https://search.google.com/test/rich-results](https://search.google.com/test/rich-results)

---
(c) 2026 SchemaCraft Pro. Commercial Agency License Granted.
