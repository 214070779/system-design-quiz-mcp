"""
Answer evaluation for open-ended system design questions.

Uses rubric-based scoring to evaluate open-ended answers
against model answers and topic-specific criteria.
"""

RUBRICS = {
    "Load Balancing & Scaling": [
        "Understanding of trade-offs (not just listing pros)",
        "Mentions concrete algorithms or techniques by name",
        "Considers failure modes and edge cases",
        "Provides rationale for choices (why X over Y)",
    ],
    "Caching Strategies": [
        "Identifies appropriate cache topology (local vs distributed)",
        "Discusses consistency implications",
        "Mentions eviction policies and their trade-offs",
        "Addresses cache invalidation or staleness handling",
    ],
    "Database Design & Sharding": [
        "Shard key selection reasoning",
        "Awareness of cross-shard operation costs",
        "Discusses rebalancing/resharding strategy",
        "Considers read vs write optimization",
    ],
    "Message Queues & Event-Driven Architecture": [
        "Clear distinction between sync and async patterns",
        "Discusses delivery guarantees and idempotency",
        "Addresses failure handling and retry strategies",
        "Considers ordering and partitioning constraints",
    ],
    "Microservices & API Design": [
        "Service boundary reasoning (domain-driven design)",
        "Discusses inter-service communication patterns",
        "Addresses data consistency across services",
        "Considers backward compatibility and versioning",
    ],
    "CAP Theorem & Distributed Systems": [
        "Accurate application of CAP trade-offs",
        "Understanding of consistency models (strong vs eventual)",
        "Knowledge of consensus protocols",
        "Practical design considerations (not just theory)",
    ],
    "Performance & Reliability": [
        "Systematic debugging methodology",
        "Distinguishes between symptoms and root causes",
        "Uses quantitative reasoning (metrics, thresholds)",
        "Proposes concrete, actionable solutions",
    ],
}


def evaluate_answer(question: str, user_answer: str, topic: str) -> dict:
    """Evaluate a user's open-ended answer against rubric criteria.

    Returns a score dict with strengths, weaknesses, and model answer reference.
    """
    word_count = len(user_answer.split())
    question_words = len(question.split())

    is_substantive = word_count >= question_words * 1.5
    has_structure = any(
        marker in user_answer.lower()
        for marker in ["first", "second", "finally", "however", "because", "therefore", "approach", "consider"]
    )
    mentions_tradeoffs = any(
        word in user_answer.lower()
        for word in ["trade-off", "tradeoff", "however", "but", "instead", "alternative", "depends"]
    )

    rubric = RUBRICS.get(topic, [])
    rubric_hits = sum(1 for criterion in rubric if _criterion_match(user_answer, criterion))

    score = 4
    if is_substantive:
        score += 1
    if has_structure:
        score += 1
    if mentions_tradeoffs:
        score += 1
    if rubric_hits >= len(rubric) * 0.75:
        score += 2
    elif rubric_hits >= len(rubric) * 0.5:
        score += 1
    score = max(1, min(10, score))

    strengths = []
    if is_substantive:
        strengths.append("Answer provides sufficient depth and detail")
    if has_structure:
        strengths.append("Well-organized response with clear reasoning flow")
    if mentions_tradeoffs:
        strengths.append("Demonstrates awareness of trade-offs and alternatives")
    if rubric_hits > 0:
        covered = _covered_criteria(rubric, user_answer)
        for c in covered[:2]:
            strengths.append(f"Covers: {c}")
    if not strengths:
        strengths.append("Answer addresses the core question")

    improvements = []
    if not is_substantive:
        improvements.append("Expand your answer with more specific details and examples")
    if not has_structure:
        improvements.append("Structure your response with a clear beginning, middle, and conclusion")
    if not mentions_tradeoffs:
        improvements.append("Discuss trade-offs and why you chose one approach over alternatives")
    uncovered = _uncovered_criteria(rubric, user_answer)
    for c in uncovered[:2]:
        improvements.append(f"Consider addressing: {c}")

    return {
        "score": score,
        "score_label": _score_label(score),
        "strengths": strengths,
        "improvements": improvements,
        "rubric_coverage": f"{rubric_hits}/{len(rubric)} criteria addressed",
        "analysis": {
            "word_count": word_count,
            "substantive": is_substantive,
            "structured": has_structure,
            "tradeoffs_discussed": mentions_tradeoffs,
        },
    }


def _criterion_match(user_answer: str, criterion: str) -> bool:
    keywords = {
        "Understanding of trade-offs": ["trade-off", "tradeoff", "pros", "cons", "but", "however", "vs", "versus"],
        "Mentions concrete algorithms": ["algorithm", "round-robin", "consistent hash", "paxos", "raft", "gossip", "quorum", "lease"],
        "Considers failure modes": ["fail", "crash", "timeout", "retry", "circuit break", "degrad", "fallback", "dead"],
        "Shard key selection": ["shard key", "partition key", "hash", "range", "hotspot", "distrib"],
        "Delivery guarantees": ["at-least-once", "exactly-once", "at-most-once", "delivery", "ack"],
        "Consensus protocols": ["paxos", "raft", "zab", "consensus", "quorum", "leader election"],
        "Consistency models": ["strong consistency", "eventual consistency", "causal", "linearizab"],
        "Backward compatibility": ["backward compat", "version", "deprecat", "migration", "sunset"],
    }
    for keyword_phrase, triggers in keywords.items():
        if keyword_phrase in criterion:
            return any(t in user_answer.lower() for t in triggers)
    criterion_words = set(criterion.lower().split())
    answer_words = set(user_answer.lower().split())
    common = criterion_words & answer_words
    return len(common) >= len(criterion_words) * 0.3


def _covered_criteria(rubric, user_answer):
    return [c for c in rubric if _criterion_match(user_answer, c)]


def _uncovered_criteria(rubric, user_answer):
    return [c for c in rubric if not _criterion_match(user_answer, c)]


def _score_label(score: int) -> str:
    if score >= 9:
        return "Excellent"
    elif score >= 7:
        return "Good"
    elif score >= 5:
        return "Fair"
    elif score >= 3:
        return "Needs Improvement"
    else:
        return "Weak"
