# WhatsApp Bridge: Async Event Handling Fix

**Date:** 2026-03-30
**File modified:** `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge/main.go`

## Problem

The bridge was producing constant warnings like:

```
[Client WARN] Node handling took 1m17.483243083s for <message ...>
[Client WARN] Node handling is taking long for <message ...> (started 30.01s ago)
```

Messages were also being missed/dropped during busy periods.

## Root Cause

The whatsmeow library processes events **synchronously** in a single event loop. Our event handler called `handleMessage()` directly, which runs two potentially slow operations:

1. **`GetChatName()`** — does a SQLite lookup, and if the chat name isn't cached, makes a **network call** to WhatsApp (`client.GetGroupInfo()` or `client.Store.Contacts.GetContact()`). These calls were taking 20-90+ seconds.

2. **`StoreMessage()` / `StoreChat()`** — SQLite writes that can occasionally block.

While one message was being processed, the event loop was frozen. No other messages could be received, causing:
- "Node handling took..." warnings (whatsmeow's built-in slow handler detection)
- Missed messages (the event loop couldn't accept new events)

## Fix

### 1. Async Event Handling (main.go ~line 910)

Wrapped `handleMessage` and `handleHistorySync` in goroutines so the event handler returns immediately:

```go
// Before (blocking)
case *events.Message:
    handleMessage(client, messageStore, v, logger)

// After (non-blocking)
case *events.Message:
    go handleMessage(client, messageStore, v, logger)
```

Same change applied to `handleHistorySync`.

### 2. SQLite WAL Mode + Busy Timeout (main.go ~line 57)

Since messages now process concurrently, multiple goroutines may write to SQLite simultaneously. Added WAL mode and a busy timeout to handle this safely:

```go
// Before
db, err := sql.Open("sqlite3", "file:store/messages.db?_foreign_keys=on")

// After
db, err := sql.Open("sqlite3", "file:store/messages.db?_foreign_keys=on&_journal_mode=WAL&_busy_timeout=5000")
```

- **WAL (Write-Ahead Logging):** Allows concurrent reads while a write is in progress, instead of locking the entire database.
- **busy_timeout=5000:** If the database is locked, wait up to 5 seconds before returning an error (instead of failing immediately).

## How to Apply

Restart the bridge process:

```bash
cd /Volumes/Courses/Keto/whatsapp-mcp/whatsapp-bridge
go build -o whatsapp-client .
./whatsapp-client
```

## Expected Result

- No more "Node handling took..." warnings
- Reliable message delivery with no drops
- Slightly higher memory usage (one goroutine per concurrent message, negligible)
