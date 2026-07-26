from collections import Counter


def suggest_skills(blocks_json: list, usage_stats: dict = None) -> list:
    if not blocks_json:
        return []

    tool_counts = Counter()
    domain_tools = {}

    for b in blocks_json:
        domain = b.get("domain", "unknown")
        tool = b.get("tool")
        if tool:
            tool_counts[tool] += 1
            domain_tools.setdefault(domain, Counter())[tool] += 1

    if usage_stats:
        for tool, count in usage_stats.items():
            tool_counts[tool] += count

    suggestions = []
    for domain, tools in domain_tools.items():
        for tool, count in tools.items():
            if count >= 5:
                suggestions.append(
                    {
                        "type": "skill_suggestion",
                        "domain": domain,
                        "tool": tool,
                        "usage_count": count,
                        "suggestion": (
                            f"Create a specialized agent for {tool} in "
                            f"{domain} (used {count} times)."
                        ),
                        "reasoning": (
                            f"High usage frequency ({count}x) suggests "
                            "a dedicated skill would improve efficiency."
                        ),
                    }
                )

    if not suggestions:
        top_tools = tool_counts.most_common(3)
        if top_tools:
            suggestions.append(
                {
                    "type": "skill_suggestion",
                    "domain": "general",
                    "tool": top_tools[0][0],
                    "usage_count": top_tools[0][1],
                    "suggestion": (
                        f"Most used tool is {top_tools[0][0]} "
                        f"({top_tools[0][1]} times). "
                        "Consider creating targeted skills."
                    ),
                    "reasoning": (
                        "Tool usage suggests areas for skill optimization."
                    ),
                }
            )

    return suggestions
