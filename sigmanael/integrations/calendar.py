"""Calendar integration for managing schedules."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from sigmanael.integrations import BaseIntegration


class CalendarIntegration(BaseIntegration):
    """Integration for calendar management."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.events: List[Dict[str, Any]] = []
    
    @property
    def name(self) -> str:
        return "calendar"
    
    def connect(self) -> bool:
        """Connect to calendar service."""
        # In a real implementation, this would connect to Google Calendar, Outlook, etc.
        self.enabled = True
        return True
    
    def disconnect(self) -> None:
        """Disconnect from calendar service."""
        self.enabled = False
    
    def query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Query calendar for events.
        
        Args:
            query: Query string (e.g., "today", "this week", "tomorrow")
            context: Optional context dictionary
            
        Returns:
            List of events matching the query
        """
        query_lower = query.lower()
        
        if "today" in query_lower:
            return self.get_events_for_day(datetime.now())
        elif "tomorrow" in query_lower:
            return self.get_events_for_day(datetime.now() + timedelta(days=1))
        elif "week" in query_lower:
            return self.get_events_for_week()
        
        return []
    
    def get_events_for_day(self, date: datetime) -> List[Dict[str, Any]]:
        """Get events for a specific day."""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        return [
            event for event in self.events
            if start_of_day <= event.get('start', datetime.min) < end_of_day
        ]
    
    def get_events_for_week(self) -> List[Dict[str, Any]]:
        """Get events for the current week."""
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        
        return [
            event for event in self.events
            if start_of_week <= event.get('start', datetime.min) < end_of_week
        ]
    
    def add_event(self, title: str, start: datetime, end: datetime, 
                  description: str = "") -> Dict[str, Any]:
        """Add a new event to the calendar."""
        event = {
            'title': title,
            'start': start,
            'end': end,
            'description': description
        }
        self.events.append(event)
        return event
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities."""
        return [
            "view_schedule",
            "add_event",
            "query_events",
            "manage_calendar"
        ]
