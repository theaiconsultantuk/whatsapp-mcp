# MCP LaunchAgents Documentation

## Overview

This document describes the macOS LaunchAgent setup for three Model Context Protocol (MCP) servers:
- WhatsApp Bridge MCP Server
- Slack MCP Server
- Obsidian MCP Server

All services are configured to run automatically on login and restart on crashes.

---

## Service Details

### 1. WhatsApp Bridge MCP

**Purpose:** Bridges WhatsApp messages to the MCP protocol, providing REST API access to WhatsApp functionality.

| Property | Value |
|----------|-------|
| **Label** | `com.whatsapp.bridge` |
| **Executable** | `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/whatsapp-bridge` |
| **Working Directory** | `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge` |
| **Plist Location** | `~/Library/LaunchAgents/com.whatsapp.bridge.plist` |
| **Stdout Log** | `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/logs/stdout.log` |
| **Stderr Log** | `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/logs/stderr.log` |
| **REST API Port** | `8080` |
| **Database** | `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/store/messages.db` |

**Features:**
- REST API for sending WhatsApp messages
- Message history storage in SQLite
- QR code authentication web interface at `http://localhost:8080/qr`
- Automatic reconnection on disconnection
- Media message support (images, audio, video, documents)

---

### 2. Slack MCP Server

**Purpose:** Provides MCP interface to Slack workspace functionality.

| Property | Value |
|----------|-------|
| **Label** | `com.slack.mcp` |
| **Executable** | `/Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server/run-mcp-server.sh` |
| **Working Directory** | `/Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server` |
| **Plist Location** | `~/Library/LaunchAgents/com.slack.mcp.plist` |
| **Stdout Log** | `/Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server/logs/stdout.log` |
| **Stderr Log** | `/Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server/logs/stderr.log` |
| **Environment** | Loads from `.env` file in working directory |

---

### 3. Obsidian MCP Server

**Purpose:** Provides MCP interface to Obsidian vault functionality.

| Property | Value |
|----------|-------|
| **Label** | `com.obsidian.mcp` |
| **Executable** | `/Users/paulcowen/.nvm/versions/node/v20.18.3/bin/obsidian-mcp-server` |
| **Working Directory** | `/Users/paulcowen` |
| **Plist Location** | `~/Library/LaunchAgents/com.obsidian.mcp.plist` |
| **Stdout Log** | `/Users/paulcowen/Library/Logs/obsidian-mcp-stdout.log` |
| **Stderr Log** | `/Users/paulcowen/Library/Logs/obsidian-mcp-stderr.log` |
| **Node Version** | v20.18.3 (via nvm) |

---

## Management Commands

### Loading Services (Enable Auto-Start)

```bash
# Load all services
launchctl load ~/Library/LaunchAgents/com.whatsapp.bridge.plist
launchctl load ~/Library/LaunchAgents/com.slack.mcp.plist
launchctl load ~/Library/LaunchAgents/com.obsidian.mcp.plist
```

### Starting/Stopping Services

```bash
# Start
launchctl start com.whatsapp.bridge
launchctl start com.slack.mcp
launchctl start com.obsidian.mcp

# Stop
launchctl stop com.whatsapp.bridge
launchctl stop com.slack.mcp
launchctl stop com.obsidian.mcp

# Restart
launchctl stop com.whatsapp.bridge && launchctl start com.whatsapp.bridge
```

### Checking Status

```bash
# Check all MCP services
launchctl list | grep -E "slack|obsidian|whatsapp"

# Check specific service
launchctl list | grep com.whatsapp.bridge
```

---

## Log Locations

### WhatsApp Bridge
```bash
tail -f /Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/logs/stdout.log
tail -f /Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/logs/stderr.log
```

### Slack MCP
```bash
tail -f /Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server/logs/stdout.log
tail -f /Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server/logs/stderr.log
```

### Obsidian MCP
```bash
tail -f /Users/paulcowen/Library/Logs/obsidian-mcp-stdout.log
tail -f /Users/paulcowen/Library/Logs/obsidian-mcp-stderr.log
```

---

## Troubleshooting

### Service Won't Start

1. Check if plist exists: `ls -la ~/Library/LaunchAgents/com.<service>.plist`
2. Check plist syntax: `plutil -lint ~/Library/LaunchAgents/com.<service>.plist`
3. Check executable permissions: `ls -la <path-to-executable>`
4. Check logs for errors: `tail -50 <stderr-log-path>`

### WhatsApp Bridge Specific

- **Device logs out:** Ensure phone has stable internet, remove other linked devices
- **QR won't scan:** Use `http://localhost:8080/qr` for larger QR code
- **Port 8080 in use:** Kill process: `lsof -ti:8080 | xargs kill -9`

---

## Quick Reference

| Service | Label | Logs Path |
|---------|-------|-----------|
| WhatsApp | `com.whatsapp.bridge` | `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/logs/` |
| Slack | `com.slack.mcp` | `/Volumes/Courses/Scripts/Python/MCP/Slack-MCP/slack-mcp-server/logs/` |
| Obsidian | `com.obsidian.mcp` | `/Users/paulcowen/Library/Logs/obsidian-mcp-*.log` |

---

**Version:** 1.0
**Date:** 2025-12-21
**Status:** WhatsApp Bridge connected and operational
