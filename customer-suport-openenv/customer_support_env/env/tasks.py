TASKS = [
    {
        "id": 1,
        "type": "password_reset",
        "difficulty": "easy",
        "text": "I forgot my password, help me login",
        "hidden_tool": "send_reset_link",
        "optimal_steps": 4,
        "sentiment": "neutral"
    },
    {
        "id": 2,
        "type": "refund",
        "difficulty": "medium",
        "text": "I want a refund for order #123",
        "hidden_tool": "refund_api",
        "optimal_steps": 5,
        "sentiment": "slightly_negative"
    },
    {
        "id": 3,
        "type": "multi_issue",
        "difficulty": "hard",
        "text": "I was charged twice and my order is late!",
        "hidden_tool": "check_order_status",
        "optimal_steps": 7,
        "sentiment": "angry"
    },
    {
        "id": 4,
        "type": "fraud",
        "difficulty": "hard",
        "text": "Unauthorized transaction detected!",
        "requires_escalation": True,
        "optimal_steps": 6,
        "sentiment": "angry"
    }
]