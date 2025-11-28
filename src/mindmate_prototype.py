"""
MindMate Harmony Space - Python Prototype
DEMONSTRATES ALL 3 HACKATHON AGENTS
Team MetaUnit: Freddie Bundi, Lazarus Gatimu, Michelle Alex
"""

from datetime import datetime
import json

class MindMateAI:
    """
    Implements all 3 required hackathon agents in Python
    Can be later converted to Jaclang once syntax is resolved
    """
    
    def __init__(self):
        self.emotional_history = []
        self.setup_strategies()
    
    def setup_strategies(self):
        """Initialize coping strategies database"""
        self.strategies = {
            "anxious": [
                {"name": "Deep Breathing", "effectiveness": 0.8, "description": "Take 5 slow, deep breaths"},
                {"name": "Grounding Technique", "effectiveness": 0.7, "description": "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste"}
            ],
            "sad": [
                {"name": "Gratitude Journal", "effectiveness": 0.6, "description": "Write down 3 things you're grateful for"},
                {"name": "Positive Activity", "effectiveness": 0.7, "description": "Do something you usually enjoy"}
            ],
            "angry": [
                {"name": "Physical Activity", "effectiveness": 0.9, "description": "10-minute walk or stretch"},
                {"name": "Timeout", "effectiveness": 0.8, "description": "Remove yourself from the situation for 5 minutes"}
            ],
            "stressed": [
                {"name": "Priority List", "effectiveness": 0.7, "description": "Write down and prioritize your tasks"},
                {"name": "Breakdown", "effectiveness": 0.6, "description": "Break big tasks into smaller steps"}
            ]
        }
    
    # AGENT 1: Mood Logger
    def log_mood(self, mood, intensity, situation, triggers=None, notes=None):
        """Agent 1: Tracks emotional states with context"""
        emotional_state = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "intensity": intensity,
            "situation": situation,
            "triggers": triggers or [],
            "notes": notes
        }
        self.emotional_history.append(emotional_state)
        print(f"📝 Mood logged: {mood} (intensity: {intensity})")
        return emotional_state
    
    # AGENT 2: Pattern Analyzer
    def analyze_patterns(self):
        """Agent 2: Analyzes emotional trends and patterns"""
        if not self.emotional_history:
            return {"status": "no_data", "message": "No emotional data yet"}
        
        # Analyze frequency
        mood_counts = {}
        intensity_sum = {}
        
        for state in self.emotional_history:
            mood = state["mood"]
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            intensity_sum[mood] = intensity_sum.get(mood, 0) + state["intensity"]
        
        # Calculate insights
        most_common_mood = max(mood_counts, key=mood_counts.get)
        average_intensities = {mood: intensity_sum[mood]/count for mood, count in mood_counts.items()}
        
        # Trigger analysis
        all_triggers = []
        for state in self.emotional_history:
            all_triggers.extend(state["triggers"])
        
        common_triggers = {}
        for trigger in all_triggers:
            common_triggers[trigger] = common_triggers.get(trigger, 0) + 1
        
        return {
            "most_common_mood": most_common_mood,
            "mood_frequency": mood_counts,
            "average_intensities": average_intensities,
            "common_triggers": common_triggers,
            "total_entries": len(self.emotional_history)
        }
    
    # AGENT 3: Strategy Suggester
    def suggest_strategies(self, current_mood, intensity):
        """Agent 3: Recommends personalized coping strategies"""
        if current_mood not in self.strategies:
            # Default strategies for unknown moods
            return [{
                "name": "Mindful Breathing", 
                "effectiveness": 0.7, 
                "description": "Focus on your breath for 2 minutes"
            }]
        
        strategies = self.strategies[current_mood]
        
        # Sort by effectiveness (consider intensity)
        if intensity >= 7:  # High intensity
            strategies.sort(key=lambda x: x["effectiveness"], reverse=True)
        else:  # Lower intensity
            strategies.sort(key=lambda x: x["effectiveness"])
        
        return strategies[:2]  # Return top 2 suggestions

def demo_all_agents():
    """Demonstrate all 3 hackathon agents working together"""
    print("🧠 MINDMATE HARMONY SPACE - TEAM METAUNIT")
    print("=" * 60)
    
    ai = MindMateAI()
    
    print("\\n🎯 DEMONSTRATING ALL 3 HACKATHON AGENTS:")
    print("=" * 40)
    
    # AGENT 1: Log sample data
    print("\\n1. AGENT 1: Mood Logger")
    ai.log_mood("excited", 8, "starting hackathon", ["collaboration", "learning"])
    ai.log_mood("anxious", 6, "technical challenges", ["uncertainty"])
    ai.log_mood("happy", 7, "making progress", ["accomplishment"])
    ai.log_mood("anxious", 5, "planning next steps", ["decision making"])
    
    # AGENT 2: Analyze patterns
    print("\\n2. AGENT 2: Pattern Analyzer")
    patterns = ai.analyze_patterns()
    print(f"   Most common mood: {patterns['most_common_mood']}")
    print(f"   Mood frequency: {patterns['mood_frequency']}")
    print(f"   Common triggers: {patterns['common_triggers']}")
    
    # AGENT 3: Get suggestions
    print("\\n3. AGENT 3: Strategy Suggester")
    strategies = ai.suggest_strategies("anxious", 6)
    print("   Recommended strategies:")
    for i, strategy in enumerate(strategies, 1):
        print(f"   {i}. {strategy['name']}: {strategy['description']}")
    
    print("\\n🎉 SUCCESS! All 3 hackathon agents demonstrated!")
    print("📊 Total emotional states tracked:", len(ai.emotional_history))
    print("🚀 Ready for Jaclang conversion!")

if __name__ == "__main__":
    demo_all_agents()
