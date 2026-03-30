TASKS = [
    {
        "id": 1,
        "difficulty": "easy",
        "text": "Reset my password",
        "requires_tool": True,
        "optimal_steps": 4,
        "sentiment": "neutral"
    },
    {
        "id": 2,
        "difficulty": "medium",
        "text": "Refund my order #123, I didn't like the product",
        "requires_tool": True,
        "optimal_steps": 5,
        "sentiment": "slightly_negative"
    },
    {
        "id": 3,
        "difficulty": "hard",
        "text": "I was charged twice, order #456 is late and I'm very frustrated!",
        "requires_tool": True,
        "multi_issue": True,
        "optimal_steps": 7,
        "sentiment": "angry"
    }
]