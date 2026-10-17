"""
The Engine - Workspace Isolation & Node Lifecycle Manager
Enforces context isolation between revenue streams and manages safe archiving of retired nodes.
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from the_engine.config import NODES_DIR, get_utc_iso, get_utc_now

logger = logging.getLogger("TheEngine.Isolation")


class NodeIsolationManager:
    def __init__(self, nodes_dir: Path = NODES_DIR):
        self.nodes_dir = nodes_dir
        self.archived_dir = nodes_dir / "archived"
        self.nodes_dir.mkdir(parents=True, exist_ok=True)
        self.archived_dir.mkdir(parents=True, exist_ok=True)

    def get_node_path(self, node_id: str) -> Path:
        """Returns the isolated workspace path for a specific node."""
        return self.nodes_dir / node_id

    def create_node_workspace(self, node_id: str, metadata: Dict[str, Any]) -> Path:
        """
        Initializes an isolated workspace directory with standard project structure:
        - manifest.json
        - public/ (static assets, landing pages)
        - src/ (code and backend tools)
        - distribution/ (marketing, SEO, social)
        - telemetry/ (logs, conversion stats)
        """
        node_path = self.get_node_path(node_id)
        if node_path.exists():
            logger.info(f"Node workspace '{node_id}' already exists at {node_path}")
            return node_path

        node_path.mkdir(parents=True, exist_ok=True)
        (node_path / "public").mkdir(exist_ok=True)
        (node_path / "src").mkdir(exist_ok=True)
        (node_path / "distribution").mkdir(exist_ok=True)
        (node_path / "telemetry").mkdir(exist_ok=True)

        manifest = {
            "node_id": node_id,
            "created_at": get_utc_iso(),
            "status": "INITIALIZED",
            "metadata": metadata,
            "consecutive_negative_cycles": 0,
            "last_evaluated": None
        }

        with open(node_path / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"Isolated node workspace created: {node_path}")
        return node_path

    def read_manifest(self, node_id: str) -> Optional[Dict[str, Any]]:
        manifest_file = self.get_node_path(node_id) / "manifest.json"
        if not manifest_file.exists():
            return None
        with open(manifest_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_manifest(self, node_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        manifest_file = self.get_node_path(node_id) / "manifest.json"
        data = self.read_manifest(node_id) or {"node_id": node_id}
        data.update(updates)
        data["updated_at"] = get_utc_iso()
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data

    def list_active_nodes(self) -> List[str]:
        """Returns all active, non-archived node IDs."""
        nodes = []
        for item in self.nodes_dir.iterdir():
            if item.is_dir() and item.name != "archived" and (item / "manifest.json").exists():
                nodes.append(item.name)
        return sorted(nodes)

    def list_archived_nodes(self) -> List[str]:
        """Returns all archived node IDs."""
        nodes = []
        for item in self.archived_dir.iterdir():
            if item.is_dir() and (item / "manifest.json").exists():
                nodes.append(item.name)
        return sorted(nodes)

    def archive_node(self, node_id: str, reason: str, lessons_learned: Dict[str, Any]) -> Path:
        """
        Safely moves a node workspace to the archived directory,
        extracting lessons learned and preserving all audit logs.
        """
        src = self.get_node_path(node_id)
        if not src.exists():
            raise FileNotFoundError(f"Cannot archive non-existent node '{node_id}'")

        timestamp = get_utc_now().strftime("%Y%m%d_%H%M%S")
        dest = self.archived_dir / f"{node_id}_{timestamp}"

        # Update manifest before moving
        manifest = self.read_manifest(node_id) or {}
        manifest["status"] = "ARCHIVED"
        manifest["archived_at"] = get_utc_iso()
        manifest["archive_reason"] = reason
        manifest["lessons_learned"] = lessons_learned

        with open(src / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Move directory
        shutil.move(str(src), str(dest))
        logger.warning(f"Node '{node_id}' archived to {dest}. Reason: {reason}")
        return dest
