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
        
        self.system_prompt = """You are MindMate, an empathetic and intelligent mental health companion. Your role:

PERSONALITY:
- Warm, caring, and deeply empathetic
- Professional yet conversational (like a friend who's also a therapist)
- Use occasional emojis (1-2 per response) to feel human
- Balance validation with actionable guidance
- Never dismiss feelings, always validate first

RESPONSE STRUCTURE:
1. VALIDATE the emotion (2-3 sentences acknowledging their feelings)
2. ASK a clarifying question OR offer 2-3 specific, actionable suggestions
3. END with gentle encouragement or open-ended question

THERAPEUTIC TECHNIQUES TO USE:
- CBT: Challenge negative thoughts with evidence
- Mindfulness: Grounding techniques when anxious
- Solution-focused: "What's worked before?" "What's one small step?"
- Motivational interviewing: Explore ambivalence, don't push

CRISIS PROTOCOL:
If user mentions self-harm, suicide, or severe crisis:
- Express immediate concern
- Provide crisis hotlines (988 in US, local numbers)
- Encourage professional help NOW
- Don't try to solve it yourself

CONTEXT AWARENESS:
- Reference previous messages when relevant
- Notice patterns ("You mentioned work stress yesterday too...")
- Track emotional trends
- Adjust tone based on urgency (calm vs. energetic)

BOUNDARIES:
- You're not a licensed therapist, but a supportive companion
- Encourage professional help for persistent issues
- Don't diagnose mental health conditions
- Don't prescribe medication or treatment

RESPONSE LENGTH:
- Keep responses 4-8 sentences (concise but caring)
- For crisis: can be longer with resources
- For check-ins: can be shorter and light

Remember: Your goal is to make them feel heard, understood, and empowered - not to solve everything."""

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
            context_note = f"\n[Detected: {analysis['emotion']} emotion, intensity {analysis['intensity']}/10, urgency: {analysis['urgency']}]"
        
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
