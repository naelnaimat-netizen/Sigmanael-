"""Tests for the personal assistant core functionality."""

import pytest
from datetime import datetime, timedelta

from sigmanael.core.assistant import PersonalAssistant
from sigmanael.integrations.calendar import CalendarIntegration
from sigmanael.integrations.notes import NotesIntegration


class TestPersonalAssistant:
    """Test cases for PersonalAssistant."""
    
    def test_initialization(self):
        """Test assistant initialization."""
        assistant = PersonalAssistant(user_id="test_user", user_name="Test User")
        
        assert assistant.user_id == "test_user"
        assert assistant.user_name == "Test User"
        assert assistant.profile is not None
        assert assistant.learner is not None
    
    def test_add_integration(self):
        """Test adding integrations."""
        assistant = PersonalAssistant(user_id="test_user")
        calendar = CalendarIntegration()
        
        result = assistant.add_integration(calendar)
        
        assert result is True
        assert "calendar" in assistant.integrations
    
    def test_remove_integration(self):
        """Test removing integrations."""
        assistant = PersonalAssistant(user_id="test_user")
        calendar = CalendarIntegration()
        assistant.add_integration(calendar)
        
        assistant.remove_integration("calendar")
        
        assert "calendar" not in assistant.integrations
    
    def test_start_conversation(self):
        """Test starting a conversation."""
        assistant = PersonalAssistant(user_id="test_user")
        
        conv_id = assistant.start_conversation()
        
        assert conv_id is not None
        assert assistant.current_conversation is not None
        assert assistant.current_conversation.conversation_id == conv_id
    
    def test_chat_basic(self):
        """Test basic chat functionality."""
        assistant = PersonalAssistant(user_id="test_user", user_name="Test")
        
        response = assistant.chat("Hello")
        
        assert response is not None
        assert "Test" in response or "hello" in response.lower()
    
    def test_chat_help(self):
        """Test help command."""
        assistant = PersonalAssistant(user_id="test_user")
        assistant.add_integration(CalendarIntegration())
        
        response = assistant.chat("What can you do?")
        
        assert "help" in response.lower() or "calendar" in response.lower()
    
    def test_calendar_integration(self):
        """Test calendar integration."""
        assistant = PersonalAssistant(user_id="test_user")
        calendar = CalendarIntegration()
        
        # Add event
        now = datetime.now()
        calendar.add_event(
            title="Test Meeting",
            start=now,
            end=now + timedelta(hours=1)
        )
        
        assistant.add_integration(calendar)
        
        response = assistant.chat("What's on my schedule today?")
        
        assert "Test Meeting" in response or "event" in response.lower()
    
    def test_notes_integration(self):
        """Test notes integration."""
        assistant = PersonalAssistant(user_id="test_user")
        notes = NotesIntegration()
        
        # Add note
        notes.add_note(
            title="Test Note",
            content="This is a test"
        )
        
        assistant.add_integration(notes)
        
        response = assistant.chat("Find my test notes")
        
        assert "Test Note" in response or "note" in response.lower()
    
    def test_behavior_learning(self):
        """Test behavior learning."""
        assistant = PersonalAssistant(user_id="test_user")
        
        # Simulate interactions
        for _ in range(3):
            assistant.chat("What's on my schedule?")
        
        # Check that behavior was recorded
        preferences = assistant.learner.get_preferences()
        
        assert preferences is not None
        assert "common_queries" in preferences
    
    def test_preferences_update(self):
        """Test updating preferences."""
        assistant = PersonalAssistant(user_id="test_user")
        
        new_prefs = {"theme": "dark", "language": "en"}
        assistant.update_preferences(new_prefs)
        
        assert assistant.profile.preferences["theme"] == "dark"
        assert assistant.profile.preferences["language"] == "en"


class TestCalendarIntegration:
    """Test cases for CalendarIntegration."""
    
    def test_initialization(self):
        """Test calendar initialization."""
        calendar = CalendarIntegration()
        
        assert calendar.name == "calendar"
        assert calendar.events == []
    
    def test_connect(self):
        """Test calendar connection."""
        calendar = CalendarIntegration()
        
        result = calendar.connect()
        
        assert result is True
        assert calendar.enabled is True
    
    def test_add_event(self):
        """Test adding events."""
        calendar = CalendarIntegration()
        now = datetime.now()
        
        event = calendar.add_event(
            title="Test Event",
            start=now,
            end=now + timedelta(hours=1),
            description="Test description"
        )
        
        assert event is not None
        assert event["title"] == "Test Event"
        assert len(calendar.events) == 1
    
    def test_query_today(self):
        """Test querying today's events."""
        calendar = CalendarIntegration()
        now = datetime.now()
        
        calendar.add_event(
            title="Today's Event",
            start=now,
            end=now + timedelta(hours=1)
        )
        
        results = calendar.query("today")
        
        assert len(results) > 0
        assert results[0]["title"] == "Today's Event"


class TestNotesIntegration:
    """Test cases for NotesIntegration."""
    
    def test_initialization(self):
        """Test notes initialization."""
        notes = NotesIntegration()
        
        assert notes.name == "notes"
        assert notes.notes == []
    
    def test_add_note(self):
        """Test adding notes."""
        notes = NotesIntegration()
        
        note = notes.add_note(
            title="Test Note",
            content="Test content",
            tags=["test"]
        )
        
        assert note is not None
        assert note["title"] == "Test Note"
        assert len(notes.notes) == 1
    
    def test_query_notes(self):
        """Test querying notes."""
        notes = NotesIntegration()
        
        notes.add_note(title="Shopping List", content="Buy milk")
        notes.add_note(title="Todo", content="Finish project")
        
        results = notes.query("shopping")
        
        assert len(results) == 1
        assert results[0]["title"] == "Shopping List"
    
    def test_update_note(self):
        """Test updating notes."""
        notes = NotesIntegration()
        
        note = notes.add_note(title="Original", content="Original content")
        note_id = note["id"]
        
        updated = notes.update_note(note_id, title="Updated")
        
        assert updated is not None
        assert updated["title"] == "Updated"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
