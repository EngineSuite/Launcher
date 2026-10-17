"""
The Engine - Base Agent Class
Defines the standard lifecycle, self-correction retry handler, and HITL interface for all agents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from the_engine.core.hitl import HITLGatekeeper, HITLAlert

logger = logging.getLogger("TheEngine.Agents")


class BaseAgent(ABC):
    def __init__(self, name: str, role: str, hitl_gatekeeper: HITLGatekeeper):
        self.name = name
        self.role = role
        self.hitl = hitl_gatekeeper
        self.retry_counts: Dict[str, int] = {}

    def log(self, message: str, level: str = "info") -> None:
        log_fn = getattr(logger, level.lower(), logger.info)
        log_fn(f"[{self.name} - {self.role}]: {message}")

    def execute_with_self_correction(self, node_id: str, task_name: str, task_fn, *args, **kwargs) -> Any:
        """
        Executes a task. If exceptions occur, attempts self-correction up to 5 times.
        On the 5th consecutive failure on the same error, triggers the HITL gatekeeper.
        """
        attempts = 0
        while attempts < self.hitl.max_consecutive_failures:
            try:
                result = task_fn(*args, **kwargs)
                self.hitl.record_success(node_id, task_name)
                return result
            except Exception as e:
                attempts += 1
                error_code = f"ERR_{task_name.upper()}_{type(e).__name__}"
                self.log(f"Attempt {attempts} failed with {error_code}: {e}", level="warning")

                hitl_alert = self.hitl.check_stagnation(node_id, error_code, str(e))
                if hitl_alert:
                    self.log(f"STAGNATION LIMIT REACHED. Halting node execution.", level="error")
                    print(hitl_alert.format_alert())
                    raise RuntimeError(f"HITL Intervention Required: {hitl_alert.description}")

                # Self-correction hook
                self.attempt_self_repair(node_id, task_name, error_code, e)

        raise RuntimeError(f"Task '{task_name}' failed after {attempts} attempts.")

    def attempt_self_repair(self, node_id: str, task_name: str, error_code: str, error: Exception) -> None:
        """Default hook for self-repairing agent state before retry."""
        self.log(f"Attempting self-repair for {error_code} on task {task_name}...", level="info")

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method to be implemented by each specialized agent."""
        pass
