from collections import Counter
import re


def consolidate_blocks(blocks_json: list) -> list:
    if not blocks_json:
        return []

    groups = {}
    for b in blocks_json:
        domain = b.get("domain", "unknown")
        tags = tuple(sorted(b.get("tags", [])))
        key = (domain, tags)
        groups.setdefault(key, []).append(b)

    results = []
    for (domain, tags), group in groups.items():
        if len(group) < 2:
            continue

        all_content = [b.get("content", "") for b in group]
        words = [
            w
            for c in all_content
            for w in re.findall(r"\w+", c.lower())
            if len(w) > 3
        ]
        common_words = [w for w, _ in Counter(words).most_common(5)]

        registers = [b.get("register", "") for b in group]
        common_register = Counter(registers).most_common(1)[0][0] if registers else "SENSE"

        generalization = {
            "type": "consolidation",
            "domain": domain,
            "tags": list(tags),
            "source_count": len(group),
            "common_terms": common_words,
            "generalized_claim": (
                f"Across {len(group)} blocks in {domain}, "
                f"recurring themes: {', '.join(common_words)}."
            ),
            "register": "FACT" if common_register else "SENSE",
        }
        results.append(generalization)

    return results
