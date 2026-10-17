"""
The Engine - Global Configuration & Guardrails
Enforces zero-upfront-cost rules, HITL constraints, and agent parameters.
"""

from pathlib import Path
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

def get_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "the_engine" / "storage"
NODES_DIR = BASE_DIR / "nodes"
REPORTS_DIR = STORAGE_DIR / "reports"
LEDGER_PATH = STORAGE_DIR / "ledger.json"
STATE_PATH = STORAGE_DIR / "state.json"

# Financial Guardrails ($0 Upfront Cost Paradigm)
STRICT_ZERO_COST = True
INITIAL_CAPITAL = 0.00  # Strictly $0 upfront
MAX_TRANSACTION_COST_WITHOUT_APPROVAL = 0.00  # Forbidden to spend any money unless earned first
MAX_DAILY_OPERATIONAL_LOSS = 0.00  # Zero loss allowed

# Autonomy & Self-Correction Guardrails
MAX_SELF_CORRECTION_ATTEMPTS = 5  # Ping HITL on 5th consecutive failure
OPTIMIZATION_WINDOW_HOURS = 48  # Review performance after 48 hours
FAIL_SAFE_CONSECUTIVE_DAYS = 3  # Archive node after 3 days of negative/zero traction
BUDGET_SCALE_PERCENTAGE = 0.20  # Scale budget by 20% if profitable

# Supported Free-Tier Hosting Targets
FREE_HOSTING_PLATFORMS = [
    "GitHub Pages (Free static hosting)",
    "Cloudflare Pages & Workers (Free tier: 100k req/day)",
    "Vercel (Free Hobby tier)",
    "Render (Free web service tier)",
    "Netlify (Free starter tier)"
]

# Supported Zero-Upfront Monetization Gateways
FREE_PAYMENT_GATEWAYS = [
    "Gumroad (Zero upfront, pay-as-you-earn fee)",
    "Lemon Squeezy (Zero upfront, MoR model)",
    "BuyMeACoffee / Ko-fi (Zero upfront donation/micropayments)",
    "Stripe Checkout (Direct links, pay-per-successful-transaction)",
    "GitHub Sponsors (Zero platform fee)"
]
