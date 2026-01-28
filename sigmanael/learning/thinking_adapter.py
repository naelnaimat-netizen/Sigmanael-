"""Enhanced thinking pattern adaptation module.

This module enables the assistant to mirror the user's thinking style
while maintaining ethical and legal boundaries.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from sigmanael.learning import BehaviorLearner


class ThinkingPatternAdapter:
    """Adapts to user's thinking patterns and communication style."""
    
    def __init__(self, user_id: str, learner: BehaviorLearner):
        """Initialize the thinking pattern adapter.
        
        Args:
            user_id: User identifier
            learner: BehaviorLearner instance
        """
        self.user_id = user_id
        self.learner = learner
        self.patterns: Dict[str, Any] = {
            'communication_style': {},
            'decision_making': {},
            'information_processing': {},
            'problem_solving': {},
            'priorities': {},
            'thinking_speed': 'moderate',
            'detail_level': 'balanced'
        }
    
    def analyze_communication_style(self, message: str, response: str) -> None:
        """Analyze and learn communication patterns.
        
        Args:
            message: User's message
            response: Assistant's response
        """
        # Track formality
        formal_indicators = ['please', 'thank you', 'kindly', 'regards']
        casual_indicators = ['hey', 'yeah', 'gonna', 'wanna']
        
        message_lower = message.lower()
        formality_score = sum(1 for ind in formal_indicators if ind in message_lower)
        formality_score -= sum(1 for ind in casual_indicators if ind in message_lower)
        
        if 'formality' not in self.patterns['communication_style']:
            self.patterns['communication_style']['formality'] = []
        self.patterns['communication_style']['formality'].append(formality_score)
        
        # Track verbosity preference
        msg_length = len(message.split())
        if 'preferred_length' not in self.patterns['communication_style']:
            self.patterns['communication_style']['preferred_length'] = []
        self.patterns['communication_style']['preferred_length'].append(msg_length)
    
    def analyze_decision_making(self, context: Dict[str, Any]) -> None:
        """Analyze decision-making patterns.
        
        Args:
            context: Context with decision information
        """
        if 'decision' in context:
            decision_type = context.get('decision_type', 'unknown')
            speed = context.get('decision_speed', 'moderate')
            
            if 'types' not in self.patterns['decision_making']:
                self.patterns['decision_making']['types'] = defaultdict(int)
            self.patterns['decision_making']['types'][decision_type] += 1
            
            if 'speed' not in self.patterns['decision_making']:
                self.patterns['decision_making']['speed'] = []
            self.patterns['decision_making']['speed'].append(speed)
    
    def analyze_information_processing(self, query_type: str, detail_requested: str) -> None:
        """Analyze how user processes information.
        
        Args:
            query_type: Type of information query
            detail_requested: Level of detail requested (high/medium/low)
        """
        if 'preferences' not in self.patterns['information_processing']:
            self.patterns['information_processing']['preferences'] = defaultdict(int)
        
        key = f"{query_type}:{detail_requested}"
        self.patterns['information_processing']['preferences'][key] += 1
    
    def get_adapted_response_style(self) -> Dict[str, Any]:
        """Get adapted response style based on learned patterns.
        
        Returns:
            Dictionary with style parameters
        """
        style = {
            'formality': 'neutral',
            'verbosity': 'moderate',
            'detail_level': 'balanced',
            'structure': 'organized'
        }
        
        # Determine formality
        if 'formality' in self.patterns['communication_style']:
            formality_scores = self.patterns['communication_style']['formality']
            if formality_scores:
                avg_formality = sum(formality_scores) / len(formality_scores)
                if avg_formality > 1:
                    style['formality'] = 'formal'
                elif avg_formality < -1:
                    style['formality'] = 'casual'
        
        # Determine verbosity
        if 'preferred_length' in self.patterns['communication_style']:
            lengths = self.patterns['communication_style']['preferred_length']
            if lengths:
                avg_length = sum(lengths) / len(lengths)
                if avg_length > 30:
                    style['verbosity'] = 'detailed'
                elif avg_length < 10:
                    style['verbosity'] = 'concise'
        
        return style
    
    def adapt_response(self, base_response: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Adapt response to match user's thinking pattern.
        
        Args:
            base_response: Original response text
            context: Optional context information
            
        Returns:
            Adapted response
        """
        style = self.get_adapted_response_style()
        adapted = base_response
        
        # Apply formality
        if style['formality'] == 'casual':
            adapted = adapted.replace('Hello', 'Hey')
            adapted = adapted.replace('please', '')
            adapted = adapted.replace('Thank you', 'Thanks')
        elif style['formality'] == 'formal':
            adapted = adapted.replace('Hey', 'Hello')
            adapted = adapted.replace('Thanks', 'Thank you')
        
        # Apply verbosity
        if style['verbosity'] == 'concise' and len(adapted.split()) > 50:
            # Summarize if too verbose for user preference
            sentences = adapted.split('. ')
            adapted = '. '.join(sentences[:3]) + '.'
        
        return adapted
    
    def get_thinking_insights(self) -> Dict[str, Any]:
        """Get insights about user's thinking patterns.
        
        Returns:
            Dictionary with thinking pattern insights
        """
        insights = {
            'communication_style': self.get_adapted_response_style(),
            'common_topics': self.learner.get_preferences().get('topic_interests', {}),
            'interaction_patterns': {
                'preferred_times': self.learner.get_preferences().get('preferred_times', {}),
                'common_queries': self.learner.get_preferences().get('common_queries', {})
            }
        }
        
        return insights
    
    def apply_ethical_filter(self, message: str) -> tuple[bool, Optional[str]]:
        """Apply ethical guidelines to message processing.
        
        Args:
            message: Message to check
            
        Returns:
            Tuple of (is_acceptable, reason_if_not)
        """
        # Check for harmful content indicators
        harmful_keywords = [
            'illegal', 'harm', 'attack', 'weapon', 'violence',
            'abuse', 'exploit', 'manipulate', 'deceive'
        ]
        
        message_lower = message.lower()
        for keyword in harmful_keywords:
            if keyword in message_lower:
                # This is a simple check - in production, use more sophisticated NLP
                return False, f"Request may violate ethical guidelines"
        
        return True, None
    
    def apply_legal_filter(self, message: str) -> tuple[bool, Optional[str]]:
        """Apply legal boundaries to message processing.
        
        Args:
            message: Message to check
            
        Returns:
            Tuple of (is_acceptable, reason_if_not)
        """
        # Check for legal violation indicators
        legal_keywords = [
            'copyright infringement', 'piracy', 'hack', 'crack',
            'steal', 'fraud', 'scam'
        ]
        
        message_lower = message.lower()
        for keyword in legal_keywords:
            if keyword in message_lower:
                return False, f"Request may violate legal boundaries"
        
        return True, None
