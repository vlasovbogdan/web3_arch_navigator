#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class ArchProfile:
    key: str
    name: str
    tagline: str
    description: str
    privacy_focus: float     # 0–1
    soundness_focus: float   # 0–1
    performance_focus: float # 0–1
    complexity: float        # 0–1 (higher = more complex)


PROFILES: Dict[str, ArchProfile] = {
    "aztec": ArchProfile(
        key="aztec",
        name="Aztec-style zk Rollup",
        tagline="Encrypted state + zk circuits on Ethereum.",
        description=(
            "Privacy-first rollup that uses zero-knowledge proofs for "
            "encrypted balances and private smart contracts. Most suitable "
            "when you need on-chain privacy and Ethereum composability."
        ),
        privacy_focus=0.95,
        soundness_focus=0.82,
        performance_focus=0.60,
        complexity=0.78,
    ),
    "zama": ArchProfile(
        key="zama",
        name="Zama-style FHE Compute Stack",
        tagline="Fully homomorphic encrypted compute around Web3 data.",
        description=(
            "FHE-heavy design where application logic and analytics operate "
            "on encrypted data. Useful when you need strong privacy across "
            "off-chain or hybrid compute pipelines."
        ),
        privacy_focus=0.90,
        soundness_focus=0.86,
        performance_focus=0.40,
        complexity=0.88,
    ),
    "soundness": ArchProfile(
        key="soundness",
        name="Soundness-first Protocol Lab",
        tagline="Formally specified and verified Web3 protocols.",
        description=(
            "Design discipline centered on specifications, proofs, and "
            "verified implementations. Best suited when correctness and "
            "long-term maintainability are the primary constraints."
        ),
        privacy_focus=0.55,
        soundness_focus=0.98,
        performance_focus=0.72,
        complexity=0.65,
    ),
}


def score_fit(
    profile: ArchProfile,
    need_privacy: int,
    need_formal: int,
    need_throughput: int,
    tolerance_latency: int,
    team_crypto_experience: int,
) -> Dict[str, Any]:
    """
    All need_* arguments are 0–10 integers.
    """
    p = profile

    def norm(x: float) -> float:
        return max(0.0, min(1.0, x))

    privacy_need = need_privacy / 10.0
    formal_need = need_formal / 10.0
    throughput_need = need_throughput / 10.0
    latency_tolerance = tolerance_latency / 10.0
    crypto_skill = team_crypto_experience / 10.0

    privacy_match = 1.0 - abs(privacy_need - p.privacy_focus)
    soundness_match = 1.0 - abs(formal_need - p.soundness_focus)
    perf_match = 1.0 - abs(throughput_need - p.performance_focus)

    latency_penalty = (1.0 - latency_tolerance) * (p.complexity * 0.5)
    complexity_penalty = max(0.0, p.complexity - crypto_skill)

    raw_score = (
        privacy_match * 0.40
        + soundness_match * 0.30
        + perf_match * 0.30
        - latency_penalty * 0.30
        - complexity_penalty * 0.40
    )

    final_score = norm(raw_score)

    if final_score >= 0.8:
        label = "excellent"
    elif final_score >= 0.65:
        label = "good"
    elif final_score >= 0.5:
        label = "moderate"
    else:
        label = "weak"

    return {
        "profile": p.key,
        "name": p.name,
        "tagline": p.tagline,
        "description": p.description,
        "privacyFocus": round(p.privacy_focus, 3),
        "soundnessFocus": round(p.soundness_focus, 3),
        "performanceFocus": round(p.performance_focus, 3),
        "complexity": round(p.complexity, 3),
        "privacyNeed": need_privacy,
        "formalNeed": need_formal,
        "throughputNeed": need_throughput,
        "latencyTolerance": tolerance_latency,
        "cryptoExperience": team_crypto_experience,
        "fitScore": round(final_score, 3),
        "fitLabel": label,
    }


