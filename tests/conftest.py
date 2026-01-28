"""Test configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(autouse=True)
def temp_data_dir(monkeypatch):
    """Create a temporary data directory for tests."""
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)
    
    # Mock the get_data_dir function to use temp directory
    def mock_get_data_dir():
        return temp_path
    
    monkeypatch.setattr("sigmanael.utils.get_data_dir", mock_get_data_dir)
    monkeypatch.setattr("sigmanael.core.get_data_dir", mock_get_data_dir)
    monkeypatch.setattr("sigmanael.learning.get_data_dir", mock_get_data_dir)
    
    yield temp_path
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
