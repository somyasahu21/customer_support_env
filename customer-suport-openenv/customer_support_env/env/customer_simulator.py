import random

RESPONSES = {
    "angry": [
        "This is unacceptable!",
        "Why is this taking so long?",
        "I want this fixed NOW!"
    ],
    "neutral": [
        "Okay, please continue.",
        "Can you help me with this?",
        "I’m waiting."
    ],
    "happy": [
        "Thanks, that helps!",
        "Appreciate your support.",
        "That worked!"
    ]
}


def generate_customer_reply(env, action):
    emotion = env.user_emotion

    if action.action_type == "respond":
        if env.customer_satisfaction > 0.8:
            emotion = "happy"
        elif env.customer_satisfaction < 0.5:
            emotion = "angry"

    env.user_emotion = emotion

    return random.choice(RESPONSES[emotion])