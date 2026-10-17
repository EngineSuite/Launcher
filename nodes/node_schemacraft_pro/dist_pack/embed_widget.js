/**
 * SchemaCraft Whitelabel Injection Widget
 * Automatically fetches and injects Google-compliant JSON-LD structured data into the document <head>.
 *
 * Usage:
 *   <script src="embed_widget.js" data-schema-src="https://example.com/schema.json" async></script>
 */
(function() {
  'use strict';
  const currentScript = document.currentScript || (function() {
    const scripts = document.getElementsByTagName('script');
    return scripts[scripts.length - 1];
  })();

  const schemaSrc = currentScript ? currentScript.getAttribute('data-schema-src') : null;
  const inlineConfig = currentScript ? currentScript.getAttribute('data-schema-config') : null;

  function injectSchema(jsonObj) {
    try {
      const script = document.createElement('script');
      script.type = 'application/ld+json';
      script.text = JSON.stringify(jsonObj);
      document.head.appendChild(script);
      if (window.console && window.console.log) {
        console.log('[SchemaCraft] Successfully injected Schema.org markup:', jsonObj['@type']);
      }
    } catch (e) {
      console.error('[SchemaCraft] Failed to inject structured data:', e);
    }
  }

  if (inlineConfig) {
    try {
      injectSchema(JSON.parse(inlineConfig));
    } catch (e) {
      console.error('[SchemaCraft] Invalid data-schema-config JSON:', e);
    }
  } else if (schemaSrc) {
    fetch(schemaSrc)
      .then(function(res) { return res.json(); })
      .then(function(data) { injectSchema(data); })
      .catch(function(err) { console.error('[SchemaCraft] Could not load schema from ' + schemaSrc, err); });
  }
})();
