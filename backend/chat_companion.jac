// ============================================
// MINDMATE CHAT COMPANION - FULL AI SYSTEM
// ============================================

import:py from datetime { datetime }
import:py from typing { Dict, List }

// ============================================
// ENHANCED NODE DEFINITIONS
// ============================================

node User {
    has name: str;
    has email: str;
    has joined_date: str;
}

node MoodEntry {
    has entry_id: str;
    has date: str;
    has timestamp: str;
    has mood_score: int;
    has mood_type: str;
    has journal_text: str;
    has triggers: list[str];
}

node ChatMessage {
    has message_id: str;
    has timestamp: str;
    has role: str;  // "user" or "assistant"
    has content: str;
    has detected_emotion: str;
    has detected_intensity: int;
}

node ConversationSession {
    has session_id: str;
    has start_time: str;
    has summary: str;
}

// ============================================
// EDGES
// ============================================

edge has_mood;
edge has_message;
edge has_session;

// ============================================
// WALKER: Initialize User with Chat Support
// ============================================

walker initialize_chat_user {
    has name: str = "User";
    has email: str = "user@mindmate.ai";

    can setup with `root entry {
        user_node = spawn here ++> User(
            name = self.name,
            email = self.email,
            joined_date = str(datetime.now().date())
        );
        
        report {
            "status": "success",
            "message": "Chat-enabled user initialized",
            "user": user_node
        };
    }
}

// ============================================
// byLLM WALKER: AI Chat Companion
// ============================================

walker:byLLM chat_companion {
    has user_message: str;
    has conversation_history: list = [];
    has user_mood_history: list = [];
    
    can respond with `root entry {
        '''
        You are MindMate, a warm, empathetic AI mental wellness companion. Your personality:
        
        Core Traits:
        - Deeply empathetic and validating
        - Occasionally humorous but never dismissive
        - Conversational and natural (like texting a friend)
        - Professional knowledge but casual tone
        - Uses emojis thoughtfully (1-2 per message)
        
        📋 Your Conversation Style:
        - Start with validation ("I hear you", "That makes sense")
        - Ask thoughtful follow-up questions
        - Offer 1-2 concrete, actionable suggestions
        - Reference past conversations when relevant
        - End with encouragement or a gentle question
        - Keep responses 3-5 sentences (concise but caring)
        
        🚫 Never:
        - Be overly formal or clinical
        - Give multiple-choice responses
        - Use bullet points unless specifically asked
        - Provide medical diagnoses
        - Be dismissive of feelings
        
        📊 Context:
        User's message: {self.user_message}
        Recent conversation: {self.conversation_history[-3:] if self.conversation_history else "First message"}
        User's mood pattern: {self.user_mood_history[-2:] if self.user_mood_history else "No history yet"}
        
        Respond naturally and supportively. If they seem in crisis, gently suggest professional help.
        '''
        
        report {
            "assistant_message": response,
            "timestamp": str(datetime.now())
        };
    }
}

// ============================================
// byLLM WALKER: Emotion Analyzer
// ============================================

