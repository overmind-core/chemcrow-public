#!/usr/bin/env python3
"""Call the running ChemCrow agent server.

Usage (Overmind shell command or manual):
    python query_agent.py "What is the MW of tylenol?"

Reads AGENT_URL from the environment (default: http://localhost:8000).
Prints the agent's answer to stdout and exits 0 on success, 1 on error.
"""

import json
import os
import sys
import urllib.request

AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8080")


def main():
    if len(sys.argv) < 2:
        print("Usage: query_agent.py <question>", file=sys.stderr)
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    payload = json.dumps({"query": query}).encode()

    req = urllib.request.Request(
        f"{AGENT_URL}/run",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read())
            print(body.get("output", ""))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"Agent error: {body.get('error', e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
