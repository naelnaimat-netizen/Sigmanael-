"""Behavior learning module for adapting to user patterns."""

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional
import json
from pathlib import Path

from sigmanael.models import BehaviorData
from sigmanael.utils import get_data_dir, load_json, save_json


class BehaviorLearner:
    """Learns and adapts to user behavior patterns."""
    
    def __init__(self, user_id: str):
        """Initialize behavior learner for a user.
        
        Args:
            user_id: Unique user identifier
        """
        self.user_id = user_id
        self.data_file = get_data_dir() / f"behavior_{user_id}.json"
        self.patterns: Dict[str, Any] = self._load_patterns()
        self.action_history: List[BehaviorData] = []
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Load learned patterns from storage."""
        data = load_json(self.data_file)
        return data.get('patterns', {
            'common_queries': defaultdict(int),
            'preferred_times': defaultdict(int),
            'interaction_style': {},
            'topic_interests': defaultdict(int)
        })
    
    def _save_patterns(self) -> None:
        """Save learned patterns to storage."""
        data = {
            'patterns': dict(self.patterns),
            'last_updated': datetime.now().isoformat()
        }
        save_json(self.data_file, data)
    
    def record_action(self, action: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Record a user action for learning.
        
        Args:
            action: Action type (e.g., 'query', 'command', 'integration_use')
            context: Additional context about the action
        """
        behavior_data = BehaviorData(
            user_id=self.user_id,
            action=action,
            context=context or {}
        )
        self.action_history.append(behavior_data)
        self._update_patterns(behavior_data)
    
    def _update_patterns(self, behavior: BehaviorData) -> None:
        """Update learned patterns based on new behavior data."""
        # Track common queries
        if behavior.action == 'query':
            query_type = behavior.context.get('query_type', 'general')
            if 'common_queries' not in self.patterns:
                self.patterns['common_queries'] = defaultdict(int)
            self.patterns['common_queries'][query_type] = \
                self.patterns['common_queries'].get(query_type, 0) + 1
        
        # Track preferred interaction times
        hour = behavior.timestamp.hour
        if 'preferred_times' not in self.patterns:
            self.patterns['preferred_times'] = defaultdict(int)
        self.patterns['preferred_times'][str(hour)] = \
            self.patterns['preferred_times'].get(str(hour), 0) + 1
        
        # Track topic interests
        if 'topic' in behavior.context:
            topic = behavior.context['topic']
            if 'topic_interests' not in self.patterns:
                self.patterns['topic_interests'] = defaultdict(int)
            self.patterns['topic_interests'][topic] = \
                self.patterns['topic_interests'].get(topic, 0) + 1
        
        self._save_patterns()
    
    def get_suggestions(self, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """Get personalized suggestions based on learned behavior.
        
        Args:
            context: Current context
            
        Returns:
            List of suggested actions or queries
        """
        suggestions = []
        
        # Suggest based on common queries
        common_queries = dict(self.patterns.get('common_queries', {}))
        if common_queries:
            top_queries = sorted(common_queries.items(), key=lambda x: x[1], reverse=True)[:3]
            suggestions.extend([f"Check {q[0]}" for q in top_queries])
        
        # Suggest based on time of day
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            suggestions.append("Review morning schedule")
        elif 12 <= current_hour < 18:
            suggestions.append("Check afternoon tasks")
        else:
            suggestions.append("Review tomorrow's plans")
        
        return suggestions
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences learned from behavior.
        
        Returns:
            Dictionary of learned preferences
        """
        return {
            'common_queries': dict(self.patterns.get('common_queries', {})),
            'preferred_times': dict(self.patterns.get('preferred_times', {})),
            'topic_interests': dict(self.patterns.get('topic_interests', {}))
        }
    
    def adapt_response_style(self, base_response: str) -> str:
        """Adapt response style based on learned preferences.
        
        Args:
            base_response: Base response text
            
        Returns:
            Adapted response
        """
        # In a real implementation, this would adjust tone, verbosity, etc.
        # based on user interaction history
        style = self.patterns.get('interaction_style', {})
        
        # Simple example: adjust formality
        if style.get('formality') == 'casual':
            return base_response.replace('Hello', 'Hey').replace('please', '')
        
        return base_response
