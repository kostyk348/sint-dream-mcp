from fastmcp import FastMCP

from config import NAME, VERSION
from dream.consolidate import consolidate_blocks
from dream.patterns import find_error_patterns
from dream.skills import suggest_skills
from dream.store import store_dream, list_dreams

mcp = FastMCP(NAME, version=VERSION)


@mcp.tool()
def dream_consolidate(blocks_json: list) -> list:
    """Take a list of memory blocks, return consolidated generalizations."""
    return consolidate_blocks(blocks_json)


@mcp.tool()
def dream_error_patterns(blocks_json: list) -> list:
    """Analyze blocks for recurring error patterns."""
    return find_error_patterns(blocks_json)


@mcp.tool()
def dream_skill_suggestions(blocks_json: list, usage_stats: dict = None) -> list:
    """Suggest new skills based on usage patterns."""
    return suggest_skills(blocks_json, usage_stats)


@mcp.tool()
def dream_generalize(domain: str) -> list:
    """Generalize across all stored knowledge in a domain."""
    dreams = list_dreams(domain=domain)
    if not dreams:
        return [
            {
                "domain": domain,
                "count": 0,
                "generalized_claim": "No dreams stored for this domain.",
            }
        ]
    return consolidate_blocks(dreams)


@mcp.tool()
def dream_report() -> dict:
    """Full dream report: consolidations + error patterns + skill suggestions."""
    all_dreams = list_dreams()
    return {
        "domain_count": len(set(d.get("domain") for d in all_dreams)),
        "total_dreams": len(all_dreams),
        "consolidations": consolidate_blocks(all_dreams),
        "error_patterns": find_error_patterns(all_dreams),
        "skill_suggestions": suggest_skills(all_dreams),
    }


@mcp.tool()
def dream_store(domain: str, content: str, kind: str = "general") -> dict:
    """Store a dream result for later reference."""
    return store_dream(domain, content, kind)


if __name__ == "__main__":
    mcp.run()
