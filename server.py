#!/usr/bin/env python3
'''
MCP Server for System Design Interview Quiz Practice.

Tools:
  generate_question  - Get a system design quiz question (MCQ or open-ended)
  evaluate_answer    - Score an open-ended answer against rubric criteria
  get_topics         - List all available system design topics with question counts
'''

import random
import json
from typing import Optional
from mcp.server.fastmcp import FastMCP

from questions import QUESTIONS
from evaluator import evaluate_answer

mcp = FastMCP("system_design_quiz")

TOPICS = sorted(set(q["topic"] for q in QUESTIONS))
QUESTIONS_BY_TOPIC: dict[str, list] = {}
for q in QUESTIONS:
    QUESTIONS_BY_TOPIC.setdefault(q["topic"], []).append(q)


def _question_to_output(q: dict) -> dict:
    out = {
        "id": q["id"],
        "topic": q["topic"],
        "difficulty": q["difficulty"],
        "type": q["type"],
        "question": q["question"],
        "explanation": q["explanation"],
        "hint": q["hint"],
    }
    if q["type"] == "mcq":
        out["options"] = q["options"]
        out["correct"] = q["correct"]
    return out


@mcp.tool(
    name="generate_question",
    annotations={
        "title": "Generate System Design Quiz Question",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def generate_question(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
) -> str:
    """Generate a system design quiz question, optionally filtered by topic, difficulty, or type.

    Use this tool when:
    - A user wants to practice system design interview questions
    - You need to quiz someone on a specific system design topic
    - You want to test knowledge across all system design areas
    - A user asks "quiz me on [topic]"

    The returned question includes the question text, options (for MCQ), correct answer,
    explanation, hint, and metadata (topic, difficulty).

    For MCQ questions, use the returned question+options to present the quiz.
    For open-ended questions, collect the user's answer and pass it to evaluate_answer.
    """
    pool = QUESTIONS

    if topic:
        if topic not in TOPICS:
            return json.dumps({
                "error": f"Topic '{topic}' not found.",
                "available_topics": TOPICS,
            })
        pool = QUESTIONS_BY_TOPIC[topic]

    if difficulty:
        pool = [q for q in pool if q["difficulty"] == difficulty]

    if question_type:
        pool = [q for q in pool if q["type"] == question_type]

    if not pool:
        return json.dumps({
            "error": "No questions match the specified filters.",
            "try_adjusting": "Remove some filters to broaden the search.",
        })

    chosen = random.choice(pool)
    return json.dumps(_question_to_output(chosen), ensure_ascii=False)


@mcp.tool(
    name="evaluate_answer",
    annotations={
        "title": "Evaluate System Design Answer",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def evaluate_answer_tool(
    question: str,
    user_answer: str,
    topic: str = "System Design",
) -> str:
    """Evaluate a user's answer to an open-ended system design question.

    Use this tool when:
    - A user has answered an open-ended system design question and wants feedback
    - You need to score and provide improvement suggestions
    - The user wants to know how their answer compares to expectations

    The evaluation returns:
    - Score (1-10) with a label (Weak → Excellent)
    - Specific strengths of the answer
    - Actionable improvement suggestions
    - Rubric coverage (how many evaluation criteria were addressed)
    - Analysis metadata (word count, structure quality, trade-off discussion)

    Best results: encourage users to give detailed, structured answers with
    specific technical details and trade-off analysis.
    """
    result = evaluate_answer(question, user_answer, topic)
    return json.dumps(result, ensure_ascii=False)


@mcp.tool(
    name="get_topics",
    annotations={
        "title": "Get System Design Topics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def get_topics() -> str:
    """List all available system design topics with question counts and difficulty breakdowns.

    Use this tool when:
    - A user wants to see what topics are available
    - You need to help a user choose what to study
    - A user asks "what should I study?" or "what topics do you have?"
    - Before calling generate_question to decide which topic to filter by

    The response includes per-topic question counts, difficulty distribution,
    and a study recommendation for users who don't know where to start.
    """
    topic_info = []
    for topic in TOPICS:
        qs = QUESTIONS_BY_TOPIC[topic]
        difficulty_dist = {}
        for q in qs:
            difficulty_dist[q["difficulty"]] = difficulty_dist.get(q["difficulty"], 0) + 1
        mcq_count = sum(1 for q in qs if q["type"] == "mcq")
        open_count = sum(1 for q in qs if q["type"] == "open_ended")
        topic_info.append({
            "topic": topic,
            "total_questions": len(qs),
            "difficulty_breakdown": difficulty_dist,
            "mcq_count": mcq_count,
            "open_ended_count": open_count,
        })

    return json.dumps({
        "topics": topic_info,
        "total_questions": len(QUESTIONS),
        "total_topics": len(TOPICS),
        "study_recommendation": "If you're new to system design, start with Load Balancing & Scaling or Caching Strategies (easier topics). For interview preparation, focus on Database Design, CAP Theorem, and Performance topics.",
    }, ensure_ascii=False)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
