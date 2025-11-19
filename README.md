# web3_arch_navigator

A tiny command line helper that suggests which kind of architecture your project is closer to:

- an Aztec-style zk rollup
- a Zama-style FHE compute stack
- a soundness-first protocol lab

It does not connect to any chain. Instead, it scores your project along privacy, soundness, performance, and complexity axes and prints a ranked list of fits plus a recommendation.


Repository layout

This repository intentionally contains exactly two files:

- app.py
- README.md


Concept

Many Web3 teams are trying to decide whether they are:

- more like a privacy rollup (Aztec style)
- more like an encrypted compute product (Zama style)
- more like a formally verified protocol (soundness oriented)

web3_arch_navigator asks you for a few high-level signals:

- How badly you need privacy on or around chain
- How strongly you care about formal verification and proofs
- How much throughput you think you need
- How tolerant you are to latency from proofs or FHE
- How experienced your team is with cryptography

It then scores three conceptual profiles and shows which direction might be the most natural fit for your roadmap.


Installation

Requirements:

- Python 3.8 or newer

Steps:

1. Create a new GitHub repository with any name.
2. Place app.py and this README.md file in the root of the repository.
3. Make sure python is on your PATH (either python or python3).
4. No external dependencies are required; the script uses only the standard library.


Usage

All commands below are meant to be run from the root of the repository.

Quick run with defaults:

python app.py

Prefer strong privacy, strong formal verification, and accept some latency:

python app.py --need-privacy 9 --need-formal 9 --need-throughput 5 --latency-tolerance 6 --crypto-experience 7

High throughput chain with moderate privacy and little tolerance for latency:

python app.py --need-privacy 5 --need-formal 6 --need-throughput 9 --latency-tolerance 3 --crypto-experience 5

Team with low cryptography experience trying to decide where to start:

python app.py --need-privacy 7 --need-formal 5 --need-throughput 6 --latency-tolerance 7 --crypto-experience 2


JSON output

If you want to integrate the navigator into dashboards or internal tools, you can request JSON:

python app.py --need-privacy 8 --need-formal 7 --need-throughput 6 --json

The JSON document includes:

- inputs (your 0–10 scores)
- results (per-profile fit scores and labels)
- summary (best profile and ranking)


How it works

For each profile (aztec, zama, soundness), the script stores:

- privacyFocus
- soundnessFocus
- performanceFocus
- complexity

Your answers are normalized to a 0–10 scale and compared to each profile. A composite fit score is computed using:

- closeness of privacy needs to the profile
- closeness of soundness needs to the profile
- closeness of throughput needs to the profile
- a penalty when latency tolerance is low but complexity is high
- a penalty when team cryptography experience is below the profile’s complexity

The score is then clamped between 0 and 1 and labeled as:

- excellent
- good
- moderate
- weak


Interpreting the results

The tool is not diagnostic or prescriptive. It is a structured way to have the “what are we actually building?” conversation:

- If Aztec-style scores highest, your project might trend toward a privacy rollup with encrypted state and zk circuits over Ethereum.
- If Zama-style scores highest, you might be closer to an FHE-heavy architecture with encrypted compute in and around Web3 data.
- If the soundness-first profile wins, it might be worth leaning into specifications, proofs, and clean, formally shaped protocols.

You can rerun the tool as your priorities shift or as your team gains more cryptography experience.


Notes

- All numbers and weights are illustrative and intentionally simple.
- The script does not model economics, specific chains, or vendor products.
- It is safe to run in any environment because it does not talk to a network or wallet.
- You are encouraged to fork the repository and tune the profiles or scoring rules to match your own reality.
