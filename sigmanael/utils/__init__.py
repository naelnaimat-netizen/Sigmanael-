"""Utility functions for the personal assistant system."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


def get_data_dir() -> Path:
    """Get the data directory for storing user data."""
    data_dir = Path.home() / ".sigmanael"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def load_json(filepath: Path) -> Dict[str, Any]:
    """Load JSON data from file."""
    if not filepath.exists():
        return {}
    
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """Save JSON data to file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def sanitize_user_id(user_id: str) -> str:
    """Sanitize user ID for file system usage."""
    return "".join(c for c in user_id if c.isalnum() or c in ('-', '_'))


class Config:
    """Configuration manager."""
    
    def __init__(self):
        self.config_file = get_data_dir() / "config.json"
        self._config = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        return load_json(self.config_file)
    
    def save(self) -> None:
        """Save configuration to file."""
        save_json(self.config_file, self._config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
        self.save()
    
    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get value from environment or config."""
        return os.getenv(key) or self.get(key, default)
