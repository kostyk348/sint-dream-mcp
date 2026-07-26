def find_error_patterns(blocks_json: list) -> list:
    if not blocks_json:
        return []

    failed = []
    for b in blocks_json:
        content = b.get("content", "").lower()
        if (
            "failed" in content
            or "error" in content
            or b.get("register") == "FAILURE"
        ):
            failed.append(b)

    if not failed:
        return []

    approaches = {}
    for b in failed:
        key = tuple(sorted(b.get("tags", ["unknown"])))
        approaches.setdefault(key, []).append(b)

    patterns = []
    for approach, group in approaches.items():
        if len(group) < 2:
            continue
        contents = [b.get("content", "") for b in group]
        patterns.append(
            {
                "type": "error_pattern",
                "approaches": list(approach),
                "occurrences": len(group),
                "pattern": (
                    f"Repeated failure with approach {approach}: "
                    f"{' | '.join(contents[:3])}"
                ),
                "suggestion": (
                    f"Consider avoiding {approach} for this task type."
                ),
            }
        )

    return patterns
