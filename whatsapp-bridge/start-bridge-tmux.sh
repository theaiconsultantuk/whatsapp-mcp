#!/bin/bash
# Launched by com.whatsapp.bridge LaunchAgent.
# Runs whatsapp-bridge inside a detached tmux session you can attach to:
#     tmux attach -t wa-bridge      (detach again with Ctrl-b d)
#
# 22 Sep 2026 — BUG FIXED HERE. The old guard was `if ! tmux has-session`, which
# treated the EXISTENCE of a wa-bridge session as proof the bridge was running.
# tmux-resurrect restores a wa-bridge session on boot — shell prompt, old scrollback,
# no loop inside it. So has-session said yes, this script skipped starting the bridge,
# and launchd happily reported the wrapper healthy. The bridge was down for 5 days
# (17-22 Sep) and nothing anywhere said so.
# Generalise: "process X exists" is never evidence that X is doing anything. Guard on
# the real worker (pgrep -x whatsapp-bridge), never on its container.

SESSION="wa-bridge"
DIR="${WA_BRIDGE_DIR:-$HOME/ClaudeProjects/whatsapp-mcp/whatsapp-bridge}"
TMUX="/opt/homebrew/bin/tmux"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

bridge_alive() { pgrep -x whatsapp-bridge >/dev/null 2>&1; }

start_loop() {
  "$TMUX" kill-session -t "$SESSION" 2>/dev/null
  "$TMUX" new-session -d -s "$SESSION" -c "$DIR" \
    "while true; do echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] starting whatsapp-bridge\"; ./whatsapp-bridge; echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] bridge exited (code \$?), restarting in 5s\"; sleep 5; done"
  log "wa-bridge session (re)created"
}

if ! "$TMUX" has-session -t "$SESSION" 2>/dev/null; then
  log "no wa-bridge session"
  start_loop
elif ! bridge_alive; then
  sleep 5                       # a real loop restarts within ~5s; don't race it
  if ! bridge_alive; then
    log "wa-bridge session exists but no whatsapp-bridge process — tmux-resurrect ghost, recreating"
    start_loop
  fi
fi

# Supervise. Exit if the tmux server dies (launchd KeepAlive rebuilds everything);
# rebuild the session ourselves if the worker stays dead inside a live session.
while "$TMUX" has-session -t "$SESSION" 2>/dev/null; do
  sleep 30
  if ! bridge_alive; then
    sleep 25                    # grace for the inner 5s restart loop
    bridge_alive || { log "whatsapp-bridge still dead inside a live session — rebuilding"; start_loop; }
  fi
done
log "tmux session gone — exiting so launchd can rebuild"
