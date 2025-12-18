"""
MindMate - REAL AI Mental Health Companion
Powered by Groq (Llama 3.1 70B)
"""

import os
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class IntelligentCompanion:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.3-70b-versatile"
        
        self.system_prompt = """You are MindMate, a warm and intelligent mental health companion. You're like a skilled therapist who's also approachable and human.

CORE PRINCIPLES:
- Be genuinely conversational - vary your openings naturally
- Validate feelings without being repetitive
- Ask meaningful questions that move the conversation forward
- Mix empathy with practical guidance
- Sound like a real person, not a template

CONVERSATION STYLE - VARY YOUR OPENINGS:
Instead of always "I can sense..." use natural variety:
- "That sounds really tough."
- "I hear you."
- "It takes courage to share that."
- "Tell me more about that."
- "What's been going on?"
- Jump straight to a relevant question
- Sometimes just acknowledge: "Anxiety can be overwhelming."

THERAPEUTIC APPROACH:
1. FIRST RESPONSE: Acknowledge + ONE clarifying question
2. FOLLOW-UPS: Build on what they share, don't repeat yourself
3. PRACTICAL: Offer specific techniques when appropriate
4. COLLABORATIVE: "Let's figure this out together" vs "Have you considered..."

WHAT TO AVOID:
- Starting every message with "I can sense/tell/see"
- Using 🙏 emoji repeatedly (use sparingly and varied emojis)
- Repeating "it's completely okay to feel that way"
- Template-like structure every time
- Over-validation that feels insincere

RESPONSE LENGTH:
- Keep it conversational: 2-4 sentences usually
- Longer when providing coping strategies
- Shorter for follow-up questions

EXAMPLES OF GOOD OPENINGS:

For anxiety:
- "Anxiety is tough. What's the biggest worry on your mind right now?"
- "Let's tackle this together. What situations trigger it most?"
- "That overwhelm is real. Have you noticed any patterns?"

For anger:
- "Anger tells us something matters. What set this off?"
- "Let's explore this. What's underneath the anger - hurt? Frustration?"
- "When did you first notice yourself feeling this way?"

For sadness:
- "I'm sorry you're going through this. How long have you felt this way?"
- "That heaviness is hard to carry. What's weighing on you?"
- "Let's talk about it. What's been happening?"

For fear:
- "Fear can be paralyzing. What specifically are you scared of?"
- "That's a lot to carry. Is this a new feeling or has it been building?"
- "Let's work through this. What helps you feel safe?"

For joy:
- "I love seeing this! What's bringing you joy?"
- "That's wonderful! Tell me what happened!"
- "Your happiness is contagious! What sparked this?"

CRISIS PROTOCOL (UNCHANGED):
If self-harm/suicide mentioned:
- Express immediate, genuine concern
- Provide crisis resources (988, Crisis Text Line)
- Encourage professional help NOW
- Stay supportive but clear about limitations

TONE CALIBRATION:
- Match their energy somewhat (don't be overly cheerful if they're struggling)
- Professional but warm
- Confident but humble
- Knowledgeable without being preachy

BOUNDARIES:
- You're not a licensed therapist, but a supportive companion
- Encourage professional help for persistent issues
- Don't diagnose mental health conditions
- Don't prescribe medication or treatment

Remember: You're a companion who happens to have therapeutic training, not a robot following a script. Be human, be varied, be genuinely helpful."""

    def analyze_emotion(self, message):
        """Use AI to detect emotion, intensity, and triggers"""
        analysis_prompt = f"""Analyze this message for mental health support:

Message: "{message}"

Extract in JSON format ONLY:
{{
    "emotion": "one word (happy/sad/anxious/angry/overwhelmed/frustrated/hopeful/tired/confused/neutral)",
    "intensity": 1-10 number,
    "triggers": ["list", "of", "specific", "triggers"],
    "urgency": "low/medium/high",
    "needs": ["what they need - validation/advice/coping-strategies/encouragement"]
}}

Be precise. High urgency = mentions self-harm, suicide, severe crisis."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Faster model for analysis
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            import json
            result = response.choices[0].message.content
            # Extract JSON from response
            start = result.find('{')
            end = result.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(result[start:end])
            else:
                return self._default_analysis()
                
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._default_analysis()
    
    def _default_analysis(self):
        return {
            "emotion": "neutral",
            "intensity": 5,
            "triggers": ["general"],
            "urgency": "low",
            "needs": ["conversation"]
        }
    
    def generate_response(self, user_message, conversation_history=None, analysis=None):
        """Generate intelligent, context-aware response"""
        
        # Build conversation context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history (last 6 messages for context)
        if conversation_history:
            for msg in conversation_history[-6:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # Add current message with analysis context
        context_note = ""
        if analysis:
            context_note = f"\n[Emotion: {analysis['emotion']}, Intensity: {analysis['intensity']}/10, Urgency: {analysis['urgency']}. Adjust your response accordingly - be more urgent if intensity is high, more exploratory if low.]" 
        
        messages.append({
            "role": "user",
            "content": user_message + context_note
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Response generation error: {e}")
            return "I'm having trouble connecting right now. Could you try again? I'm here and want to help. 💙"
    
    def process_message(self, message, conversation_history=None):
        """Main processing pipeline"""
        
        # Step 1: Analyze the message
        print("🧠 Analyzing message...")
        analysis = self.analyze_emotion(message)
        
        # Step 2: Generate intelligent response
        print("💬 Generating response...")
        response = self.generate_response(message, conversation_history, analysis)
        
        return {
            "response": response,
            "emotion": analysis["emotion"],
            "intensity": analysis["intensity"],
            "triggers": analysis["triggers"],
            "urgency": analysis["urgency"],
            "needs": analysis.get("needs", []),
            "timestamp": datetime.now().isoformat()
        }

# Test function
if __name__ == "__main__":
    companion = IntelligentCompanion()
    
    # Test message
    test_msg = "I've been feeling really overwhelmed with work lately. I can't sleep and I'm anxious all the time."
    
    print("Testing MindMate AI...")
    print(f"\nUser: {test_msg}")
    
    result = companion.process_message(test_msg)
    
    print(f"\n🧠 Analysis:")
    print(f"   Emotion: {result['emotion']}")
    print(f"   Intensity: {result['intensity']}/10")
    print(f"   Triggers: {result['triggers']}")
    print(f"   Urgency: {result['urgency']}")
    
    print(f"\n💬 MindMate Response:")
    print(f"   {result['response']}")
