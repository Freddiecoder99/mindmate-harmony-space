walker talk_to_mindmate {
    has input_mood = "overwhelmed";

    can byllm.complete;

    report byllm.complete(
        model="openai/gpt-3.5-turbo",
        prompt= "You are a compassionate mental wellbeing companion. A user is feeling '" + input_mood + "'. Please give them one short, friendly coping strategy. Respond in one sentence.",
        temperature=0.7
    );
}