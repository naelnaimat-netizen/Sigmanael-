"""Base integration class for connecting to digital products."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseIntegration(ABC):
    """Base class for all product integrations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the integration.
        
        Args:
            config: Configuration dictionary for the integration
        """
        self.config = config or {}
        self.enabled = True
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the integration name."""
        pass
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the product/service.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the product/service."""
        pass
    
    @abstractmethod
    def query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Query the integration for data.
        
        Args:
            query: Query string
            context: Optional context dictionary
            
        Returns:
            Query results
        """
        pass
    
    def is_connected(self) -> bool:
        """Check if the integration is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.enabled
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities this integration provides.
        
        Returns:
            List of capability strings
        """
        return []
