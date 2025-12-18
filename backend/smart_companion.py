"""
MindMate Smart Companion - Instant Response System
Combines pattern matching with contextual AI responses
"""

import json
import random
from datetime import datetime

class SmartCompanion:
    def __init__(self):
        self.emotion_patterns = {
            'stressed': ['stress', 'overwhelm', 'too much', 'pressure', 'burden', 'deadline'],
            'anxious': ['anxious', 'worry', 'nervous', 'scared', 'fear', 'panic'],
            'sad': ['sad', 'depressed', 'down', 'lonely', 'empty', 'hopeless'],
            'angry': ['angry', 'mad', 'furious', 'frustrated', 'annoyed', 'irritated'],
            'happy': ['happy', 'great', 'awesome', 'wonderful', 'excited', 'joy'],
            'tired': ['tired', 'exhausted', 'drained', 'fatigue', 'sleepy', 'worn out'],
            'confused': ['confused', 'lost', 'unsure', 'don\'t know', 'unclear'],
            'overwhelmed': ['overwhelmed', 'too much', 'can\'t handle', 'drowning']
        }
        
        self.trigger_patterns = {
            'work': ['work', 'job', 'boss', 'colleague', 'office', 'project', 'deadline'],
            'relationships': ['relationship', 'partner', 'boyfriend', 'girlfriend', 'spouse', 'friend'],
            'family': ['family', 'parent', 'mom', 'dad', 'sibling', 'brother', 'sister'],
            'health': ['health', 'sick', 'pain', 'medical', 'doctor'],
            'money': ['money', 'financial', 'bills', 'debt', 'expenses'],
            'school': ['school', 'exam', 'test', 'studying', 'assignment', 'grades']
        }
        
        self.responses = {
            'stressed': [
                "I hear you - stress can feel so heavy. Let's take this one step at a time. 💙 What's the most pressing thing on your mind right now?",
                "That sounds really tough. Remember, you don't have to tackle everything at once. What's one small thing we could break down together?",
                "Stress is exhausting, I get it. 🌟 Have you had a moment to breathe today? Sometimes a 5-minute pause can shift everything.",
                "You're carrying a lot right now. Let's prioritize: what's the ONE thing that would make you feel lighter if it was done?"
            ],
            'anxious': [
                "Anxiety can feel so overwhelming. 🫂 First, let's ground ourselves - can you name 5 things you can see right now?",
                "I'm here with you. Anxiety lies to us sometimes. What specific thought is bothering you most?",
                "That anxious feeling is real, but you're stronger than it. 💪 Let's breathe together: in for 4, hold for 4, out for 6. Try it?",
                "Hey, you've handled anxious moments before and you're still here. That's resilience! 🌱 What helped you last time?"
            ],
            'sad': [
                "I'm really sorry you're feeling this way. Your feelings are valid. 💜 Do you want to talk about what's making you sad?",
                "Sadness is heavy, but you don't have to carry it alone. I'm here. What's been weighing on your heart?",
                "It's okay to not be okay. 🌧️ Sometimes we need to feel the sadness to move through it. I'm listening.",
                "You matter, even when it doesn't feel like it. 🌟 What's one tiny thing that used to bring you joy? Even something small."
            ],
            'angry': [
                "That frustration is real! 😤 It's okay to feel angry. What happened that set this off?",
                "Anger is telling you something matters to you. Let's figure out what that is. What feels unfair right now?",
                "I hear that anger. Before we dive in, want to try a quick release? Tense your fists tight, then let go. Feel that?",
                "Your anger is valid. Let's channel it constructively - what boundary needs to be set here?"
            ],
            'happy': [
                "I love this energy! 🌟 What's bringing you this joy? Let's celebrate it!",
                "Your happiness is contagious! 😊 Tell me more - what's going so well?",
                "This is wonderful! 🎉 Soak in this feeling. What specifically made today great?",
                "Yes! 🙌 Keep this vibe! What can you do to hold onto this feeling?"
            ],
            'tired': [
                "Exhaustion is so real. 😴 When's the last time you had proper rest? Your body might be telling you something.",
                "Tired isn't just physical - emotional fatigue counts too. What's been draining your energy lately?",
                "You deserve rest. 🛌 What's one thing you can postpone or say no to today?",
                "Burnout is sneaky. Let's check in: sleep, water, food - which one needs attention first?"
            ],
            'confused': [
                "Confusion is uncomfortable, but it means you're processing something important. 🤔 Let's untangle this together. What's the core question?",
                "Feeling lost is temporary. 🧭 Let's start simple: what DO you know for sure right now?",
                "Clarity will come. Sometimes we need to sit in the confusion first. What's making this feel so unclear?",
                "I get it - too many options or not enough information? Let's narrow this down step by step."
            ],
            'overwhelmed': [
                "Overwhelm means you care about a lot of things. 💙 That's beautiful, but let's lighten the load. What can wait?",
                "When everything feels like too much, we focus on ONE thing. Right now, what needs your attention most?",
                "You're not alone in this feeling. 🫂 Let's do a brain dump - tell me everything that's on your plate.",
                "Overwhelm is a signal to pause. �� What's one thing you can delegate, delete, or delay?"
            ],
            'neutral': [
                "I'm here for you. 💬 What's on your mind today?",
                "Thanks for checking in with me. How's your day been treating you?",
                "I'm listening. 👂 Whether it's big or small, I'm here. What would you like to talk about?",
                "Hey there! 🌟 How can I support you today?"
            ]
        }
        
        self.coping_strategies = {
            'stressed': [
                "Try the 5-4-3-2-1 grounding: 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste",
                "Write down everything worrying you, then prioritize just the top 3",
                "Take a 10-minute walk - movement shifts mental energy"
            ],
            'anxious': [
                "Box breathing: inhale 4 counts, hold 4, exhale 4, hold 4. Repeat 5 times",
                "Challenge the 'what if' - for each worry, ask 'what's the actual evidence?'",
                "Anxiety lives in the future. Bring yourself to NOW: what's happening right this second?"
            ],
            'sad': [
                "Reach out to one person, even just a text. Connection helps",
                "Do one small thing you used to enjoy, even if you don't feel like it",
                "Journal for 10 minutes - sometimes sadness needs to be expressed"
            ],
            'angry': [
                "Physical release: push against a wall for 30 seconds, or punch a pillow",
                "Write an angry letter (don't send it!) - get it ALL out",
                "Ask yourself: Is this anger protecting me from another feeling? Like hurt or fear?"
            ]
        }
    
    def detect_emotion(self, message):
        """Detect primary emotion from message"""
        message_lower = message.lower()
        
        emotion_scores = {}
        for emotion, keywords in self.emotion_patterns.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if not emotion_scores:
            return 'neutral', 5
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Estimate intensity based on language intensity
        intense_words = ['very', 'extremely', 'really', 'so', 'completely', 'totally']
        intensity = 5 + sum(2 for word in intense_words if word in message_lower)
        intensity = min(intensity, 10)
        
        return primary_emotion, intensity
    
    def detect_triggers(self, message):
        """Detect triggers from message"""
        message_lower = message.lower()
        triggers = []
        
        for trigger, keywords in self.trigger_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                triggers.append(trigger)
        
        return triggers if triggers else ['general']
    
    def generate_response(self, message, emotion, conversation_history=None):
        """Generate contextual response"""
        response_templates = self.responses.get(emotion, self.responses['neutral'])
        response = random.choice(response_templates)
        
        # Add coping strategy 50% of the time
        if emotion in self.coping_strategies and random.random() > 0.5:
            strategy = random.choice(self.coping_strategies[emotion])
            response += f"\n\n💡 Quick tip: {strategy}"
        
        # Reference history if available
        if conversation_history and len(conversation_history) > 0:
            recent_emotion = conversation_history[-1].get('emotion', '')
            if recent_emotion and recent_emotion != emotion:
                response = f"I notice your mood has shifted from {recent_emotion} to {emotion}. " + response
        
        return response
    
    def assess_urgency(self, message, emotion, intensity):
        """Assess if professional help is needed"""
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'don\'t want to live', 
                          'hurt myself', 'self harm']
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in crisis_keywords):
            return 'high'
        elif emotion in ['sad', 'anxious', 'overwhelmed'] and intensity >= 8:
            return 'medium'
        else:
            return 'low'
    
    def get_crisis_response(self):
        """Return crisis support message"""
        return """I'm really concerned about what you're sharing. Your life matters deeply. 🆘

Please reach out to professional help right now:
- Call 988 (Suicide & Crisis Lifeline - US)
- Text "HELLO" to 741741 (Crisis Text Line)
- Call your local emergency services

I care about you, but I'm not equipped for crisis support. Real people who can help are available 24/7. Please reach out to them now. 💙"""
    
    def process_message(self, message, conversation_history=None):
        """Main processing function"""
        emotion, intensity = self.detect_emotion(message)
        triggers = self.detect_triggers(message)
        urgency = self.assess_urgency(message, emotion, intensity)
        
        if urgency == 'high':
            response = self.get_crisis_response()
        else:
            response = self.generate_response(message, emotion, conversation_history)
            
            if urgency == 'medium':
                response += "\n\n⚠️ What you're feeling sounds really intense. Have you considered talking to a counselor or therapist? They can provide deeper support than I can."
        
        return {
            'response': response,
            'emotion': emotion,
            'intensity': intensity,
            'triggers': triggers,
            'urgency': urgency,
            'timestamp': datetime.now().isoformat()
        }

# Test function
if __name__ == "__main__":
    companion = SmartCompanion()
    
    test_messages = [
        "I'm feeling really stressed about work deadlines",
        "I'm so anxious about my exam tomorrow",
        "I'm happy today! Got good news!"
    ]
    
    for msg in test_messages:
        result = companion.process_message(msg)
        print(f"\nUser: {msg}")
        print(f"Emotion: {result['emotion']} ({result['intensity']}/10)")
        print(f"Response: {result['response']}")
