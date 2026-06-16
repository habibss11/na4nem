from difflib import SequenceMatcher
import os

WEIGHTS = {
    "relevance": float(os.getenv("US_SELECTOR_W_RELEVANCE", 0.5)),
    "source_coverage": float(os.getenv("US_SELECTOR_W_SOURCE", 0.2)),
    "numeric_consistency": float(os.getenv("US_SELECTOR_W_NUM", 0.2)),
    "conciseness": float(os.getenv("US_SELECTOR_W_CONCISE", 0.05)),
    "cost": float(os.getenv("US_SELECTOR_W_COST", -0.05)),
}


def str_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def numeric_consistency_check(answer: str, query: str) -> float:
    import re
    def parse_nums(s):
        raw = re.findall(r"\d+[\.,]?\d*", s)
        nums = []
        for r in raw:
            try:
                nums.append(float(r.replace(',', '.')))
            except Exception:
                continue
        return nums

    nums_ans = parse_nums(answer)
    nums_q = parse_nums(query)
    if not nums_q:
        return 1.0
    if not nums_ans:
        return 0.0
    # compare element-wise up to length
    pairs = list(zip(nums_ans, nums_q))
    if not pairs:
        return 0.0
    diffs = [abs(a - b) for a, b in pairs]
    avg_rel = sum(1.0 / (1.0 + d) for d in diffs) / len(diffs)
    return max(0.0, min(1.0, avg_rel))


def score_candidate(candidate: str, query: str, docs: list, token_cost: float = 0.0) -> float:
    rels = [str_similarity(candidate, d.get("text", "")) for d in docs]
    relevance = max(rels) if rels else 0.0
    sources = [d.get("source") for d in docs]
    coverage = sum(1 for s in sources if s and s.lower() in candidate.lower()) / max(1, len(sources))
    numeric = numeric_consistency_check(candidate, query)
    conciseness = 1.0 / (1.0 + len(candidate.split()))
    cost_penalty = token_cost
    score = (
        WEIGHTS["relevance"] * relevance
        + WEIGHTS["source_coverage"] * coverage
        + WEIGHTS["numeric_consistency"] * numeric
        + WEIGHTS["conciseness"] * conciseness
        + WEIGHTS["cost"] * cost_penalty
    )
    return score


def select_best(candidates: list, query: str, docs: list):
    scored = []
    for c in candidates:
        if not c:
            continue
        # token_cost approximated by length/1000
        token_cost = len(c.split()) / 1000.0
        s = score_candidate(c, query, docs, token_cost=token_cost)
        scored.append((s, c))
    if not scored:
        return None, None
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0]
