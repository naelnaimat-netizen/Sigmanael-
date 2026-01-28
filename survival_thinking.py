"""
Survival Thinking Framework - Practical Implementation
Inspired by wolf pack behavior and natural survival strategies
"""

from enum import Enum
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime


class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class RewardLevel(Enum):
    """Potential reward levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXCEPTIONAL = 4


class DecisionAction(Enum):
    """Recommended actions based on risk/reward analysis"""
    ACT_IMMEDIATELY = "Act immediately - high reward, low risk"
    PREPARE_AND_ACT = "Prepare thoroughly, then act - high reward, high risk"
    ACT_IF_CONVENIENT = "Act if convenient - low reward, low risk"
    AVOID = "Avoid - low reward, high risk"
    REASSESS = "Reassess - unclear risk/reward profile"


@dataclass
class Opportunity:
    """Represents a potential opportunity or challenge"""
    name: str
    description: str
    risk_level: RiskLevel
    reward_level: RewardLevel
    resources_required: List[str]
    time_sensitive: bool = False
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PackMember:
    """Represents a team member with specific strengths"""
    name: str
    strengths: List[str]
    experience_level: int  # 1-10
    available: bool = True
    current_task: Optional[str] = None


class WolfThinkingEngine:
    """
    Main engine for implementing wolf-inspired decision making
    """
    
    def __init__(self, pack_name: str = "Alpha Pack"):
        self.pack_name = pack_name
        self.pack_members: List[PackMember] = []
        self.territory: Dict[str, any] = {}
        self.learned_patterns: List[Dict] = []
        self.resources: Dict[str, int] = {}
        
    def scan_environment(self, threats: List[str], opportunities: List[Opportunity], 
                        resources: Dict[str, int]) -> Dict:
        """
        STEP 1: Survey the environment
        
        Wolf behavior: Constantly aware of surroundings through multiple senses
        """
        scan_result = {
            'timestamp': datetime.now(),
            'threats_detected': len(threats),
            'threats': threats,
            'opportunities_detected': len(opportunities),
            'opportunities': opportunities,
            'resources_available': resources,
            'threat_level': self._assess_overall_threat(threats)
        }
        
        # Update internal state
        self.resources = resources
        
        return scan_result
    
    def assess_pack_capacity(self, required_skills: List[str]) -> Dict:
        """
        STEP 2: Evaluate pack capacity
        
        Wolf behavior: Know the strengths and limitations of each pack member
        """
        available_members = [m for m in self.pack_members if m.available]
        
        capability_score = 0
        matched_members = []
        
        for skill in required_skills:
            for member in available_members:
                if skill.lower() in [s.lower() for s in member.strengths]:
                    capability_score += member.experience_level
                    matched_members.append({
                        'member': member.name,
                        'skill': skill,
                        'experience': member.experience_level
                    })
                    break
        
        return {
            'total_capacity': len(available_members),
            'available_members': [m.name for m in available_members],
            'capability_score': capability_score,
            'skill_matches': matched_members,
            'readiness': capability_score >= len(required_skills) * 5  # Average 5+ experience
        }
    
    def strategize(self, opportunity: Opportunity, pack_assessment: Dict) -> Dict:
        """
        STEP 3: Plan the approach
        
        Wolf behavior: Patient observation and strategic planning before action
        """
        decision = self._evaluate_risk_reward(opportunity.risk_level, opportunity.reward_level)
        
        # Check if we have the resources
        resource_check = all(
            self.resources.get(resource, 0) > 0 
            for resource in opportunity.resources_required
        )
        
        # Develop strategy
        strategy = {
            'opportunity': opportunity.name,
            'decision': decision.value,
            'action_type': decision,
            'pack_ready': pack_assessment['readiness'],
            'resources_available': resource_check,
            'recommended_approach': self._generate_approach(opportunity, pack_assessment),
            'contingency_plan': self._generate_contingency(opportunity),
            'go_no_go': pack_assessment['readiness'] and resource_check and decision != DecisionAction.AVOID
        }
        
        return strategy
    
    def coordinate_pack(self, strategy: Dict, required_skills: List[str]) -> List[Dict]:
        """
        STEP 4: Align the pack
        
        Wolf behavior: Clear communication and role assignment
        """
        assignments = []
        available_members = [m for m in self.pack_members if m.available]
        
        # Assign roles based on strengths
        for skill in required_skills:
            best_match = None
            best_score = 0
            
            for member in available_members:
                if skill.lower() in [s.lower() for s in member.strengths]:
                    if member.experience_level > best_score:
                        best_score = member.experience_level
                        best_match = member
            
            if best_match:
                assignments.append({
                    'role': skill,
                    'assigned_to': best_match.name,
                    'experience_level': best_match.experience_level
                })
                best_match.available = False
                best_match.current_task = strategy['opportunity']
        
        return assignments
    
    def execute(self, strategy: Dict, execution_func: Callable) -> Dict:
        """
        STEP 5: Execute with precision
        
        Wolf behavior: Strike at optimal moment with coordinated action
        """
        if not strategy['go_no_go']:
            return {
                'status': 'aborted',
                'reason': 'Strategy assessment failed go/no-go criteria',
                'timestamp': datetime.now()
            }
        
        try:
            result = execution_func()
            execution_result = {
                'status': 'success',
                'result': result,
                'timestamp': datetime.now(),
                'strategy_used': strategy['recommended_approach']
            }
        except Exception as e:
            execution_result = {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now(),
                'contingency_activated': True
            }
        
        # Learn from execution
        self.reflect(strategy, execution_result)
        
        return execution_result
    
    def reflect(self, strategy: Dict, outcome: Dict):
        """
        STEP 6: Learn from outcomes
        
        Wolf behavior: Adapt hunting strategies based on success/failure
        """
        lesson = {
            'timestamp': datetime.now(),
            'opportunity': strategy['opportunity'],
            'approach': strategy['recommended_approach'],
            'outcome': outcome['status'],
            'success': outcome['status'] == 'success'
        }
        
        self.learned_patterns.append(lesson)
        
        # Make pack members available again
        for member in self.pack_members:
            if member.current_task == strategy['opportunity']:
                member.available = True
                member.current_task = None
                # Increase experience slightly if successful
                if outcome['status'] == 'success':
                    member.experience_level = min(10, member.experience_level + 0.1)
    
    def _evaluate_risk_reward(self, risk: RiskLevel, reward: RewardLevel) -> DecisionAction:
        """
        Risk/Reward matrix for decision making
        """
        if reward.value >= 3 and risk.value <= 2:
            return DecisionAction.ACT_IMMEDIATELY
        elif reward.value >= 3 and risk.value >= 3:
            return DecisionAction.PREPARE_AND_ACT
        elif reward.value <= 2 and risk.value <= 2:
            return DecisionAction.ACT_IF_CONVENIENT
        elif reward.value <= 2 and risk.value >= 3:
            return DecisionAction.AVOID
        else:
            return DecisionAction.REASSESS
    
    def _assess_overall_threat(self, threats: List[str]) -> str:
        """Assess the overall threat level"""
        if len(threats) == 0:
            return "low"
        elif len(threats) <= 2:
            return "moderate"
        elif len(threats) <= 4:
            return "high"
        else:
            return "critical"
    
    def _generate_approach(self, opportunity: Opportunity, assessment: Dict) -> str:
        """Generate recommended approach based on opportunity and capabilities"""
        if opportunity.time_sensitive:
            return "Swift coordinated strike - time-sensitive opportunity"
        elif opportunity.risk_level.value >= 3:
            return "Cautious approach - high risk requires preparation"
        elif assessment['capability_score'] > len(opportunity.resources_required) * 7:
            return "Aggressive approach - pack is highly capable"
        else:
            return "Measured approach - balance capability with risk"
    
    def _generate_contingency(self, opportunity: Opportunity) -> str:
        """Generate contingency plan"""
        if opportunity.risk_level.value >= 3:
            return "Retreat and reassess if conditions worsen"
        else:
            return "Adapt approach based on initial results"
    
    def add_pack_member(self, member: PackMember):
        """Add a member to the pack"""
        self.pack_members.append(member)
    
    def get_pack_status(self) -> Dict:
        """Get current pack status"""
        return {
            'pack_name': self.pack_name,
            'total_members': len(self.pack_members),
            'available_members': len([m for m in self.pack_members if m.available]),
            'resources': self.resources,
            'learned_patterns': len(self.learned_patterns),
            'recent_successes': len([p for p in self.learned_patterns if p['success']])
        }


# Example usage
if __name__ == "__main__":
    # Initialize the pack
    wolf_engine = WolfThinkingEngine("Sigma Pack")
    
    # Add pack members
    wolf_engine.add_pack_member(PackMember("Alpha", ["leadership", "strategy"], 9))
    wolf_engine.add_pack_member(PackMember("Beta", ["tracking", "analysis"], 8))
    wolf_engine.add_pack_member(PackMember("Scout", ["reconnaissance", "speed"], 7))
    wolf_engine.add_pack_member(PackMember("Hunter", ["execution", "strength"], 8))
    
    # Define an opportunity
    opportunity = Opportunity(
        name="New Territory Expansion",
        description="Opportunity to expand into adjacent territory",
        risk_level=RiskLevel.MEDIUM,
        reward_level=RewardLevel.HIGH,
        resources_required=["energy", "time", "coordination"],
        time_sensitive=True
    )
    
    # Execute the wolf decision process
    print("=== WOLF THINKING FRAMEWORK - DECISION PROCESS ===\n")
    
    # Step 1: Scan
    scan = wolf_engine.scan_environment(
        threats=["competing pack", "resource scarcity"],
        opportunities=[opportunity],
        resources={"energy": 80, "time": 5, "coordination": 10}
    )
    print(f"1. SCAN: Detected {scan['opportunities_detected']} opportunities, {scan['threats_detected']} threats")
    print(f"   Threat Level: {scan['threat_level']}\n")
    
    # Step 2: Assess
    assessment = wolf_engine.assess_pack_capacity(["leadership", "tracking", "execution"])
    print(f"2. ASSESS: Pack readiness = {assessment['readiness']}")
    print(f"   Capability Score: {assessment['capability_score']}\n")
    
    # Step 3: Strategize
    strategy = wolf_engine.strategize(opportunity, assessment)
    print(f"3. STRATEGIZE: Decision = {strategy['decision']}")
    print(f"   Approach: {strategy['recommended_approach']}")
    print(f"   Go/No-Go: {strategy['go_no_go']}\n")
    
    # Step 4: Coordinate
    assignments = wolf_engine.coordinate_pack(strategy, ["leadership", "tracking", "execution"])
    print(f"4. COORDINATE: Assigned {len(assignments)} roles")
    for assignment in assignments:
        print(f"   {assignment['role']} -> {assignment['assigned_to']} (exp: {assignment['experience_level']})")
    print()
    
    # Step 5: Execute
    def sample_execution():
        return "Territory successfully expanded by 20%"
    
    result = wolf_engine.execute(strategy, sample_execution)
    print(f"5. EXECUTE: Status = {result['status']}")
    if result['status'] == 'success':
        print(f"   Result: {result['result']}\n")
    
    # Step 6: Reflect (automatic in execute)
    status = wolf_engine.get_pack_status()
    print(f"6. REFLECT: Learned patterns = {status['learned_patterns']}")
    print(f"   Recent successes: {status['recent_successes']}/{status['learned_patterns']}")
    print(f"\nPack Status: {status['available_members']}/{status['total_members']} members available")
