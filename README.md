# System Design Quiz MCP Server

Practice system design interview questions directly from your AI assistant. Generate quiz questions across 7 topics, get rubric-based answer evaluation, and level up your system design skills.

## Tools

| Tool | Description |
|------|-------------|
| `generate_question` | Get a system design question (MCQ or open-ended), filtered by topic, difficulty, or type |
| `evaluate_answer` | Score your open-ended answer (1-10) with rubric-based feedback and improvement suggestions |
| `get_topics` | Browse all available topics with question counts and study recommendations |

## Topics (35 questions)

1. **Load Balancing & Scaling** — Round-robin, weighted distribution, connection draining, horizontal vs vertical
2. **Caching Strategies** — Write-through, LRU, cache stampede, fanout-on-write vs fanout-on-read
3. **Database Design & Sharding** — Hash vs range sharding, denormalization, cross-shard operations
4. **Message Queues & Event-Driven** — At-least-once delivery, queue vs topic, backpressure, saga pattern
5. **Microservices & API Design** — API gateway, idempotency, saga pattern, versioning strategies
6. **CAP Theorem & Distributed Systems** — Consistency vs availability, Paxos, hybrid consistency models
7. **Performance & Reliability** — Throughput vs latency, circuit breaker, tail latency, debugging methodology

## Quick Start

### Prerequisites
- Python 3.11+

### Install

```bash
pip install mcp pydantic
```

### Run locally

```bash
git clone https://github.com/214070779/system-design-quiz-mcp.git
cd system-design-quiz-mcp
python3 server.py
```

### Configure in Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "system-design-quiz": {
      "command": "python3",
      "args": ["/path/to/system-design-quiz-mcp/server.py"]
    }
  }
}
```

## Use Cases

- **Interview prep**: "Quiz me on load balancing" → generates MCQ, evaluates your thinking
- **Study sessions**: "Give me a hard question about CAP theorem" → targeted difficulty
- **Answer practice**: "Evaluate my answer to this design question" → rubric-based scoring
- **Topic overview**: "What topics should I study?" → get recommendations

## License

MIT
