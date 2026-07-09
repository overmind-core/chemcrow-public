#!/usr/bin/env python3
import sys

from chemcrow.agents import ChemCrow


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = sys.stdin.read().strip()

    if not query:
        print("Usage: run_agent.py <question>", file=sys.stderr)
        sys.exit(1)

    agent = ChemCrow(streaming=False, local_rxn=True)
    print(agent.run(query))


if __name__ == "__main__":
    main()
