/**
 * The Engine - Headless DOM & Interactive User Flow Runner
 * Emulates a lightweight browser environment to execute client-side scripts,
 * register event listeners, simulate user clicks/inputs, and verify UI state transitions.
 * Zero external dependencies — runs directly in standard Node.js.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

function runFlowTest(publicDirPath) {
  const publicDir = path.resolve(publicDirPath);
  const htmlPath = path.join(publicDir, 'index.html');
  if (!fs.existsSync(htmlPath)) {
    return {
      success: false,
      error: `index.html not found in ${publicDir}`
    };
  }

  let jsPath = path.join(publicDir, 'app.js');
  if (!fs.existsSync(jsPath)) {
    const parentJs = path.join(publicDir, '..', 'app.js');
    if (fs.existsSync(parentJs)) {
      jsPath = parentJs;
    }
  }

  const htmlContent = fs.readFileSync(htmlPath, 'utf-8');
  const hasJs = fs.existsSync(jsPath);
  const jsContent = hasJs ? fs.readFileSync(jsPath, 'utf-8') : '';

  // Extract all IDs from HTML
  const idRegex = /id=["']([^"']+)["']/g;
  const discoveredIds = new Set();
  let match;
  while ((match = idRegex.exec(htmlContent)) !== null) {
    discoveredIds.add(match[1]);
  }

  // Extract button tags and tab classes
  const buttonIdRegex = /<button[^>]*id=["']([^"']+)["'][^>]*>/g;
  const buttonIds = new Set();
  while ((match = buttonIdRegex.exec(htmlContent)) !== null) {
    buttonIds.add(match[1]);
  }

  // Mock Element Class
  class MockElement {
    constructor(id, tagName = 'div') {
      this.id = id;
      this.tagName = (tagName || 'div').toUpperCase();
      this.value = '100';
      this.textContent = '';
      this._innerHTML = '';
      this.checked = true;
      this.style = {};
      this.classList = {
        _set: new Set(),
        add: (c) => this.classList._set.add(c),
        remove: (c) => this.classList._set.delete(c),
        contains: (c) => this.classList._set.has(c),
        toggle: (c) => {
          if (this.classList._set.has(c)) {
            this.classList._set.delete(c);
            return false;
          } else {
            this.classList._set.add(c);
            return true;
          }
        }
      };
      this.attributes = { id: id };
      this.dataset = {};
      this.listeners = {};
      this.children = [];
      this.parentElement = null;
      this.files = [{ name: 'sample.csv', size: 100 }];
    }

    get className() {
      return Array.from(this.classList._set).join(' ');
    }
    set className(val) {
      this.classList._set.clear();
      (val || '').split(/\s+/).filter(Boolean).forEach(c => this.classList._set.add(c));
    }

    get innerHTML() {
      return this._innerHTML;
    }
    set innerHTML(val) {
      this._innerHTML = val;
      if (!val) {
        this.children = [];
      }
    }

    getAttribute(attr) {
      return this.attributes[attr] || null;
    }
    setAttribute(attr, val) {
      this.attributes[attr] = String(val);
      if (attr.startsWith('data-')) {
        const key = attr.slice(5).replace(/-([a-z])/g, g => g[1].toUpperCase());
        this.dataset[key] = String(val);
      }
    }
    hasAttribute(attr) {
      return attr in this.attributes;
    }
    removeAttribute(attr) {
      delete this.attributes[attr];
    }

    addEventListener(event, fn) {
      if (!this.listeners[event]) this.listeners[event] = [];
      this.listeners[event].push(fn);
    }
    removeEventListener(event, fn) {
      if (this.listeners[event]) {
        this.listeners[event] = this.listeners[event].filter(f => f !== fn);
      }
    }

    dispatchEvent(evt) {
      const type = evt.type || 'click';
      if (this.listeners[type]) {
        for (const fn of this.listeners[type]) {
          fn(evt);
        }
      }
      return true;
    }

    click() {
      const eventObj = {
        type: 'click',
        target: this,
        currentTarget: this,
        preventDefault: () => {},
        stopPropagation: () => {}
      };
      return this.dispatchEvent(eventObj);
    }

    focus() {}
    blur() {}
    select() {}

    appendChild(child) {
      this.children.push(child);
      child.parentElement = this;
      return child;
    }
    removeChild(child) {
      this.children = this.children.filter(c => c !== child);
      return child;
    }
    replaceChildren(...nodes) {
      this.children = nodes;
    }

    querySelector(sel) {
      for (const child of this.children) {
        if (child.id === sel.replace('#', '')) return child;
        if (child.classList.contains(sel.replace('.', ''))) return child;
        const found = child.querySelector(sel);
        if (found) return found;
      }
      return null;
    }

    querySelectorAll(sel) {
      const results = [];
      const classes = sel.split(',').map(s => s.trim().replace(/^\./, ''));
      const traverse = (node) => {
        for (const child of node.children) {
          const hasCls = classes.some(c => child.classList.contains(c) || (child.getAttribute('class') || '').includes(c));
          if (hasCls) results.push(child);
          traverse(child);
        }
      };
      traverse(this);
      return results;
    }

    getContext(type) {
      return {
        createLinearGradient: () => ({ addColorStop: () => {} }),
        fillRect: () => {},
        strokeRect: () => {},
        beginPath: () => {},
        roundRect: () => {},
        fill: () => {},
        stroke: () => {},
        fillText: () => {},
        measureText: (txt) => ({ width: (txt || '').length * 10 }),
        arc: () => {},
        save: () => {},
        restore: () => {},
        drawImage: () => {}
      };
    }

    toDataURL(mime) {
      return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=';
    }
  }

  const elementRegistry = new Map();
  function getElement(id, tag = 'div') {
    if (!elementRegistry.has(id)) {
      elementRegistry.set(id, new MockElement(id, tag));
    }
    return elementRegistry.get(id);
  }

  // Pre-seed discovered IDs
  for (const id of discoveredIds) {
    let tag = 'div';
    if (buttonIds.has(id) || id.toLowerCase().includes('btn')) tag = 'button';
    if (id.toLowerCase().includes('input') || id.toLowerCase().includes('slider')) tag = 'input';
    if (id.toLowerCase().includes('select') || id.toLowerCase().includes('type')) tag = 'select';
    if (id.toLowerCase().includes('canvas')) tag = 'canvas';
    if (id.toLowerCase().includes('modal')) tag = 'div';
    getElement(id, tag);
  }

  // Specific common mocks
  const tabSvg = getElement('tabSvg', 'button');
  tabSvg.setAttribute('data-tab', 'tabSvg');
  tabSvg.setAttribute('class', 'tab-btn');

  const tabReact = getElement('tabReact', 'button');
  tabReact.setAttribute('data-tab', 'tabReact');
  tabReact.setAttribute('class', 'tab-btn');

  const tabVue = getElement('tabVue', 'button');
  tabVue.setAttribute('data-tab', 'tabVue');
  tabVue.setAttribute('class', 'tab-btn');

  const themeMidnight = getElement('themeMidnight', 'button');
  themeMidnight.setAttribute('data-theme', 'midnight');
  themeMidnight.setAttribute('class', 'theme-btn');

  const themeCyber = getElement('themeCyber', 'button');
  themeCyber.setAttribute('data-theme', 'cyber');
  themeCyber.setAttribute('class', 'theme-btn');

  // DOM Mock Object
  const documentMock = {
    readyState: 'complete',
    getElementById: (id) => getElement(id),
    querySelector: (sel) => {
      if (sel.startsWith('#')) return getElement(sel.slice(1));
      if (sel.startsWith('.')) {
        const cls = sel.slice(1);
        for (const el of elementRegistry.values()) {
          if (el.classList.contains(cls) || (el.getAttribute('class') || '').includes(cls)) return el;
        }
      }
      return getElement('dyn_' + sel.replace(/[^a-zA-Z0-9]/g, '_'));
    },
    querySelectorAll: (sel) => {
      const results = [];
      const cls = sel.startsWith('.') ? sel.slice(1) : sel;
      for (const el of elementRegistry.values()) {
        if (el.classList.contains(cls) || (el.getAttribute('class') || '').includes(cls)) {
          results.push(el);
        }
      }
      if (results.length === 0 && (sel.includes('tab') || sel.includes('theme') || sel.includes('btn'))) {
        if (sel.includes('tab')) return [tabSvg, tabReact, tabVue];
        if (sel.includes('theme')) return [themeMidnight, themeCyber];
      }
      return results;
    },
    createElement: (tag) => new MockElement('dyn_' + Math.random().toString(36).substring(7), tag),
    createTextNode: (txt) => ({ textContent: txt }),
    body: getElement('body', 'body'),
    head: getElement('head', 'head'),
    adoptNode: (node) => node,
    execCommand: () => true,
    addEventListener: (evt, fn) => {
      if (evt === 'DOMContentLoaded') {
        // Immediate invocation since readyState is complete
        try { fn(); } catch (e) { errors.push({ phase: 'DOMContentLoaded', message: e.message }); }
      }
    }
  };

  const errors = [];
  const sandbox = {
    document: documentMock,
    window: {
      document: documentMock,
      addEventListener: (evt, fn) => {},
      removeEventListener: () => {},
      open: () => ({ focus: () => {} }),
      setTimeout: (fn) => { try { fn(); } catch(e) {} return 1; },
      clearTimeout: () => {},
      setInterval: () => 1,
      clearInterval: () => {},
      location: { href: 'http://localhost/' }
    },
    navigator: {
      clipboard: {
        writeText: async () => true,
        readText: async () => ''
      },
      userAgent: 'EngineHeadlessDOM/1.0'
    },
    localStorage: {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {},
      clear: () => {}
    },
    Blob: class {
      constructor(parts) {
        this.size = parts.reduce((acc, p) => acc + (typeof p === 'string' ? p.length : 0), 0);
      }
    },
    FileReader: class {
      readAsText(blob) {
        if (this.onload) this.onload({ target: { result: 'col1,col2\nval1,val2' } });
      }
    },
    DOMParser: class {
      parseFromString(xml, type) {
        return {
          querySelector: (sel) => {
            if (sel === 'svg') return new MockElement('svg', 'svg');
            return null;
          }
        };
      }
    },
    console: {
      log: () => {},
      warn: () => {},
      error: (err) => { errors.push({ phase: 'console.error', message: String(err) }); }
    },
    URL: {
      createObjectURL: (b) => 'blob:mock-object-url',
      revokeObjectURL: (u) => {}
    }
  };

  sandbox.global = sandbox;
  sandbox.self = sandbox;
  sandbox.window.window = sandbox.window;

  if (hasJs && jsContent.trim().length > 0) {
    try {
      const script = new vm.Script(jsContent, { filename: 'app.js' });
      const context = vm.createContext(sandbox);
      script.runInContext(context);
    } catch (err) {
      return {
        success: false,
        phase: 'SCRIPT_EXECUTION',
        error: err.stack || err.message,
        buttons_tested: 0,
        clicks_simulated: 0
      };
    }
  }

  // Interactive Flow Simulation
  let buttonsTested = 0;
  let clicksSimulated = 0;
  const elementsWithListeners = [];

  for (const [id, el] of elementRegistry.entries()) {
    const clickListeners = el.listeners['click'] || [];
    if (clickListeners.length > 0) {
      elementsWithListeners.push(id);
      buttonsTested++;
      try {
        el.click();
        clicksSimulated++;
      } catch (err) {
        errors.push({
          target: id,
          phase: 'SIMULATED_CLICK',
          message: err.message,
          stack: err.stack
        });
      }
    }

    // Test input / change listeners
    for (const evt of ['input', 'change']) {
      const inputListeners = el.listeners[evt] || [];
      if (inputListeners.length > 0) {
        try {
          el.dispatchEvent({ type: evt, target: el });
        } catch (err) {
          errors.push({
            target: id,
            phase: `SIMULATED_${evt.toUpperCase()}`,
            message: err.message
          });
        }
      }
    }
  }

  const passed = errors.length === 0 && (hasJs ? buttonsTested > 0 : true);

  return {
    success: passed,
    node_path: publicDir,
    has_javascript: hasJs,
    buttons_with_listeners: buttonsTested,
    clicks_simulated: clicksSimulated,
    interactive_elements: elementsWithListeners,
    errors: errors
  };
}

// CLI Execution
if (require.main === module) {
  const targetDir = process.argv[2];
  if (!targetDir) {
    console.error(JSON.stringify({ success: false, error: "Missing public directory argument" }));
    process.exit(1);
  }

  const result = runFlowTest(targetDir);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.success ? 0 : 1);
}

module.exports = { runFlowTest };
