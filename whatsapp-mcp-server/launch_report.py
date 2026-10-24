"""Summarise who has been starting the WhatsApp MCP server.

    python3 launch_report.py            # last 24h
    python3 launch_report.py --hours 72
"""
import argparse
import collections
import json
import os
import time

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "launches.jsonl")

ap = argparse.ArgumentParser()
ap.add_argument("--hours", type=float, default=24)
args = ap.parse_args()
cutoff = time.time() - args.hours * 3600

rows = []
with open(LOG) as f:
    for line in f:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r["epoch"] >= cutoff:
            rows.append(r)


def origin(r):
    # The first ancestor that isn't uv/claude says what started the session.
    for a in r["ancestry"]:
        name = a["cmd"].split()[0].rsplit("/", 1)[-1]
        if name not in ("uv", "claude", "node"):
            return f'{a["user"]}: {a["cmd"][:90]}'
    return "(no ancestor beyond claude)"


print(f"{len(rows)} launches in the last {args.hours:g}h\n")
for label, key in (("By hour", lambda r: r["ts"][:13]),
                   ("By origin", origin),
                   ("By entrypoint", lambda r: r["env"].get("CLAUDE_CODE_ENTRYPOINT", "?")),
                   ("Over SSH from", lambda r: r["env"].get("SSH_CONNECTION", "local").split(" ")[0]),
                   ("Working dir", lambda r: r["env"].get("PWD", "?"))):
    print(label)
    for k, n in collections.Counter(map(key, rows)).most_common(10):
        print(f"  {n:5}  {k}")
    print()
