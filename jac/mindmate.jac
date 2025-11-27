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

walker init {
    has input_mood = "happy";
    has input_situation = "testing";
    
    with entry {
        // Create emotional state directly in init walker
        new_emotion = spawn here ++> node::emotional_state;
        new_emotion.timestamp = std.time_now();
        new_emotion.mood_rating = input_mood;
        new_emotion.situation = input_situation;
        
        std.out("MindMate Emotional Tracking Graph initialized! 🧠");
        report "Created emotional state: " + input_mood;
    }
}