walker:byLLM analyze_message_emotion {
    has user_message: str;
    
    can analyze with `root entry {
        '''
        Analyze this message for emotional content. Be a skilled emotional intelligence expert.
        
        Message: "{self.user_message}"
        
        Extract:
        1. Primary emotion (choose ONE: happy, sad, anxious, angry, overwhelmed, calm, excited, frustrated, hopeful, neutral)
        2. Intensity (1-10 scale, where 1=very mild, 10=extremely intense)
        3. Triggers mentioned (list of specific things: work, relationships, health, money, family, etc.)
        4. Urgency (low/medium/high - is this person in immediate distress?)
        
        Respond ONLY in JSON:
        {
            "emotion": "emotion_name",
            "intensity": 7,
            "triggers": ["trigger1", "trigger2"],
            "urgency": "low",
            "reasoning": "Brief explanation"
        }
        '''
        
        report analysis_result;
    }
}

// ============================================
// WALKER: Save Chat Message
// ============================================

walker save_chat_message {
    has user_message: str;
    has assistant_response: str;
    has detected_emotion: str;
    has detected_intensity: int;
    has triggers: list;
    
    can save with User entry {
        import:py uuid;
        
        # Save user message
        user_msg = spawn here ++> ChatMessage(
            message_id = str(uuid.uuid4())[:8],
            timestamp = str(datetime.now()),
            role = "user",
            content = self.user_message,
            detected_emotion = self.detected_emotion,
            detected_intensity = self.detected_intensity
        );
        
        # Save assistant response
        assistant_msg = spawn here ++> ChatMessage(
            message_id = str(uuid.uuid4())[:8],
            timestamp = str(datetime.now()),
            role = "assistant",
            content = self.assistant_response,
            detected_emotion = "",
            detected_intensity = 0
        );
        
        # Create mood entry if emotion detected
        if self.detected_emotion != "neutral" {
            mood_entry = spawn here ++> MoodEntry(
                entry_id = str(uuid.uuid4())[:8],
                date = str(datetime.now().date()),
                timestamp = str(datetime.now()),
                mood_score = self.detected_intensity,
                mood_type = self.detected_emotion,
                journal_text = self.user_message,
                triggers = self.triggers
            );
        }
        
        report {
            "status": "success",
            "message": "Chat saved and mood logged"
        };
    }
}

// ============================================
// WALKER: Get Conversation History
// ============================================

walker get_chat_history {
    has limit: int = 20;
    
    can retrieve with User entry {
        messages = -[has_message]-> (`?ChatMessage);
        
        # Sort by timestamp and limit
        sorted_messages = sorted(messages, key=lambda x: x.timestamp)[-self.limit:];
        
        history = [];
        for msg in sorted_messages {
            history.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "emotion": msg.detected_emotion if msg.role == "user" else "",
                "intensity": msg.detected_intensity if msg.role == "user" else 0
            });
        }
        
        report {
            "history": history,
            "total_messages": len(messages)
        };
    }
}

// ============================================
// WALKER: Get Mood Summary from Chats
// ============================================

walker get_mood_summary {
    can summarize with User entry {
        moods = -[has_mood]-> (`?MoodEntry);
        
        if len(moods) == 0 {
            report {
                "average_mood": 0,
                "total_entries": 0,
                "common_emotions": [],
                "common_triggers": []
            };
            return;
        }
        
        # Calculate statistics
        total_score = sum([m.mood_score for m in moods]);
        avg_mood = total_score / len(moods);
        
        # Count emotions
        emotion_counts = {};
        trigger_counts = {};
        
        for mood in moods {
            emotion_counts[mood.mood_type] = emotion_counts.get(mood.mood_type, 0) + 1;
            for trigger in mood.triggers {
                trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1;
            }
        }
        
        # Get top 3
        top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3];
        top_triggers = sorted(trigger_counts.items(), key=lambda x: x[1], reverse=True)[:3];
        
        report {
            "average_mood": round(avg_mood, 1),
            "total_entries": len(moods),
            "common_emotions": [e[0] for e in top_emotions],
            "common_triggers": [t[0] for t in top_triggers],
            "recent_trend": "improving" if moods[-1].mood_score > avg_mood else "stable"
        };
    }
}

// ============================================
// MAIN WALKER: Process Chat Message
// ============================================

walker process_chat {
    has user_message: str;
    
    can handle with User entry {
        analysis = spawn here walker analyze_message_emotion(
            user_message = self.user_message
        );
        
        history = spawn here walker get_chat_history(limit = 10);
        
        mood_summary = spawn here walker get_mood_summary();
        
        ai_response = spawn here walker chat_companion(
            user_message = self.user_message,
            conversation_history = history.get("history", []),
            user_mood_history = [mood_summary]
        );
       
        save_result = spawn here walker save_chat_message(
            user_message = self.user_message,
            assistant_response = ai_response.get("assistant_message", ""),
            detected_emotion = analysis.get("emotion", "neutral"),
            detected_intensity = analysis.get("intensity", 5),
            triggers = analysis.get("triggers", [])
        );
        
        report {
            "user_message": self.user_message,
            "assistant_response": ai_response.get("assistant_message"),
            "detected_emotion": analysis.get("emotion"),
            "detected_intensity": analysis.get("intensity"),
            "triggers": analysis.get("triggers"),
            "urgency": analysis.get("urgency"),
            "mood_summary": mood_summary
        };
    }
}
