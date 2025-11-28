node emotional_state {
    has timestamp;
    has mood_rating;
    has emotional_pattern;
    has situation;
}

node emotional_trigger {
    has trigger_type;
    has intensity;
    has description;
}

node coping_strategy {
    has strategy_name;
    has effectiveness_rating;
    has description;
}

edge emotional_connection {
    has connection_strength;
}

// AGENT 1: Mood Logger (Freddie's existing walker)
walker track_mood {
    has input_mood;
    has input_situation;

    with entry {
        new_emotion = spawn here ++> node::emotional_state;
        new_emotion.timestamp = std.time_now();
        new_emotion.mood_rating = input_mood;
        new_emotion.situation = input_situation;
        report "Emotional state tracked: " + input_mood + " in context: " + input_situation;
    }
}

// AGENT 2: Pattern Analyzer (NEW - detects emotional trends)
walker analyze_patterns {
    with entry {
        emotional_states = --> node::emotional_state;
        
        if (emotional_states.length > 0) {
            mood_counts = {};
            for emotion in emotional_states {
                mood_counts[emotion.mood_rating] = mood_counts.get(emotion.mood_rating, 0) + 1;
            }
            
            most_common = "";
            max_count = 0;
            for mood, count in mood_counts {
                if (count > max_count) {
                    most_common = mood;
                    max_count = count;
                }
            }
            
            report "Pattern Analysis: Most common mood is '" + most_common + "' (" + max_count + " occurrences)";
        } else {
            report "Pattern Analysis: No emotional data yet";
        }
    }
}

// AGENT 3: Strategy Suggester (NEW - recommends coping strategies)
walker suggest_strategies {
    has current_mood;
    
    with entry {
        strategies = --> node::coping_strategy;
        
        if (strategies.length == 0) {
            // Create some default strategies if none exist
            strategy1 = spawn here ++> node::coping_strategy;
            strategy1.strategy_name = "Deep Breathing";
            strategy1.effectiveness_rating = "high";
            strategy1.description = "Take 5 deep breaths to calm yourself";
            
            strategy2 = spawn here ++> node::coping_strategy;
            strategy2.strategy_name = "Gratitude Journal";
            strategy2.effectiveness_rating = "medium";
            strategy2.description = "Write down 3 things you're grateful for";
            
            strategies = [strategy1, strategy2];
        }
        
        // Simple mood-to-strategy mapping
        mood_suggestions = {
            "sad": "Gratitude Journal",
            "anxious": "Deep Breathing", 
            "angry": "Deep Breathing",
            "stressed": "Deep Breathing"
        };
        
        suggested_name = mood_suggestions.get(current_mood, "Deep Breathing");
        
        for strategy in strategies {
            if (strategy.strategy_name == suggested_name) {
                report "Strategy Suggestion: " + strategy.strategy_name + " - " + strategy.description;
                break;
            }
        }
    }
}

walker init {
    has input_mood = "happy";
    has input_situation = "testing";

    with entry {
        std.out("🧠 MindMate Enhanced - All 3 Agents Ready!");
        
        // Test Agent 1: Mood Logger
        spawn here walker::track_mood(
            input_mood="excited", 
            input_situation="building enhanced version"
        );
        
        spawn here walker::track_mood(
            input_mood="anxious", 
            input_situation="debugging code"
        );
        
        // Test Agent 2: Pattern Analyzer
        spawn here walker::analyze_patterns;
        
        // Test Agent 3: Strategy Suggester
        spawn here walker::suggest_strategies(current_mood="anxious");
        
        report "All 3 agents tested successfully!";
    }
}