def summarize_recommendation(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    best = max(results, key=lambda r: r["fitScore"])
    sorted_all = sorted(results, key=lambda r: r["fitScore"], reverse=True)
    ranking = [
        {"profile": r["profile"], "name": r["name"], "fitScore": r["fitScore"], "fitLabel": r["fitLabel"]}
        for r in sorted_all
    ]
    summary = {
        "bestProfile": best["profile"],
        "bestName": best["name"],
        "bestFitScore": best["fitScore"],
        "bestFitLabel": best["fitLabel"],
        "ranking": ranking,
    }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="web3_arch_navigator",
        description=(
            "Interactive-style scorer that helps you navigate between Aztec-style zk rollups, "
            "Zama-style FHE stacks, and soundness-first protocol labs based on your constraints."
        ),
    )
    parser.add_argument(
        "--need-privacy",
        type=int,
        default=8,
        help="How strong is your need for privacy? 0–10 (default: 8).",
    )
    parser.add_argument(
        "--need-formal",
        type=int,
        default=7,
        help="How strong is your need for formal verification / proofs? 0–10 (default: 7).",
    )
    parser.add_argument(
        "--need-throughput",
        type=int,
        default=6,
        help="How strong is your need for high throughput? 0–10 (default: 6).",
    )
    parser.add_argument(
        "--latency-tolerance",
        type=int,
        default=5,
        help="Tolerance for higher latency / proving time. 0–10 (default: 5).",
    )
    parser.add_argument(
        "--crypto-experience",
        type=int,
        default=6,
        help="Average team cryptography experience. 0–10 (default: 6).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of human-readable summary.",
    )
    return parser.parse_args()


def print_human(results: List[Dict[str, Any]], summary: Dict[str, Any]) -> None:
    print("🧭 web3_arch_navigator")
    print("")
    print("Input profile:")
    print(f"  Need privacy           : {results[0]['privacyNeed']} / 10")
    print(f"  Need formal verification: {results[0]['formalNeed']} / 10")
    print(f"  Need throughput        : {results[0]['throughputNeed']} / 10")
    print(f"  Latency tolerance      : {results[0]['latencyTolerance']} / 10")
    print(f"  Team crypto experience : {results[0]['cryptoExperience']} / 10")
    print("")
    print("Fit scores by architecture:")
    for r in sorted(results, key=lambda x: x["fitScore"], reverse=True):
        bar = "█" * int(r["fitScore"] * 20)
        print(f"- {r['name']} ({r['profile']}): {r['fitScore']:.3f} ({r['fitLabel']}) {bar}")
    print("")
    print("Recommended direction:")
    print(f"  → {summary['bestName']} ({summary['bestProfile']})")
    print("")
    best = next(r for r in results if r["profile"] == summary["bestProfile"])
    print("Why this might fit:")
    print(f"  {best['tagline']}")
    print("")
    print("Short description:")
    print(f"  {best['description']}")


def main() -> None:
    args = parse_args()

    need_privacy = max(0, min(10, args.need_privacy))
    need_formal = max(0, min(10, args.need_formal))
    need_throughput = max(0, min(10, args.need_throughput))
    latency_tolerance = max(0, min(10, args.latency_tolerance))
    crypto_experience = max(0, min(10, args.crypto_experience))

    results: List[Dict[str, Any]] = []
    for profile in PROFILES.values():
        results.append(
            score_fit(
                profile=profile,
                need_privacy=need_privacy,
                need_formal=need_formal,
                need_throughput=need_throughput,
                tolerance_latency=latency_tolerance,
                team_crypto_experience=crypto_experience,
            )
        )

    summary = summarize_recommendation(results)

    if args.json:
        payload: Dict[str, Any] = {
            "inputs": {
                "needPrivacy": need_privacy,
                "needFormal": need_formal,
                "needThroughput": need_throughput,
                "latencyTolerance": latency_tolerance,
                "cryptoExperience": crypto_experience,
            },
            "results": results,
            "summary": summary,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(results, summary)


if __name__ == "__main__":
    main()
