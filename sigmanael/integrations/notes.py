"""Notes integration for managing personal notes."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sigmanael.integrations import BaseIntegration


class NotesIntegration(BaseIntegration):
    """Integration for managing personal notes."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.notes: List[Dict[str, Any]] = []
    
    @property
    def name(self) -> str:
        return "notes"
    
    def connect(self) -> bool:
        """Connect to notes service."""
        self.enabled = True
        return True
    
    def disconnect(self) -> None:
        """Disconnect from notes service."""
        self.enabled = False
    
    def query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Query notes.
        
        Args:
            query: Search query
            context: Optional context dictionary
            
        Returns:
            List of notes matching the query
        """
        query_lower = query.lower()
        
        # Simple keyword search
        results = []
        for note in self.notes:
            title_lower = note.get('title', '').lower()
            content_lower = note.get('content', '').lower()
            
            if query_lower in title_lower or query_lower in content_lower:
                results.append(note)
        
        return results
    
    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """Add a new note."""
        note = {
            'id': len(self.notes) + 1,
            'title': title,
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self.notes.append(note)
        return note
    
    def update_note(self, note_id: int, title: Optional[str] = None, 
                   content: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update an existing note."""
        for note in self.notes:
            if note['id'] == note_id:
                if title:
                    note['title'] = title
                if content:
                    note['content'] = content
                note['updated_at'] = datetime.now()
                return note
        return None
    
    def get_all_notes(self) -> List[Dict[str, Any]]:
        """Get all notes."""
        return self.notes.copy()
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities."""
        return [
            "create_note",
            "search_notes",
            "update_note",
            "manage_notes"
        ]
