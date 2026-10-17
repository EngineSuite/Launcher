"""
The Engine - Financial Ledger & Zero-Cost Guardrail Controller
Monitors spend vs. revenue, calculates ROI daily, and enforces the $0 upfront cost mandate.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from the_engine.config import LEDGER_PATH, INITIAL_CAPITAL, STRICT_ZERO_COST, get_utc_iso

logger = logging.getLogger("TheEngine.Ledger")


class Ledger:
    def __init__(self, ledger_path: Path = LEDGER_PATH):
        self.ledger_path = ledger_path
        self.data: Dict[str, Any] = {
            "initial_capital": INITIAL_CAPITAL,
            "earned_balance": 0.00,
            "total_revenue": 0.00,
            "total_expenses": 0.00,
            "safe_account_reserve": 0.00,
            "reinvestable_balance": 0.00,
            "nodes": {},
            "transactions": [],
            "daily_snapshots": []
        }
        self.load()

    def load(self) -> None:
        """Loads the ledger from disk, or initializes it if not found."""
        if self.ledger_path.exists():
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load ledger: {e}, reinitializing defaults.")
                self.save()
        else:
            self.save()

    def save(self) -> None:
        """Saves current ledger state to disk."""
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def can_spend(self, amount: float) -> bool:
        """
        Enforces the EARN IT FIRST principle.
        If strict zero cost is active, spending is strictly forbidden unless
        covered by existing reinvestable balance.
        """
        if amount <= 0:
            return True
        if STRICT_ZERO_COST:
            return self.data["reinvestable_balance"] >= amount
        return False

    def record_revenue(self, node_id: str, amount: float, source: str, description: str = "") -> Dict[str, Any]:
        """
        Records verified incoming revenue.
        By default, 50% goes to the Safe Account Reserve (untouchable profit)
        and 50% goes to the Reinvestable Balance.
        """
        if amount <= 0:
            raise ValueError("Revenue amount must be positive.")

        timestamp = get_utc_iso()
        reserve_allocation = round(amount * 0.50, 2)
        reinvest_allocation = round(amount - reserve_allocation, 2)

        self.data["total_revenue"] = round(self.data["total_revenue"] + amount, 2)
        self.data["earned_balance"] = round(self.data["earned_balance"] + amount, 2)
        self.data["safe_account_reserve"] = round(self.data["safe_account_reserve"] + reserve_allocation, 2)
        self.data["reinvestable_balance"] = round(self.data["reinvestable_balance"] + reinvest_allocation, 2)

        if node_id not in self.data["nodes"]:
            self.data["nodes"][node_id] = {"revenue": 0.0, "expenses": 0.0, "transactions": []}

        self.data["nodes"][node_id]["revenue"] = round(self.data["nodes"][node_id]["revenue"] + amount, 2)

        tx = {
            "id": f"rev_{len(self.data['transactions']) + 1}",
            "type": "REVENUE",
            "node_id": node_id,
            "amount": amount,
            "source": source,
            "description": description,
            "timestamp": timestamp,
            "reserve_allocation": reserve_allocation,
            "reinvest_allocation": reinvest_allocation
        }
        self.data["transactions"].append(tx)
        self.data["nodes"][node_id]["transactions"].append(tx["id"])
        self.save()
        return tx

    def record_expense(self, node_id: str, amount: float, category: str, description: str = "") -> Dict[str, Any]:
        """
        Records an expense if permitted by the zero-cost guardrail.
        Throws a PermissionError if funds have not been earned first.
        """
        if amount <= 0:
            return {"status": "NOOP", "amount": 0.0}

        if not self.can_spend(amount):
            raise PermissionError(
                f"ZERO-COST GUARDRAIL TRIGGERED: Cannot spend ${amount:.2f}. "
                f"Available reinvestable balance is ${self.data['reinvestable_balance']:.2f}. "
                f"Rule: Earn revenue first before spending."
            )

        timestamp = get_utc_iso()
        self.data["total_expenses"] = round(self.data["total_expenses"] + amount, 2)
        self.data["reinvestable_balance"] = round(self.data["reinvestable_balance"] - amount, 2)

        if node_id not in self.data["nodes"]:
            self.data["nodes"][node_id] = {"revenue": 0.0, "expenses": 0.0, "transactions": []}

        self.data["nodes"][node_id]["expenses"] = round(self.data["nodes"][node_id]["expenses"] + amount, 2)

        tx = {
            "id": f"exp_{len(self.data['transactions']) + 1}",
            "type": "EXPENSE",
            "node_id": node_id,
            "amount": amount,
            "category": category,
            "description": description,
            "timestamp": timestamp
        }
        self.data["transactions"].append(tx)
        self.data["nodes"][node_id]["transactions"].append(tx["id"])
        self.save()
        return tx

    def get_node_summary(self, node_id: str) -> Dict[str, Any]:
        """Returns financial summary for a specific node."""
        node_info = self.data["nodes"].get(node_id, {"revenue": 0.0, "expenses": 0.0, "transactions": []})
        rev = node_info["revenue"]
        exp = node_info["expenses"]
        net = round(rev - exp, 2)
        roi = round(((rev - exp) / exp * 100), 2) if exp > 0 else (100.0 if rev > 0 else 0.0)
        return {
            "node_id": node_id,
            "revenue": rev,
            "expenses": exp,
            "net_profit": net,
            "roi_percentage": roi,
            "transaction_count": len(node_info.get("transactions", []))
        }

    def get_global_summary(self) -> Dict[str, Any]:
        """Returns the high-level financial health of The Engine."""
        rev = self.data["total_revenue"]
        exp = self.data["total_expenses"]
        net = round(rev - exp, 2)
        return {
            "initial_capital": self.data["initial_capital"],
            "total_revenue": rev,
            "total_expenses": exp,
            "net_profit": net,
            "safe_account_reserve": self.data["safe_account_reserve"],
            "reinvestable_balance": self.data["reinvestable_balance"],
            "active_node_count": len(self.data["nodes"]),
            "zero_cost_integrity": exp == 0.0 if rev == 0.0 else exp <= rev
        }
