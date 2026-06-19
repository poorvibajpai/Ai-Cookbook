def detect_sentiment(message: str) -> str:
    text = message.lower()

    urgent_keywords = [
        "angry",
        "furious",
        "refund now",
        "cancel now",
        "unacceptable",
        "terrible",
        "frustrated",
        "charged twice",
        "charged incorrectly",
        "can't access",
        "cannot access",
        "data loss",
        "security issue",
        "urgent",
    ]

    negative_keywords = [
        "bad",
        "issue",
        "problem",
        "slow",
        "not working",
        "failed",
        "error",
        "upset",
        "annoyed",
    ]

    if any(keyword in text for keyword in urgent_keywords):
        return "urgent"

    if any(keyword in text for keyword in negative_keywords):
        return "frustrated"

    return "neutral"


def should_escalate(message: str, sentiment: str) -> bool:
    text = message.lower()

    escalation_keywords = [
        "charged twice",
        "refund now",
        "security",
        "data loss",
        "locked out",
        "cannot access my account",
        "can't access my account",
        "urgent",
    ]

    return sentiment == "urgent" or any(keyword in text for keyword in escalation_keywords)